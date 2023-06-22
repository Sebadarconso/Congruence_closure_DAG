import re
import itertools

from pyparsing import nestedExpr
from solver import Node
from pysmt.smtlib.parser import SmtLibParser

class Parser:

    def __init__(self, graph):
        self.customParser = nestedExpr('(', ')')
        self.graph = graph
        self.ids = set()
        self.atoms_dict = dict()
    
    ## function for parsing strings
    def parse(self, input):
        input = input.replace(' ', '')
        clauses = set(input.split('&'))
        res = set()
        repeated = set()

        ## pre-process for clauses
        for clause in clauses:
            clause = clause.replace('!', '')
            if clause[0] == '(':
                clause = clause[1:-1]
            parts = clause.split('=')
            res.add(parts[0])
            res.add(parts[1])

        ## check if a term in the clauses set is a subterm of another e.g. f(a) is a subterm of f(f(a))
        ## so we can focus only on the bigger one
        for element1 in res:
            for element2 in res:
                if element1 != element2 and element1 in element2 and element2[element2.find(element1) + len(element1)] in ['=', '(', ')']:
                    repeated.add(element1)
                    break
        
        ## additional control on the list of terms
        final = [string for string in res if string not in repeated]
        final2 = final.copy()
        for i in range(len(final)):
            for j in range(i+1, len(final)):
                if final[i] in final[j] and final[i] in self.atoms_dict:
                    final2[i] = None
        final2 = [x for x in final2 if x != None]
            

        ## parsing of atoms, this returns a list of lists, e.g f(f(a)) -> ['f' , ['f' ['a']]]
        for atom in final2:
            atom_as_list = self.customParser.parseString('(' + atom + ')').asList()
            self.parse_clause(atom_as_list[0])
    
    ## function for parsing smt files
    def parse_smt(self, input):
        input = input.replace(' ', '') # remove blank spaces
        clauses = set(input.split('&')) # split the conjunctions
        res = set()
        repeated = set()

        for clause in clauses:
            clause = clause.replace('!', '')
            if clause[0] == '(':
                clause = clause[1:-1]
            parts = clause.split('=')
            res.update(parts)

        ## check a string is a substring of an existing formula
        for element1 in res:
            for element2 in res:
                if element1 != element2 and element1 in element2 and element2[element2.find(element1) + len(element1)] in ['=', '(', ')']:
                    repeated.add(element1)
                    break
        
        final = res - repeated

        for atom in final:
            atom_as_list = self.customParser.parseString(f'({atom})').asList()
            self.parse_clause(atom_as_list[0])
        
    ## main function for parsing a clause, the clause is in the form of a list as it is 
    ## the output of the atom_as_list = self.customParser.parseString('(' + atom + ')').asList() function
    def parse_clause(self, atom_as_list:list):
        tmp = []

        ## extract arguments and function names
        for term in atom_as_list:
            if not isinstance(term, list):
                for t in term.split(','):
                    if not t == '': ## found two leaf arguments 
                        tmp.append(t) 
            else:
                tmp.append(term) ## term is a list so we want to extract the function name and the arguments 
        
        clause = tmp
        children = []
        atoms_dict = self.atoms_dict  
        graph_add_node = self.graph.add_node  
        node_string = self.graph.node_string  

        ## create the actual nodes for the DAG
        for i, literal in enumerate(clause):
            if isinstance(literal, list): ## if it's a list means that there are still nested functions/arguments in it 
                continue
            id = self.new_id() ## generate a new uique id
            if i + 1 < len(clause) and isinstance(clause[i + 1], list): ## there are still elements in the clause and the next one is a list 
                args = self.parse_clause(clause[i + 1]) ## get the arguments
                id_list = [arg.id for arg in args]  ## keep track of the ids that will serve as children 
            else:
                id_list = [] ## in this case we are in a leaf so it has no children 
            new_node = Node(id=id, fn=literal, args=id_list, find=id, ccpar=set()) ## create the node
            children.append(new_node)
            graph_add_node(new_node)
            atoms_dict[node_string(new_node.id).replace(' ', '')] = id ## dictionary to keep track of the nodes and their respective ids

        return children
    
    ## new id generator
    def new_id(self) -> str:
        id = next(i for i in itertools.count(1) if i not in self.ids)
        self.ids.add(id)
        return id

## function for get the equalities and the inequalities
def eq_ineq(equations, atoms_dict):
    equalities, inequalities = [], []
    forbidden_list = set() 

    ## split over the conjunction
    equations = equations.split('&')

    for eq in equations:
        if eq.startswith('('):
            eq = eq[1:-1] ## remove redundant parentheses 
        
        ## split equalities and inequalities and add to the respective lists
        parts = [atoms_dict[part.replace(' ', '')] for part in eq.split('!=')] if '!' in eq else [atoms_dict[part.replace(' ', '')] for part in eq.split('=')]

        ## if it's a negation append the parts in the inequalities and in the forbidden list
        if '!' in eq:
            inequalities.append(parts)
            forbidden_list.add(tuple(parts))
        else:
            equalities.append(parts)

    return equalities, inequalities, forbidden_list

## class for parsing smt2 files
class Custom_parser():
    def __init__(self):
        self.parser = SmtLibParser()

    def parse(self, filename):
        ## get the script and read it 
        script = SmtLibParser().get_script_fname(filename)
        f = script.get_strict_formula().serialize().__str__()[1:-1].replace(' ', '')
        symbol = '&'
        final = []

        ## if it's not a disjunction we split over the conjunction and we store all the atoms
        if '|' not in f:
            result = [item[1:-1] if item.startswith('(') else item for item in f.split(symbol)]
            final = [res.replace('!', '').replace('=', '!=')[1:-1] if '!' in res else res for res in result]
        else:
            return or_eq_parser(f)

        return symbol.join(final)

## function for parsing the disjunctions
## input: e.g f(a) & f(b) | f(b) & f(c) 
## output: ['f(a) & f(b)' , 'f(b) & f(c)']
def or_eq_parser(input_string):
    input_string = input_string.replace(' ', '')
    split_input = input_string.split('|')
    ## regex for matching all the formulas inside parentheses and separated by the equal symbol
    pattern = r'(!?\((\w+)=(\w+)\))'
    final = []

    for s in split_input:
        matches = re.findall(pattern, s)
        result = [f"{formula[1]}{'!=' if '!' in formula[0] else '='}{formula[2]}" for formula in matches]
        final.append('&'.join(result)) ## result is a list of conjunctions

    return final
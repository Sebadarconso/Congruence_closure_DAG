from pysmt.smtlib.parser import SmtLibParser
import re

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
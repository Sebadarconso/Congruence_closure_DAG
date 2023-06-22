import os
import sys

from time import time
from custom_parser import *
from solver import DAG

## Function that performs the actual solving algorithm
def run(string):
    start = time()
    print(f"Checking formula: {string}")

    ## instantiate the graph class and the parser class
    solver = DAG()
    parser = Parser(solver)

    ## parse the string
    parser.parse(string)

    ## get equalities, inequalities, forbidden list and adding them to the graph
    equalities, inequalities, forbidden_list = eq_ineq(string.strip(), parser.atoms_dict)
    solver.add_forbidden_list(forbidden_list)
    solver.add_equalities(equalities)
    solver.add_inequalities(inequalities)

    # set the ccpar for each node 
    solver.set_ccpar()
    print(f"Equalities  found: {solver.equalities}")
    print(f"Inequalities found: {solver.inequalities}")

    ## solve
    outcome = solver.solve()
    end = time()
    if solver.solve() == "SAT":
        outcome = "\033[32m" + outcome + "\033[0m"
        print(f"The formula is: {outcome}, execution time: {end - start:.5f} seconds")
        print('\033[34m' + '-'*90 + '\033[0m')
        return "SAT"
    else:
        outcome = "\033[31m" + outcome + "\033[0m" 
    print(f"The formula is: {outcome}, execution time: {end - start:.5f} seconds")
    print('\033[34m' + '-'*90 + '\033[0m')

def main():
    directory_txt = './input_txt'
    directory_smt = './input_smt2'
    # directory_txt = sys.argv[1]
    # directory_smt = sys.argv[2]
        
    print('\033[33m' + '*'*90 + '\033[0m')
    print("CHECKING TXT FILE")

    file_names = os.listdir(directory_txt)

    print('\033[33m' + '*'*90 + '\033[0m')
    for file_name in file_names:
        try:
            file_path = os.path.join(directory_txt, file_name)
            with open(file_path, 'r') as file:
                for line in file.readlines():
                    line = line.split('#', 1)[0]
                    line = line.strip()

                    ## if it's a formula in DNF
                    if '|' in line:

                        ## split over the or 
                        parts = line.split('|')
                        print('*'*90)
                        print("Checking all parts of the formula in DNF")
                        print(parts)

                        ## iterate over the formulas in end
                        for part in parts:

                            ## if only one formula is SAT the algorithm stops and returns SAT
                            ## otherwise it continues and if all the formulas are UNSAT returns UNSAT
                            if run(part.replace(' ', '')[1:-1]) == 'SAT':
                                print('*'*90)
                                break
                    else:

                        ## evaluating a conjunction of equalities and inequalities, returns SAT or UNSAT
                        run(line)
        except FileNotFoundError:
            print(f"File {file_name} not found")
        except IOError:
            print(f"Error occurred while reading file {file_name}")
    
    print('\033[33m' + '*'*90 + '\033[0m')
    print("CHECKING SMT FILES")

    file_names_smt = os.listdir(directory_smt)
    
    print('\033[33m' + '*'*90 + '\033[0m')
    for file_smt in sorted(file_names_smt):

        ## instanciate the class for parsing smt2 files
        parser_smt = Custom_parser()
        try:
            file_path_smt = os.path.join(directory_smt, file_smt)

            ## parsing smt file
            f = parser_smt.parse(file_path_smt)

            ## if the parser returns a string means that the smt2 file contains only conjunctions of equalities and inequalities
            if isinstance(f, str):
                run(f)

            ## if the parse returns a list means that the smt2 file contains a formula in DNF
            elif isinstance(f, list):
                print('*'*90)
                print("Checking all parts of the formula in DNF")

                ## iterate over all the formulas in the list 
                for formula in f:

                    ## if only one formula is SAT returns SAT and terminates
                    if run(formula) == "SAT": break
                print('*'*90)
        except FileNotFoundError:
            print(f"File {file_names_smt} not found")
        except IOError:
            print(f"Error occurred while reading the file {file_names_smt}")

if __name__ == '__main__':
    main()
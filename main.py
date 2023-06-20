import os
from time import time

from custom_parser import *
from solver import DAG

def run(string):
    start = time()
    print(f"Checking formula: {string}")
    solver = DAG()
    parser = Parser(solver)
    parser.parse(string)
    equalities, inequalities, forbidden_list = eq_ineq(string.strip(), parser.atoms_dict)
    solver.add_forbidden_list(forbidden_list)
    solver.add_equalities(equalities)
    solver.add_inequalities(inequalities)
    solver.set_ccpar()
    print(f"Equalities  found: {solver.equalities}")
    print(f"Inequalities found: {solver.inequalities}")
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
    directory_txt = 'AUTOMATED_REASONING_FINAL/input_txt'
    directory_smt = 'AUTOMATED_REASONING_FINAL/input_smt2'

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
                    if '|' in line:
                        parts = line.split('|')
                        print('*'*90)
                        print("Checking all parts of the formula in DNF")
                        print(parts)
                        for part in parts:
                            if run(part.replace(' ', '')[1:-1]) == 'SAT':
                                print('*'*90)
                                break
                    else:
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
        parser_smt = Custom_parser()
        try:
            file_path_smt = os.path.join(directory_smt, file_smt)
            f = parser_smt.parse(file_path_smt)
            if isinstance(f, str):
                run(f)
            elif isinstance(f, list):
                print('*'*90)
                print("Checking all parts of the formula in DNF")
                for formula in f:
                    if run(formula) == "SAT": break
                print('*'*90)
        except FileNotFoundError:
            print(f"File {file_names_smt} not found")
        except IOError:
            print(f"Error occurred while reading the file {file_names_smt}")

if __name__ == '__main__':
    main()
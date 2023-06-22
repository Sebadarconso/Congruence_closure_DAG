# Congruence closure with DAG - User Guide

This guide provides instructions for using the Congruence Closure Algorithm with DAG in a Google Colab notebook.

link: https://colab.research.google.com/drive/1hjzsx16ctYb4KszlUrivAsVhvu62flXd

## Table of Contents
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Adding Custom Files](#adding-custom-files)
- [Troubleshooting](#troubleshooting)
- [Most important](#most-important)
## Prerequisites
In the first cell there are all the imports for the dipendencies and the command for cloning the github repo (https://github.com/Sebadarconso/Congruence_closure_DAG), you can click on the play button in the top left of the cell to execute it.

## Usage
After the first cell has finished the execution pass on the next, in this case if you press play you will execute the main function, it takes as arguments the two paths to the directories of the input files, the paths order is important and is path_to_txt first and path_to_smt second, in this colab the path are (e.g: /content/Congruence_closure_dag/pathname_txt)
This cell usually takes some time to conclude at the first execution due to some pysmt packages but after that it runs smoothly. Running this cell without modifying the files will perform the algorithm on the test files that I provided and with the execution flow described in the report and it will output at real time the evaluation of the formulas in the input folders.

## Adding Custom Files
If you want to add custom files to the program there are two way of do it based on the type of file:
- if it's a txt file just drag and drop it in the input_txt folder
- if you want to process a single formula you can simply open the input.txt file in the input_txt folder and add it to the file
- if it's a smt2 file, you can still drag and drop it in the input_smt2 folder but it might be necessary to rename it in order to make it the first of the list (1_input.smt2), so that the program does not incurr in function renaming as I mentioned in the report, note that it will still stop after the first due to that error.
After adding the files all you have to do is press play again on the second cell and the program will print the output like before but with also the output of your formulas.

## Troubleshooting
Other the fact that the first run of the main might be slow and the problem with smt2, there are no particular problems worth of note.

## Most important
The algorithm can process both DNF and plain conjunctions of equalities and inequalities, but there are some some things to keep in mind:

- equalities and inequalites between '&' must not be surrounded by parentheses, for example it has to be like a = b & c = d or a = b & c != d, or 
f(a,b) = f(b,c) & a != b spaces do not represent a problem.
- if the formula is in DNF the parts in '&' should be the only ones surrounded by parentheses and not the whole formula, for example: (a = b & c != d) | (f(a,b) = f(b,c) & a != b) | (...&...&...) ... is a valid formula
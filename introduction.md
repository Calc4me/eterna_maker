# Introduction to the new model
This program is a complete rewriting of my old program from the ground up, meaning it works in a completely different way than before. 

In this project, you will find explanations of all the parameters, plus a good starting set of parameters. However, the explanations can be unclear if you don't understand how the program works.

## How the program works
This program works in three basic steps:
- Generate a "template" of stacks and hairpins
- Find the paired stacks and assign lengths to them, and then insert internal loops between them
  - Optionally, insert pseudoknots here if the user wants
- Generate stacks based on the given lengths and present the result

The template will look something like this: ((\*)\(\*)). The parentheses represent stacks with bulges (no internal loops), and the asterisks represent hairpin loops. The program will ask you if the given template is acceptable, along with detailed statistics if you enabled `template_stats`.

Once you continue, using your paramaters, the program will then generate a finished structure and ask if it is acceptable, again giving you stats if you enabled `full_stats`. This process can be repeated as many times as neccecary. If you set `visualize_structure = True`, then it will show you a visualization of the structure in a seperate window. The window has to be closed for the program to continue.

If you gave a filepath for export, the structure will also be written to that file for ease of use.

Feel free to use the generated structures however you like! A mention of this program would be nice if you do, however. 

-Calc4me :)
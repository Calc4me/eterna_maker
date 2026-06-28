# Introduction to the new model
This program is a complete rewriting of my old program from the ground up, meaning it works in a completely different way than before. 

In the document, you will find explanations of all the parameters, plus a good all-rounder set of parameters. However, the explanations can be unclear if you don't understand how the program works.

## How the program works
This program works in three basic steps:
- Generate a "template" of stacks and hairpins
- Find the paired stacks and assign lengths to them
- Generate stacks based on the given lengths and insert internal loops between the stacks

The template will look something like this: ((\*)\(\*)). The parentheses represent stacks with bulges (no internal loops), and the asterisks represent hairpin loops. The program will ask you if the given template is acceptable to continue with, along with the template's length.

Once you continue, using your paramaters, the program will then generate a finished structure and ask if it is acceptable. This process can be repeated as many times as neccecary. If you set visualize_structure to True, then it will show you a visualization of the structure in a seperate window. The window has to be closed for the program to continue.

Feel free to use the generated structures however you like! A mention of this program would be nice :)
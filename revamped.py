import convertstack
import gentemp
import random
from draw_rna.ipynb_draw import draw_struct

'''
A good set of parameters for well-rounded structures:

# Template Generation
tempchances = [0.85, 0.35]
temprange = [4,12]
bias = 0.025
template = []

# Template Length Assignment
assigntype = 0
mean = 6 
stdev = 2 
lengthrange = [3,10]
probabilities = [0.05, 0.05, 0.1, 0.3, 0.3, 0.1, 0.05, 0.05]

# Loop making
looprange = [1,2]

# Stack Generation
conversionvars = {
    "dotratio": 0.23, 
    "maxcountdiff": 2, 
    "maxposdiff": 1, 
    "onechance": 0.6, 
    "twochance": 0.35,
    "minloopdots": 3,
    "maxloopdots": 6 
}

# Runtime variables
generationContinueFlag = False
looplist = []
stack = []
pairslist = []
tempContinueFlag = False
stopFlag = False

# Other
debug = False
'''

'''
Fun templates:
["(", "(", "(", "(", "*", ")", ")", "(", "*", ")", ")", ")"]
["(", "(", "(", "*", ")", ")", "(", "*", ")", ")"]
["(", "(", "*", ")", ")", "(", "*", ")"]
["(", "(", "*", ")", "(", "*", ")", ")"]
'''

# Template Generation
tempchances = [0.85, 0.45] # Matrix format: [Chance for ( if ( before, chance for ( if ) before]
temprange = [4,10] # Minimum [0]/2 stacks, maximum [1]/2 stacks
bias = 0.025 # Bias towards closing (subtracts from tempchances[0])
rerollchance = 0.25 # Chance to continue after a valid template is generated
user_template = [] # Template runtime variable, set to your template if using your owen, set to [] if not using premade

# Template Length Assignment
assigntype = 0 # 0 = Normally distributed, 1 = Uniformly distributed, 2 = User-made probabilites
mean = 8 # Mean of stack lengths (option 0)
stdev = 2.5 # SD of stack lengths (option 0) 
lengthrange = [3,10] # Range of stack lengths (option 1+2)
probabilities = [0.05, 0.05, 0.1, 0.3, 0.3, 0.1, 0.05, 0.05] # Individual stack length probabilities from lengthrange[0] to lengthrange[1] (option 2)

# Loop making
looprange = [1,2] # Min internal loop size, max internal loop size

# Stack Generation
conversionvars = {
    "dotratio": 0.35, # Ratio of dots to paired bases before removal of adjacent unpaired bases
    "maxcountdiff": 2, # Max difference between unpaired base counts on each side of the generated stack that allows for random unpaired base removal
    "maxposdiff": 1, # Max difference between the position of two unpaired bases to warrant removal of one between sides of a stack
    "maxonesideposdiff": 1, # Max differece between the position of two unpaired bases to warrant removal of one on the same side of a stack
    "onechance": 0.6, # Chance for "." as the inserted unpaired base
    "twochance": 0.35, # Same as above, but "..". The remaining chance between the two is the chance that "..." is inserted.
    "minloopdots": 3, # Minimum unpaired bases in a hairpin
    "maxloopdots": 6 # Maximum unpaired bases in a hairpin
}

# Runtime variables (don't touch)
generationContinueFlag = False
looplist = []
stack = []
pairslist = []
tempContinueFlag = False
stopFlag = False

# Other
debug = False # Print more stuff to help with debugging
visualize_structure = True # Visualize the RNA structure (close the window to continue)

# Intro
print("------RNA secondary structure generator by Calc4me-------")
print("See introduction.md and README.md if you haven't already!")
print("Starting...")
print("")

# Main Loop
while not stopFlag:

    # Reset vars
    tempContinueFlag = False
    generationContinueFlag = False
    stopFlag = False
    looplist.clear()
    stack.clear()
    pairslist.clear()
    template = user_template.copy()

    # Generate template list:
    # Check if there is no user-made template
    if len(template) < 1:
        # While the user is unsatisfied
        while not tempContinueFlag:
            template = ["("]
            # While the template length is out of range
            while not temprange[0] < len("".join(template).replace("*", "")) < temprange[1]:
                template = ["("]
                # Generate template
                gentemp.generatetemp(template, tempchances, bias, debug=debug, maxlen=temprange[1]*1.5)
            structure = "".join(template)
            answer = input(f'Is {structure} (length {len(structure.replace("*", ""))}) acceptable? (Y/N) ')
            # If it is acceptable, continue
            if answer.lower() == "y":
                tempContinueFlag = True
                print("")
            else:
                tempContinueFlag = False

    # Generate template to modify
    working_template = template.copy()

    # Insert loops:
    looplist.clear()
    for pos in range(len(working_template) - 1):
        # If pos and pos+1 in the template are both stacks
        if working_template[pos] in "()" and working_template[pos + 1] in "()":
            # Add an internal loop to the looplist
            looplist.append("." * random.randint(looprange[0], looprange[1]))
        else:
            # Otherwise, add no loop
            looplist.append("")
    # Add 1 more no loop so template and looplist are the same size so zip(template,looplist) works.
    looplist.append("")
    # "Zipper" them together
    working_template = [item for pair in zip(working_template, looplist) for item in pair]

    # Assign length values to them and generate stacks:
    # Find all the stacks and their pairs and add them to a list
    pairslist.clear()
    stack.clear()
    for pos, char in enumerate(working_template):
        if char == "(":
            stack.append(pos)
        elif char == ")":
            if not stack:
                raise ValueError("Unbalanced template")
            open_pos = stack.pop()
            pairslist.append([open_pos, pos])
    # Sort the list by the first position
    pairslist.sort(key=lambda pair: pair[0])
    if debug:
        print(pairslist)

    # If the user is unsatisfied with the stacks added
    while not generationContinueFlag:
        if assigntype == 2:
            # Generate lengths for option 2
            lengths = list(range(lengthrange[0], lengthrange[1]+1))
        for i in range(len(pairslist)):
            # Normally distribute the stack sizes
            if assigntype == 0:
                stacksize = max(1, round(random.gauss(mean, stdev)))
            elif assigntype == 1:
                stacksize = random.randint(lengthrange[0], lengthrange[1])
            elif assigntype == 2:
                stacksize = random.choices(lengths, weights=probabilities, k=1)[0]
            # Generate the stack and replate the template (s and )s with it
            stacktoinsert = convertstack.convertstack(stacksize,conversionvars["dotratio"],conversionvars["onechance"],conversionvars["twochance"],conversionvars["maxcountdiff"],conversionvars["maxposdiff"],conversionvars["maxonesideposdiff"])
            working_template[pairslist[i][0]] = stacktoinsert[1]
            working_template[pairslist[i][1]] = stacktoinsert[2]
            # If it's a hairpin, add that too
            if (pairslist[i][0] + 2 < len(working_template)
                and working_template[pairslist[i][0]+2] == "*"):
                working_template[pairslist[i][0]+2] = "".join(["."] * random.randint(conversionvars["minloopdots"], conversionvars["maxloopdots"]))
        if debug:
            print(working_template)
        # Query
        structure = "".join(working_template)
        if visualize_structure:
                draw_struct("".join(['A']*len(structure)),structure)
        answer = input(f'Is {structure} (length {len(structure)}) acceptable? (Y/N) ')
        # If it is acceptable, stop generation
        print("")
        if answer.lower() == "y":
            generationContinueFlag = True
            print(f'The final structure is:')
            print(structure)
        else:
            generationContinueFlag = False
    
    # If the user wants to stop, stop, otherwise go to start
    answer = input(f'Stop? (y/n) ')
    if answer.lower() == "y":
        print("Bye! :)")
        stopFlag = True
import convertstack
import gentemp
import random
from draw_rna.ipynb_draw import draw_struct

# Template Generation
tempchances = [0.85, 0.35]
temprange = [4,12]
bias = 0.025
reroll_chance = 0.25
user_template = []

# Template Length Assignment
assigntype = 0
mean = 6 
stdev = 2 
lengthrange = [3,10]
probabilities = [0.05, 0.05, 0.1, 0.3, 0.3, 0.1, 0.05, 0.05]
min_stack_size = 2

# Loop making
looprange = [1,4] # Min internal loop size, max internal loop size

# Stack Generation
conversionvars = {
    "dotratio": 0.23, "maxcountdiff": 2, "maxposdiff": 1, "maxonesideposdiff": 1, 
    "onechance": 0.6, "twochance": 0.35, "minloopdots": 3, "maxloopdots": 6
}

# Runtime variables (don't touch)
generationContinueFlag = tempContinueFlag = stopFlag = False
looplist = []
stack = []
pairslist = []

# Other
debug = False
visualize_structure = True
full_stats = True
export_file = "structure_export.txt"
write_or_append = "a"
seed = None

# Intro
if seed is not None:
    random.seed(seed)
print("------RNA secondary structure generator by Calc4me-------")
print("Read introduction.md and README.md if you haven't already!")
print("")

# Main Loop
while not stopFlag:
    # Reset vars
    tempContinueFlag = False
    generationContinueFlag = False
    template = user_template.copy()
    # Generate template list, first check if there is no user-made template
    if len(template) < 1:
        # While the user is unsatisfied
        while not tempContinueFlag:
            while True:
                template = ["("]
                gentemp.generatetemp(template, tempchances, bias, debug=debug, maxlen=temprange[1]*1.5)
                if temprange[0] < len("".join(template).replace("*", "")) < temprange[1]:
                    break
            structure = "".join(template)
            answer = input(f'Is {structure} (length {len(structure.replace("*", ""))}) acceptable? (Y/N) ')
            # If it is acceptable, continue
            if answer.lower() == "y": 
                print("Continuing to loop and stack generation. \n")
                tempContinueFlag = True
            else: tempContinueFlag = False

    # If the user is unsatisfied with the stacks and loops added
    while not generationContinueFlag:
        # Clear detritus in the vars
        looplist.clear()
        stack.clear()
        pairslist.clear()
        # Generate template to modify
        working_template = template.copy()

        # Insert loops:
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
        working_template = [item for pair in zip(working_template, looplist) for item in pair]

        # Assign length values to them and generate stacks:
        # Find all the stacks and their pairs and add them to a list
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

        # For full stats
        bulgecount = 0
        stacklengths = []
        hairpinsizes = []

        if assigntype == 2:
            # Generate lengths for option 2
            lengths = list(range(lengthrange[0], lengthrange[1]+1))
        for i in range(len(pairslist)):
            # Normally distribute the stack sizes
            if assigntype == 0:
                stacksize = max(min_stack_size, round(random.gauss(mean, stdev)))
            elif assigntype == 1:
                stacksize = max(min_stack_size, random.randint(lengthrange[0], lengthrange[1]))
            elif assigntype == 2:
                stacksize = max(min_stack_size, random.choices(lengths, weights=probabilities, k=1)[0])
            stacklengths.append(stacksize)
            # Generate the stack and replate the template (s and )s with it
            stacktoinsert = convertstack.convertstack(stacksize,conversionvars["dotratio"],conversionvars["onechance"],conversionvars["twochance"],conversionvars["maxcountdiff"],conversionvars["maxposdiff"],conversionvars["maxonesideposdiff"])
            working_template[pairslist[i][0]] = stacktoinsert[1]
            working_template[pairslist[i][1]] = stacktoinsert[2]
            bulgecount += stacktoinsert[3]
            # If it's a hairpin, add that too
            if (pairslist[i][0] + 2 < len(working_template)
                and working_template[pairslist[i][0]+2] == "*"):
                working_template[pairslist[i][0]+2] = "." * random.randint(conversionvars["minloopdots"],conversionvars["maxloopdots"])
                hairpinsizes.append(len(working_template[pairslist[i][0]+2]))
        if debug:
            print(working_template)
        # Query
        structure = "".join(working_template)
        if visualize_structure:
                draw_struct("".join(['A']*len(structure)),structure)

        structurestats = {
            "Length": len(structure),
            "Base Pairs": structure.count("("),
            "Unpaired Bases": len(structure)-(2*structure.count("(")),
            "Average Stack Length": round(sum(stacklengths)/len(stacklengths), 3),
            "Largest Stack": max(stacklengths),
            "Smallest Stack": min(stacklengths),
            "Hairpins": template.count("*"),
            "Largest Hairpin": max(hairpinsizes),
            "Internal Loops": len("".join(template).replace("*", ""))-template.count("*")-1,
            "Bulges": bulgecount,
            "Pair Density": round(structure.count("(")/len(structure),2)
        } 
        print(f'Is {structure} acceptable?')
        if full_stats:
            print(f'Stats: \nLength: {structurestats["Length"]}, Base Pairs: {structurestats["Base Pairs"]}')
            print(f'Unpaired Bases: {structurestats["Unpaired Bases"]}, Average Stack Length: {structurestats["Average Stack Length"]}')
            print(f'Smallest & Largest Stack: {structurestats["Smallest Stack"]}, {structurestats["Largest Stack"]}')
            print(f'Hairpins: {structurestats["Hairpins"]}, Largest Hairpin: {structurestats["Largest Hairpin"]}')
            print(f'Internal Loops: {structurestats["Internal Loops"]}, Bulges: {structurestats["Bulges"]}')
            print(f'Pair Density: {structurestats["Pair Density"]}')
        answer = input("(Y/N) ")
        # If it is acceptable, stop generation
        if answer.lower() == "y":
            print("")
            generationContinueFlag = True
            if export_file != "":
                with open(export_file, write_or_append) as f:
                    f.write("\n" + structure + f'({structurestats["Length"]}, {structurestats["Base Pairs"]}, {structurestats["Hairpins"]}, {structurestats["Internal Loops"]}, {structurestats["Bulges"]}, {structurestats["Pair Density"]})')
        else: generationContinueFlag = False
    
    # If the user wants to stop, stop, otherwise go to start
    answer = input(f'Stop? (y/n) ')
    if answer.lower() == "y":
        print("\nBye! :)")
        stopFlag = True
    else: print("")
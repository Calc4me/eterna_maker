import stackfuncs
import helpers
import random
from draw_rna.ipynb_draw import draw_struct

# Runtime variables (don't touch)
generationContinueFlag = tempContinueFlag = stopFlag = pkcontinueflag = False
looplist = []
stack = []
pairslist = []
pseudoknotpairs = []
crossedmultis = 0
nummultis = 0

# Template Generation
tempchances = [0.85, 0.45]
temprange = [8,12]
bias = 0.025
reroll_chance = 0.25
user_template = []

# Template Length Assignment
assigntype = 0
mean = 7
stdev = 1.5 
lengthrange = [3,10]
probabilities = [0.05, 0.05, 0.1, 0.3, 0.3, 0.1, 0.05, 0.05]
min_stack_size = 2

# Loop making
looprange = [1,2]

# Stack Generation
conversionvars = {
    "dotratio": 0.35, "maxcountdiff": 2, "maxposdiff": 1, "maxonesideposdiff": 1, 
    "onechance": 0.6, "twochance": 0.35, "minloopdots": 4, "maxloopdots": 5
}

# Pseudoknot Generation
pseudoknots = False
numpseudoknots = 1
pkassigntype = 0
pkmean = 7 
pkstdev = 1.5 
pklengthrange = [3,10]
pkprobabilities = [0.05, 0.05, 0.1, 0.3, 0.3, 0.1, 0.05, 0.05]
pkminsize = 2
surroundrange = [1,2]
hairpinmaxdiff = 1
maxpksfromhairpin = 2
maxpkgenatt = 1000
crossedmultiloops = False

# Other
debug = False
visualize_template = True
visualize_structure = True
template_stats = True
full_stats = True
export_file = "structure_export.txt"
write_or_append = "a"
seed = None

# Intro
if seed is not None:
    random.seed(seed)
print("-------RNA secondary structure generator by Calc4me-------")
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
                nummultis = len(stackfuncs.generatetemp(template, tempchances, bias, debug=debug, maxlen=temprange[1]*1.5, returnpos=True))
                if temprange[0] < len("".join(template).replace("*", "")) < temprange[1]:
                    if debug:
                        print("Generator:", nummultis)
                        print("Finder   :", helpers.findmultipositions(template))
                    break
            structure = "".join(template)
            if visualize_template:
                visualize_temp = "".join(template.copy())
                visualize_temp = visualize_temp.translate(str.maketrans({"(": "((.", ")": ".))", "*": ".."}))
                draw_struct("".join(['A']*len(visualize_temp)),visualize_temp)
            if template_stats:
                fulltemplatestats = {
                    "Length": len(structure.replace("*", "")),
                    "Hairpins": structure.count("*"),
                    "Stacks": structure.count("("),
                    "Multiloops": nummultis,
                    
                }
            print(f'Is {structure} acceptable?')
            if full_stats:
                print(f'Length: {fulltemplatestats["Length"]}, Hairpins: {fulltemplatestats["Hairpins"]}')
                print(f'Stacks: {fulltemplatestats["Stacks"]}, Multiloops: {fulltemplatestats["Multiloops"]}')
            answer = input("(Y/N) ")
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

        # Insert pseudoknots
        if pseudoknots and working_template.count("*") >= 2:
            backup_temp = working_template.copy()
            while not pkcontinueflag:
                # Clear between tries
                pseudoknotpairs.clear()
                attemptcount = 0
                # 
                hairpincounts = [0] * working_template.count("*")
                hairpins = [""] * working_template.count("*")
                if assigntype == 2:
                    # Generate lengths for option 2
                    pklengths = list(range(lengthrange[0], lengthrange[1]+1))
                while len(pseudoknotpairs) < numpseudoknots and attemptcount < maxpkgenatt:
                    candidatepair = sorted([
                                        random.randint(0, working_template.count("*") - 1),
                                        random.randint(0, working_template.count("*") - 1)])
                    attemptcount += 1
                    if 0 != abs(candidatepair[1]-candidatepair[0]) <= hairpinmaxdiff and (candidatepair not in pseudoknotpairs) and (
                        hairpincounts[candidatepair[0]] < maxpksfromhairpin and hairpincounts[candidatepair[1]] < maxpksfromhairpin): 
                            pseudoknotpairs.append(candidatepair)
                            hairpincounts[candidatepair[0]] += 1
                            hairpincounts[candidatepair[1]] += 1
                for i in range(len(pseudoknotpairs)):
                    if assigntype == 0:
                        pksize = max(pkminsize, round(random.gauss(pkmean, pkstdev)))
                    elif assigntype == 1:
                        pksize = max(pkminsize, random.randint(pklengthrange[0], pklengthrange[1]))
                    elif assigntype == 2:
                        pksize = max(pkminsize, random.choices(pklengths, weights=pkprobabilities, k=1)[0])
                    pseudoknotpairs[i].append(pksize)
                    pseudoknotpairs[i].append([random.randint(surroundrange[0], surroundrange[1]),random.randint(surroundrange[0], surroundrange[1])])
                    pseudoknotpairs[i].append([random.randint(surroundrange[0], surroundrange[1]),random.randint(surroundrange[0], surroundrange[1])])
                # Now the format for each one is [hairpin 1 loc, hairpin 2 loc, size, [ldots, rdots], [ldots, rdots]]
                parenthmod = 0
                parenth = [
                    ("[", "]"),
                    ("{", "}"),
                    ("<", ">"),
                ]
                for i in range(len(pseudoknotpairs)):
                    hairpins[pseudoknotpairs[i][0]] += "." * pseudoknotpairs[i][3][0] + parenth[parenthmod][0] * pseudoknotpairs[i][2] + "." * pseudoknotpairs[i][3][1]
                    hairpins[pseudoknotpairs[i][1]] += "." * pseudoknotpairs[i][4][0] + parenth[parenthmod][1] * pseudoknotpairs[i][2] + "." * pseudoknotpairs[i][4][1]
                    parenthmod = (parenthmod + 1) % 3            
                count = 0
                for pos, char in enumerate(working_template):
                    if char == "*":
                        if len(hairpins[count]) > 1:
                            working_template[pos] = hairpins[count].replace("*", "")
                        count += 1
                # Check for validity
                crossedmultis = 0
                if crossedmultiloops:
                    affectedstacks = helpers.findbasesinpks(working_template)
                    stackstocheck = helpers.findmultipositions(working_template)
                    if debug:
                        print(f'Working template: {working_template}')
                        print(f'Affected stacks: {affectedstacks}')
                        print(f'Stacks to check: {stackstocheck}')
                    for multiloop in stackstocheck:
                        if sum(affectedstacks[pos] for pos in multiloop) != 0:
                            if debug:
                                print("MULTILOOP WAS FOUND WITH CROSSING PK")
                            crossedmultis += 1
                        elif debug:
                            print("MULTILOOP WAS FOUND WITHOUT CROSSING PK")
                    if crossedmultis != len(stackstocheck):
                        pkcontinueflag = False
                    else:
                        pkcontinueflag = True
                else:
                    pkcontinueflag = True
                            

            print(f'Generated {len(pseudoknotpairs)}/{numpseudoknots} psuedoknots\n')
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
            stacktoinsert = stackfuncs.convertstack(stacksize,conversionvars["dotratio"],conversionvars["onechance"],conversionvars["twochance"],conversionvars["maxcountdiff"],conversionvars["maxposdiff"],conversionvars["maxonesideposdiff"])
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

        # Stats
        if hairpinsizes == []: hairpinsizes.append(0)
        structurestats = {
            "Length": len(structure),
            "Base Pairs": structure.count("(")+structure.count("<")+structure.count("{")+structure.count("["),
            "Unpaired Bases": len(structure)-(2*(structure.count("(")+structure.count("<")+structure.count("{")+structure.count("["))),
            "Average Stack Length": round(sum(stacklengths)/len(stacklengths), 3),
            "Largest Stack": max(stacklengths),
            "Smallest Stack": min(stacklengths),
            "Hairpins": (structure.replace(".","")).count("()"),
            "Largest Hairpin": max(hairpinsizes),
            "Internal Loops": len("".join(template).replace("*", ""))-template.count("*")-"".join(template).count(")(")-2*fulltemplatestats["Multiloops"]-1,
            "Bulges": bulgecount,
            "Pair Density": round((structure.count("(")+structure.count("<")+structure.count("{")+structure.count("["))*2/len(structure),3),
            "Pseudoknot Density": round((structure.count("[")+structure.count("{")+structure.count("<"))*2/len(structure),3),
            "Pseudoknots": len(pseudoknotpairs),
            "Percent Involved": round(helpers.findbasesinpks(structure).count(1)/len(structure),3),
            "Crossed Multiloop Proportion": round(crossedmultis/nummultis,3),
            "Multiloops": fulltemplatestats["Multiloops"]
        } 
        print(f'Is {structure} acceptable?')
        if full_stats:
            print(f'Stats: \nLength: {structurestats["Length"]}, Base Pairs: {structurestats["Base Pairs"]}')
            print(f'Unpaired Bases: {structurestats["Unpaired Bases"]}, Average Stack Length: {structurestats["Average Stack Length"]}')
            print(f'Smallest & Largest Stack: {structurestats["Smallest Stack"]}, {structurestats["Largest Stack"]}')
            print(f'Hairpins: {structurestats["Hairpins"]}, Largest Hairpin: {structurestats["Largest Hairpin"]}')
            print(f'Internal Loops: {structurestats["Internal Loops"]}, Bulges: {structurestats["Bulges"]}')
            print(f'Pseudoknots: {structurestats["Pseudoknots"]}, Pseudoknot Density: {structurestats["Pseudoknot Density"]}')
            print(f'Pair Density: {structurestats["Pair Density"]}, Proportion Involved in Pseudoknots: {structurestats["Percent Involved"]}')
            print(f'Multiloops: {structurestats["Multiloops"]}, Proportion of Crossed Multiloops: {structurestats["Crossed Multiloop Proportion"]}')
        answer = input("(Y/N) ")
        # If it is acceptable, stop generation
        if answer.lower() == "y":
            print("")
            generationContinueFlag = True
            if export_file != "":
                with open(export_file, write_or_append) as f:
                    f.write("\n" + structure)
        else: generationContinueFlag = False
    
    # If the user wants to stop, stop, otherwise go to start
    answer = input(f'Stop? (y/n) ')
    if answer.lower() == "y":
        print("\nBye! :)")
        stopFlag = True
    else: print("")
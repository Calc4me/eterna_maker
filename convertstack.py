import random

def convertstack(size: int,dratio: float,onechance: float,twochance: float,maxcountdiff: int,maxposdiff: int, maxonesideposdiff: int):
    '''
    Generates a stack from given parameters.
    Parameters:
    Size (integer): The number of paired bases in the stack.
    Dratio (float): The ratio of paired bases to the number of the positions of unpaired bases
    Onechance (float): The chance for an unpaired base position to be "."
    Twochance (float): The chance for an unpaired base position to be "..", the remaining probability is for "..."
    Maxcountdiff (integer): The largest the difference in number of positions of unpaired bases can be from each stack side in order to not warrant rebalancing
    Maxposdiff (integer): The largest the difference in the position of two unpaired bases that is forbidden
    '''


    # Variables
    if size < 1:
        raise ValueError("size must be positive")
    temp = ["("] * size + [")"] * size # The unmodified stack
    dotpos = [] # To store all the positions of the unpaired bases to add
    dellist = set() # To store all the position of the unpaired bases to delete from dotpos
    numdots = min(round(dratio * size), 2 * size) # The number of unpaired bases to add (capped at 2*size)
    counts = [0,0] # Counts of unpaired base positions on each side of the stack
    split = None # Runtime var

    # Generate a sample of unpaired base positions
    dotpos = sorted(random.sample(range(2*size), numdots))

    # Make counts on each side
    for pos in dotpos:
        if pos < size:
            counts[0] += 1
        elif pos > size:
            counts[1] += 1

    # Dotpos cleaning
    for i in range(len(dotpos)):
        # Add for removal dots that are 1 position away from either end of the stack
        if dotpos[i] <= 2 or dotpos[i] >= 2*size-1 or dotpos[i]==size-1 or dotpos[i]==size+1:
            dellist.add(dotpos[i])
        if len(dotpos)-1 > i > 0:
            if abs(dotpos[i]-dotpos[i-1]) <= maxonesideposdiff:
                c = random.choice([0,1])
                dellist.add([dotpos[i], dotpos[i-1]][c])
                if i < size:
                    counts[0] -= 1
                elif i > size:
                    counts[1] -= 1
            elif abs(dotpos[i]-dotpos[i+1]) <= maxonesideposdiff:
                c = random.choice([0,1])
                dellist.add([dotpos[i], dotpos[i+1]][c])
                if i < size:
                    counts[0] -= 1
                elif i > size:
                    counts[1] -= 1 
        # Check through all pairs of dots
        for j in range(len(dotpos)-i-1):
            # Mirror the paired one to the same side as the other
            mirror = 2*size-dotpos[i+j+1]-1
            # If their positions are within the maxposdiff
            if abs(dotpos[i] - mirror) <= maxposdiff:
                # Check to see if the counts are winthin maxcountdiff of eachother
                if abs(counts[0]-counts[1]) <= maxcountdiff:
                    # If they are, randomly select one to remove
                    c = random.choice([0,1])
                    dellist.add([dotpos[i], dotpos[i+j+1]][c])
                    if c == 0 and dotpos[i] not in dellist:
                        counts[0] -= 1
                    elif c == 1 and dotpos[i+j+1] not in dellist:
                        counts[1] -= 1
                else:
                    # Otherwise try to balance them
                    if counts[0] > counts[1]:
                        dellist.add(dotpos[i])
                        if not dotpos[i] in dellist:
                            counts[0] -= 1
                    else:
                        dellist.add(dotpos[i+j+1])
                        if not dotpos[i+j+1] in dellist:
                            counts[1] -= 1

    # Remove all unwanted dotpos
    dotpos = [p for p in dotpos if p not in dellist]

    # Add either ., .., or ... based on random chance
    dotchoice = random.random()
    for i in range(len(dotpos)):
        if dotchoice < onechance:
            temp.insert(dotpos[i] + i, ".")
        elif dotchoice < onechance + twochance:
            temp.insert(dotpos[i] + i, "..")
        else:
            temp.insert(dotpos[i] + i, "...")
    
    # Split the stack 
    leftcount = 0
    for i, char in enumerate(temp):
        if char == "(":
            leftcount += 1
        if leftcount == size:
            split = [temp[:i+1], temp[i+1:]]
            break
    if split is None:
        raise RuntimeError("Stack splitting failed")

    # Return the full stack and its two halves and the bulge count
    return ["".join(temp), "".join(split[0]), "".join(split[1]), len(dotpos)]
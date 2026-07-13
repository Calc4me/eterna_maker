def findbasesinpks(struct):
    '''
    Finds bases affected by pseudoknots and returns a matching list, where 0 = not affected, and 1 = at least one base in the correspoiding structure is affected.
    Parameters:
    Struct (list/string): The given structure
    '''
    if type(struct) == list: temp_struct = "".join(struct)
    else: temp_struct = struct
    typelist = []
    final_typelist = []
    pkdepth = 0
    OPEN_PK = {"[", "{", "<"}
    CLOSE_PK = {"]", "}", ">"}
    for i in range(len(temp_struct)):
        prev = temp_struct[i-1] if i > 0 else None
        if temp_struct[i] in OPEN_PK and prev not in OPEN_PK:
            pkdepth += 1
            typelist.append(1)
        elif temp_struct[i] in CLOSE_PK and prev not in CLOSE_PK:
            pkdepth -= 1
            typelist.append(1)
        elif temp_struct[i] not in OPEN_PK | CLOSE_PK and pkdepth == 0:
            typelist.append(0)
        elif pkdepth > 0 or temp_struct[i] in OPEN_PK | CLOSE_PK:
            typelist.append(1)
    if type(struct) == list:
        for i in range(len(struct)):
            if (sum(typelist[:(len(struct[i]))]) > 0 and len(struct[i]) > 0) or (len(struct[i]) == 0 and prev_type == 1 and sum(typelist[(len(struct[i])):(len(struct[i+1]))]) > 0): 
                final_typelist.append(1) 
                prev_type = 1
            else: 
                final_typelist.append(0) 
                prev_type = 0
            typelist = typelist[len(struct[i]):]
        return final_typelist
    else:
        return typelist

def findpairedopen(struct: list, pos: int):
    '''
    Finds the corresponding ( for a ) in a structure, given a position.
    Parameters:
    Struct (list): The given structure
    Pos (integer): The position within the structure
    '''
    count = 1
    for i in range(pos):
        if struct[pos-i-1] == "(":
            count -= 1
        elif struct[pos-i-1] == ")":
            count += 1
        if count == 0:
            return pos - i - 1

def findmultipositions(struct: list):
    '''
    Finds all positions of "("s in multiloops and returns a list of lists where each sublist corresponds to one singluar multiloop.
    Parameters:
    Struct (list): The given structure
    '''
    depth = 0
    fulllist = []
    active_multis = {}
    for i, char in enumerate(struct):
        prev = struct[i-2] if i > 1 else None
        if char == "(":
            depth += 1
            if prev == ")":
                if depth not in active_multis:
                    active_multis[depth]=[i]
                else:
                    active_multis[depth].append(i)
        elif char == ")":
            if depth in active_multis:
                fulllist.append(active_multis[depth])
                active_multis.pop(depth)
            depth -= 1
    if depth != 0:
        raise ValueError("Unbalanced template")
    for multiloop in fulllist:
        multiloop.append(findpairedopen(struct, multiloop[0]-1))
        multiloop.sort()
    return fulllist
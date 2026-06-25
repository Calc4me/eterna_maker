struct = input("")

# Validation

# Other chars
if len(struct.translate((str.maketrans("", "", ".()")))) > 0:
    raise TypeError("Not a vaild RNA secondary structure (PKs are not supported yet)")

# Balace check
lcount = 0
for ch in struct:
    if ch == "(":
        lcount += 1
    elif ch == ")":
        lcount -= 1
    if lcount < 0:  # more ')' than '(' at some point
        raise TypeError("Not a valid RNA secondary structure (Unbalanced)")
# After loop, must return to zero
if lcount != 0:
    raise TypeError("Not a valid RNA secondary structure (Unbalanced)")

# Loop check
if struct.count("(..)") > 0 or struct.count("(.)") > 0 or struct.count("()"):
    raise TypeError("Not a vaild RNA secondary structure (Hairpin loop too small)")

lrglplowerbound = 6

trilpcount = struct.count("(...)")
lrglpcount = struct.count("".join(["." for x in range(lrglplowerbound)]))


print(f'{trilpcount}, {lrglpcount}')
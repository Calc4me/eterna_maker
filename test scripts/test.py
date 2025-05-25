#----- Testing ground -----#


string = "..((..)...)"
string = list(string)

# Find the matching opening '(' for the last ')'
currval = len(string) - 1         # Start from the last character 
count = 0                         # Tracks how deep we are in unmatched ')'
match = None                      # Will store the matching '(' index

while currval >= 0:
    currval -= 1
    char = string[currval]

    if char == ")":
        count += 1
    elif char == "(":
        if count == 0:
            # This '(' is not closing any ')'
            continue
        count -= 1
        if count == 0:
            match = currval
            break

# Print result
if match is not None:
    print("Matching '(' index:", match)
else:
    print("No matching '(' found.")

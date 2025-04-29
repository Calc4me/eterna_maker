'''
EteRNA Random Structure Generator
Author: Calc4me

Randomly generates valid RNA secondary structures using dot-bracket notation.
'''

import random

# ----- CONFIGURABLE PARAMETERS -----
lengthmin = 10              # Target minimum length (structure can be slightly longer)
base_weights = {            # Base probabilities for picking '.', '(' and ')'
    ".": 0.3,
    "(": 0.35,
    ")": 0.25
}
weight_adjust = 0.4          # Bias to favor repeating last character
stem_continue_boost = 1.8    # Extra encouragement to continue stems
stop_prob = 0.5              # Chance of early stopping once minimum length is reached
open_discourage = 0.2        # Penalty for adding '(' when too many are already open
hairpin_weight = 0.7         # Discourage closing ')' immediately after '.' for bigger hairpins
# -----------------------------------

# Runtime variables
seq = []                     # List for the final structure
unpaired_stack = []          # List for tracking indices of unmatched '('
currlen = 0                  # Counter for the number of unpaired dots '.' since last '('
last_char = None             # Track last added character (to adjust weights)

# Main loop
for i in range(lengthmin * 2):
    # Start each iteration with base weights
    weights = base_weights.copy()

    # Adjust weights based on the last character
    if last_char == ".":
        weights["."] += weight_adjust            # Encourage dot after dot
    elif last_char == "(":
        weights["("] += weight_adjust + stem_continue_boost  # Encourage stacking '('
    elif last_char == ")":
        weights[")"] += weight_adjust + stem_continue_boost  # Encourage stacking ')'

    # Restrictions based on current structure:
    if not unpaired_stack:
        # If no open '(' available, cannot close ')'
        weights[")"] = 0
    
    # If last '(' is too close (<3 dots), disable closing ')'    
    elif len(seq) - unpaired_stack[-1] - 1 < 3:
        weights[")"] = 0

    # Discourage adding more '(' if there are too many unclosed '('
    if len(unpaired_stack) > 5:
        weights["("] *= open_discourage

    # Discourage closing immediately after a '.' to prevent small (3-4 nt) hairpins
    if seq and seq[-1] == ".":
        weights[")"] *= hairpin_weight

    # Normalize weights so they add up to 1
    total = sum(weights.values())
    for key in weights:
        weights[key] /= total

    # Pick a character based on weighted random choice
    choices = [".", "(", ")"]
    char = random.choices(choices, weights=[weights[c] for c in choices])[0]

    # Update structure based on chosen character
    if char == ".":
        currlen += 1
        seq.append(".")
    elif char == "(":
        seq.append("(")
        unpaired_stack.append(len(seq) - 1)       # Track position of new '('
    elif char == ")":
        seq.append(")")
        unpaired_stack.pop()                      # Match with previous '('

    last_char = char

    # Natural stopping condition:
    # If minimum dots achieved, and no unpaired '(' left, allow early stop
    if not unpaired_stack and currlen >= lengthmin and random.random() < stop_prob:
        break

# After main loop, if any unpaired '(' remain, close them properly
while unpaired_stack:
    last_open = unpaired_stack.pop()
    dist = len(seq) - last_open - 1
    # Force at least 3 dots inside any closing
    while dist < random.randint(3,5):
        seq.append(".")
        dist += 1
    seq.append(")")

# Final output
print("Final sequence:")
print("".join(seq))

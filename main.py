'''
EteRNA Random Structure Generator
Author: Calc4me

Randomly generates valid RNA secondary structures using random chance and parameters specified by the user.
'''

import random

# ----- CONFIGURABLE PARAMETERS -----
lengthmin = 20                                   # Target minimum length (structure can be slightly longer)
base_weights = {".": 0.35, "(": 0.35, ")": 0.40} # Base probabilities for picking '.', '(' and ')' 
weight_adjust = 0.75                             # Bias to favor repeating last character.
stem_continue_boost = 1.25                       # Extra encouragement to continue stems. 
stop_prob = 0.95                                 # Chance of early stopping once minimum length is reached.
open_discourage = 0.35                           # Penalty for adding '(' when too many are already open.
hairpin_weight = 0.50                            # Discourage closing ')' immediately after '.' for bigger hairpins.
trailing_dot_chance = 0.6                        # Chance to add '.'s at end.
end_internal_loop_chance = 0.18                  # Chance to insert dots before a final ')'.
end_weights = [0.4, 0.4, 0.2]                    # Weights for 1, 2, or 3 '.'s at closing step.
trailing = True                                  # Add trailing '.'s or not.
internal_loop_bias = 7                           # Boost to close ')' when enough dots after matching '('
multiloop_force = False                          # Force a multiloop in the sequence generated.
# -----------------------------------

# ----- DEBUG AREA -----
debug_errors = False                             # Print full error messages.
full_debug = False                               # A more detailed look at what's going on under the hood.
# ----------------------

# Remove duplicate consecutive chars
def shorten_str(strin, char):
    strin = list(strin)
    i = 0
    while i < len(strin) - 1:
        if strin[i] == char and strin[i + 1] == char:
            strin.pop(i + 1)
        else:
            i += 1
    return ''.join(strin)

# Find matching "(" for a given position
def findmatch(string, currval):
    stri = list(string)
    count = 0
    match = None
    while currval >= 0:
        currval -= 1
        char = stri[currval]
        if char == ")":
            count += 1
        elif char == "(":
            if count == 0:
                continue
            count -= 1
            if count == 0:
                match = currval
                break
    return match if match is not None else -1

# Main generator
def generate_rna_structure(
    lengthmin,
    base_weights,
    weight_adjust,
    stem_continue_boost,
    stop_prob,
    open_discourage,
    hairpin_weight,
    trailing_dot_chance,
    end_internal_loop_chance,
    end_weights,
    trailing,
    internal_loop_bias
):
    seq = []
    unpaired_stack = []
    currlen = 0
    last_char = None
    multiloop_open_val = None

    # Generation loop
    for _ in range(lengthmin*2):
        weights = base_weights.copy()

        # Boost based on last char
        if last_char == ".":
            weights["."] += weight_adjust
        elif last_char == "(":
            weights["("] += weight_adjust + stem_continue_boost
        elif last_char == ")":
            weights[")"] += weight_adjust + stem_continue_boost
            weights["("] *= 2

        # Restrict closing if no opens
        if not unpaired_stack:
            weights[")"] = 0
        elif len(seq) - unpaired_stack[-1] - 1 < 3:
            weights[")"] = 0

        # Discourage excess open brackets
        if len(unpaired_stack) > 5:
            weights["("] *= open_discourage

        # Encourage bigger hairpins
        if seq and seq[-1] == ".":
            weights[")"] *= hairpin_weight

        # Discourage isolated pairs
        if seq and len(seq) > 2 and seq[-2:] == ".(":
            weights["."] *= 0.2

        # Multiloop bias
        if seq and unpaired_stack and multiloop_open_val == unpaired_stack[-1]:
            weights["."] *= 1.5
            weights["("] *= 2

        # Internal loop bias
        if unpaired_stack:
            match_index = findmatch("".join(seq), len(seq))
            if match_index != -1:
                dot_count = 0
                for j in range(match_index + 1, len(seq)):
                    if seq[j] == ".":
                        dot_count += 1
                    else:
                        break
                if dot_count >= 2:
                    weights[")"] *= internal_loop_bias

        # Debug
        if full_debug == True and last_char: print(f'Length: {len(seq)}\nLast char: {last_char}')
        if full_debug == True and weights: print({k: round(v, 2) for k, v in weights.items()})

        # Normalize
        total = sum(weights.values())
        for key in weights:
            weights[key] /= total
        
        # Debug
        if full_debug == True and weights: print({k: round(v, 2) for k, v in weights.items()})

        # Choose char
        char = random.choices([".", "(", ")"], weights=[weights[c] for c in [".", "(", ")"]])[0]

        if char == ".":
            currlen += 1
            seq.append(".")
        elif char == "(":
            if seq and random.random() > 0.5 and seq[-1] == ")":
                seq.append(".")
            seq.append("(")
            unpaired_stack.append(len(seq) - 1)
            multiloop_open_val = unpaired_stack[-1]
        elif char == ")":
            seq.append(")")
            if unpaired_stack:
                unpaired_stack.pop()

        last_char = char

        # Debug
        if full_debug == True: print(f'Unapaired: {unpaired_stack}')
        if full_debug == True: print(f'Char: {char}\n')

        # Ending condition
        if not unpaired_stack and currlen >= lengthmin and random.random() < stop_prob:
            if full_debug == True: print("ENDING NOW")
            break

    # Close remaining opens
    while unpaired_stack:
        last_open = unpaired_stack.pop()
        dist = len(seq) - last_open - 1
        min_loop = random.randint(4, 7)
        while dist < min_loop:
            seq.append(".")
            dist += 1

        # Internal loop bias at closure
        dot_count_after_open = 0
        match_index = findmatch("".join(seq), len(seq))
        if match_index != -1:
            for j in range(match_index + 1, len(seq)):
                if seq[j] == ".":
                    dot_count_after_open += 1
                else:
                    break

        insert_chance = end_internal_loop_chance
        if dot_count_after_open >= 1:
            insert_chance *= 2.5

        if random.random() < insert_chance:
            dots_to_insert = random.choices([1, 2, 3], weights=end_weights)[0]
            seq.extend(["."] * dots_to_insert)

        seq.append(")")

    if random.random() < trailing_dot_chance and trailing:
        extra_dots = random.randint(1, 6)
        seq.extend(["."] * extra_dots)

    return "".join(seq)

# Run once or until multiloop
result = ""
if multiloop_force:
    while ")).((" not in shorten_str(result, "."):
        if not debug_errors:
            try:
                result = generate_rna_structure(
                    lengthmin, base_weights, weight_adjust, stem_continue_boost, 
                    stop_prob, open_discourage, hairpin_weight,
                    trailing_dot_chance, end_internal_loop_chance, end_weights, trailing,
                    internal_loop_bias
                )
                print(f'Result:\n{result}\nlength: {len(result)}\n')
            except:
                print("Oops, an error occured :(")
        else:
            result = generate_rna_structure(
                lengthmin, base_weights, weight_adjust, stem_continue_boost, 
                stop_prob, open_discourage, hairpin_weight,
                trailing_dot_chance, end_internal_loop_chance, end_weights, trailing,
                internal_loop_bias
            )
            print(f'Result:\n{result}\nlength: {len(result)}\n')
else:
    result = generate_rna_structure(
        lengthmin, base_weights, weight_adjust, stem_continue_boost, 
        stop_prob, open_discourage, hairpin_weight,
        trailing_dot_chance, end_internal_loop_chance, end_weights, trailing,
        internal_loop_bias
    )
    print(f'Result:\n{result}\nlength: {len(result)}\n')

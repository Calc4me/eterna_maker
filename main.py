'''
EteRNA Random Structure Generator
Author: Calc4me

Randomly generates valid RNA secondary structures using dot-bracket notation.
'''

import random

# ----- CONFIGURABLE PARAMETERS -----
lengthmin = 24                                   # Target minimum length (structure can be slightly longer)
base_weights = {".": 0.35, "(": 0.35, ")": 0.31} # Base probabilities for picking '.', '(' and ')' 
weight_adjust = 0.45                             # Bias to favor repeating last character.
stem_continue_boost = 0.95                       # Extra encouragement to continue stems. 
stop_prob = 0.3                                  # Chance of early stopping once minimum length is reached.
open_discourage = 0.35                           # Penalty for adding '(' when too many are already open.
hairpin_weight = 0.50                            # Discourage closing ')' immediately after '.' for bigger hairpins.
trailing_dot_chance = 0.6                        # Chance to add '.'s at end.
end_internal_loop_chance = 0.10                  # Chance to insert dots before a final ')'.
end_weights = [0.4, 0.4, 0.2]                    # Weights for 1 or 2 '.'s at closing step.
trailing = True                                  # Add trailing '.'s or not.
internal_loop_bias = 7                           # Boost to close ')' when enough dots after matching '('
multiloop_force = True                           # Force a multiloop in the sequence generated.
# -----------------------------------

# ----- DEBUG AREA -----
debug_errors = False                             # Print full error messages. Note: breaks multiloop_force.
full_debug = False                               # Will be added soon!
# ----------------------

def shorten_str(strin, char):
    if not isinstance(strin, str) or not isinstance(char, str) or len(char) != 1:
        raise ValueError("Inputs must be a string and a single character")

    strin = list(strin)
    i = 0
    while i < len(strin) - 1:
        if strin[i] == char and strin[i + 1] == char:
            strin.pop(i + 1)
        else:
            i += 1
    return ''.join(strin)

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

    for _ in range(lengthmin):
        weights = base_weights.copy()

        if last_char == ".":
            weights["."] += weight_adjust * 0.75
        elif last_char == "(":
            weights["("] += weight_adjust + stem_continue_boost
        elif last_char == ")":
            weights[")"] += weight_adjust + stem_continue_boost * 0.85
            weights["("] *= 2

        if not unpaired_stack:
            weights[")"] = 0
        elif len(seq) - unpaired_stack[-1] - 1 < 3:
            weights[")"] = 0

        if len(unpaired_stack) > 5:
            weights["("] *= open_discourage

        if seq and seq[-1] == ".":
            weights[")"] *= hairpin_weight

        if seq and len(seq) > 2 and seq[-2:] == ".(":
            weights["."] *= 0.2
        
        if seq and unpaired_stack and multiloop_open_val == unpaired_stack[len(unpaired_stack)-1]:
            weights["."] *= 1.5
            weights["("] *= 2

        # ✅ Bias toward closing if enough dots after matching '('
        if unpaired_stack:
            match_index = unpaired_stack[-1]
            dot_count = 0
            for j in range(match_index + 1, len(seq)):
                if seq[j] == ".":
                    dot_count += 1
                else:
                    break
            if dot_count >= 3:
                weights["("] *= internal_loop_bias

        total = sum(weights.values())
        for key in weights:
            weights[key] /= total

        char = random.choices([".", "(", ")"], weights=[weights[c] for c in [".", "(", ")"]])[0]

        if char == ".":
            currlen += 1
            seq.append(".")
        elif char == "(":
            if random.random() > 0.5 and seq[-1] == ")":
                seq.append(".")
            seq.append("(")
            unpaired_stack.append(len(seq) - 1)
            multiloop_open_val = unpaired_stack[-1]
        elif char == ")":
            seq.append(")")
            if unpaired_stack:
                unpaired_stack.pop()

        last_char = char

        if not unpaired_stack and currlen >= lengthmin and random.random() < stop_prob:
            break

        # --- Close any remaining open pairs ---
    while unpaired_stack:
        last_open = unpaired_stack.pop()
        dist = len(seq) - last_open - 1

        # Ensure minimum loop length
        min_loop = random.randint(4, 7)
        while dist < min_loop:
            seq.append(".")
            dist += 1

        # 🧠 Check for dots after the matching '(' to bias toward internal loops
        dot_count_after_open = 0
        for j in range(last_open + 1, len(seq)):
            if seq[j] == ".":
                dot_count_after_open += 1
            else:
                break

        # 🎯 Increase dot insertion chance if unpaired bases exist after '('
        insert_chance = end_internal_loop_chance
        if dot_count_after_open >= 1:
            insert_chance *= 2.5  # boost chance if unpaired region already present

        if random.random() < insert_chance:
            dots_to_insert = random.choices([1, 2, 3], weights=end_weights)[0]
            seq.extend(["."] * dots_to_insert)

        seq.append(")")


    # --- Optional trailing unpaired dots ---
    if random.random() < trailing_dot_chance and trailing:
        extra_dots = random.randint(1, 10)
        seq.extend(["."] * extra_dots)

    return "".join(seq)


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


result = ""
if multiloop_force == True:
    while ")).((" not in shorten_str(result, "."):
        if debug_errors == False:
            try:
                result = generate_rna_structure(
                    lengthmin, base_weights, weight_adjust, stem_continue_boost, 
                    stop_prob, open_discourage, hairpin_weight,
                    trailing_dot_chance, end_internal_loop_chance, end_weights, trailing,
                    internal_loop_bias
                )
                print(f'Result:\n{result}\nlength: {len(list(result))}')
                print("")
            except:
                print("Oops, an error occured :(")
        else:
            result = generate_rna_structure(
                    lengthmin, base_weights, weight_adjust, stem_continue_boost, 
                    stop_prob, open_discourage, hairpin_weight,
                    trailing_dot_chance, end_internal_loop_chance, end_weights, trailing,
                    internal_loop_bias
                )
            print(f'Result:\n{result}\nlength: {len(list(result))}')
            print("")
'''
EteRNA Random Structure Generator
Author: Calc4me

Randomly generates valid RNA secondary structures using dot-bracket notation.
'''

import random

# ----- CONFIGURABLE PARAMETERS -----
lengthmin = 100             # Target minimum length (structure can be slightly longer)
base_weights = {            # Base probabilities for picking '.', '(' and ')'
    ".": 0.25,
    "(": 0.4,
    ")": 0.3
}
weight_adjust = 0.3          # Bias to favor repeating last character
stem_continue_boost = 2.3    # Extra encouragement to continue stems
stop_prob = 0.6              # Chance of early stopping once minimum length is reached
open_discourage = 0.6        # Penalty for adding '(' when too many are already open
hairpin_weight = 0.7         # Discourage closing ')' immediately after '.' for bigger hairpins
internal_loop_bias=0.15,     # Bias to add more internal loops
trailing_dot_chance=0.25,    # Chance to add '.'s at end
end_internal_loop_chance=0.05# Chance to insert dots before a final ')'
# -----------------------------------

def generate_rna_structure(
    lengthmin=100,
    base_weights={".": 0.25, "(": 0.4, ")": 0.3},
    weight_adjust=0.3,
    stem_continue_boost=2.4,
    stop_prob=0.6,
    open_discourage=0.3,
    hairpin_weight=0.6,
    internal_loop_bias=0.1,
    trailing_dot_chance=0.3,
    end_internal_loop_chance=0.05  # Chance to insert dots before a final ')'
):
    """
    Generate a biologically plausible dot-bracket RNA secondary structure.

    Parameters:
        lengthmin (int): Minimum desired length of the sequence
        base_weights (dict): Base probabilities for '.', '(', ')'
        weight_adjust (float): Extra chance to repeat previous character
        stem_continue_boost (float): Bias to continue a stem
        stop_prob (float): Chance to stop early after minimum length is reached
        open_discourage (float): Penalty for adding '(' when too many are unclosed
        hairpin_weight (float): Penalty for closing ')' right after '.'
        internal_loop_bias (float): Chance to allow '.)' for 1x1 internal loops
        trailing_dot_chance (float): Probability to add unpaired dots at the end
        end_internal_loop_chance (float): Chance to insert '.' or '..' before closing unmatched '('
    
    Returns:
        str: Dot-bracket notation RNA structure
    """

    seq = []               # The sequence being constructed
    unpaired_stack = []    # Indices of unmatched '('
    currlen = 0            # Count of unpaired dots added so far
    last_char = None       # Track previous character

    # --- Main sequence generation loop ---
    for _ in range(lengthmin * 2):
        weights = base_weights.copy()

        # Bias for repeating the last character
        if last_char == ".":
            weights["."] += weight_adjust
        elif last_char == "(":
            weights["("] += weight_adjust + stem_continue_boost
        elif last_char == ")":
            weights[")"] += weight_adjust + stem_continue_boost

        # Prevent unmatched ')' if no '(' open
        if not unpaired_stack:
            weights[")"] = 0
        # Prevent closing too early (hairpin needs ≥3 bases)
        elif len(seq) - unpaired_stack[-1] - 1 < 3:
            weights[")"] = 0

        # Discourage opening more if too many unclosed '('
        if len(unpaired_stack) > 5:
            weights["("] *= open_discourage

        # Discourage closing after a dot (avoid tiny hairpins)
        if seq and seq[-1] == ".":
            weights[")"] *= hairpin_weight

        # Normalize weights
        total = sum(weights.values())
        for key in weights:
            weights[key] /= total

        # Randomly pick next character
        char = random.choices([".", "(", ")"], weights=[weights[c] for c in [".", "(", ")"]])[0]

        if char == ".":
            currlen += 1
            seq.append(".")
        elif char == "(":
            seq.append("(")
            unpaired_stack.append(len(seq) - 1)
        elif char == ")":
            seq.append(")")
            if unpaired_stack:
                unpaired_stack.pop()

        last_char = char

        # Early stopping if conditions are met
        if not unpaired_stack and currlen >= lengthmin and random.random() < stop_prob:
            break

    # --- Post-processing: close unpaired '(' properly ---
    while unpaired_stack:
        last_open = unpaired_stack.pop()
        dist = len(seq) - last_open - 1

        # Ensure ≥3 unpaired between '(' and ')'
        min_loop = random.randint(3, 5)
        while dist < min_loop:
            seq.append(".")
            dist += 1

        # Chance to insert internal loop-like closure (e.g. '..)')
        if random.random() < end_internal_loop_chance:
            dots_to_insert = random.choice([1, 1, 1, 2, 2])
            seq.extend(["."] * dots_to_insert)
        
        seq.append(")")

    # --- Optional: add trailing unpaired bases ---
    if random.random() < trailing_dot_chance:
        extra_dots = random.randint(1, 5)
        seq.extend(["."] * extra_dots)

    return "".join(seq)

print(generate_rna_structure(
    lengthmin, base_weights, weight_adjust, stem_continue_boost, 
    stop_prob, open_discourage, hairpin_weight, internal_loop_bias,
    trailing_dot_chance, end_internal_loop_chance))
## Parameters explanation

Here's a explanation for each parameter :)

#### lengthmin (Int)

Target minimum length (structure can be slightly longer than 2x)  
Higher -> Longer, Lower -> Shorter

#### base_weights (Dict)

Base probabilities for picking '.', '(' and ')'  
Higher -> More likely, Lower -> Less likely

#### weight_adjust (Float)

Bias to favor repeating last character.  
Higher -> Less variety, Lower -> More variety

#### stem_continue_boost (Float)

Extra encouragement to continue stems.  
Higher -> More long stems, Lower -> Smaller stems

#### stop_prob (Float)

Chance of early stopping once minimum length is reached.  
Higher -> More likely to stop, Lower -> Less likely to stop

#### open_discourage (Float)

Penalty for adding '(' when too many are already open.  
Higher -> More open '(' at a time, Lower -> Less open '(' at a time

#### hairpin_weight (Float)

Discourage closing ')' immediately after '.' for bigger hairpins.  
Higher -> bigger hairpins, Lower -> Smaller harpins

#### trailing_dot_chance (Float)

Chance to add '.'s at end.  
Higher -> more likely to add trailing dots, Lower -> Less likely

#### end_internal_loop_chance (Float)

Chance to insert dots before a final ')'.  
Higher -> Higher chance to add .) or ..), Lower -> less likely

#### end_weights (List)

Weights for 1 or 2 '.'s at closing step.  
Higher -> More likely, Lower -> Less likely

#### trailing (Bool)

Add trailing '.'s or no.  
Higher -> More likely, Lower -> Less likely

#### internal_loop_bias (Float)

Bias towards internal loops
Higher -> More likely, Lower -> Less likely

#### multiloop_force (Bool)

Whether to force the final solution to have a multiloop or not.
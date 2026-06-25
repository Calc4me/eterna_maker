# Setting Presets
This is just a few presets to help you finetune your code to what you want. More will be added soon!

The most important setting to get right is the weights, weight_adjust, and stem_continue_boost, which can help larger structures be more solvable but make smaller structures more bland.

It takes a while to figure out settings you like, so play around with them for a while! It also normally takes me a while to get to settings I like, especially after logic changes and other updates. :)

#### Newer Settings

- Standard settings (Good place to start)
    - lengthmin = 30
    - base_weights = {".": 0.35, "(": 0.35, ")": 0.31}
    - weight_adjust = 0.5
    - stem_continue_boost = 1.2
    - stop_prob = 0.3
    - open_discourage = 0.35
    - hairpin_weight = 0.50
    - trailing_dot_chance = 0.6
    - end_internal_loop_chance = 0.10
    - end_weights = [0.4, 0.4, 0.2]
    - trailing = True
    - internal_loop_bias = 7
    - multiloop_force = False

- Small and complicated
    - lengthmin = 20
    - base_weights = {".": 0.35, "(": 0.35, ")": 0.40}
    - weight_adjust = 0.75
    - stem_continue_boost = 1.25
    - stop_prob = 0.95
    - open_discourage = 0.35
    - hairpin_weight = 0.50
    - trailing_dot_chance = 0.6
    - end_internal_loop_chance = 0.18
    - end_weights = [0.4, 0.4, 0.2]
    - trailing = True
    - internal_loop_bias = 7
    - multiloop_force = False

- Small multiloops (What I used for Partiality 3)
    - lengthmin = 22
    - base_weights = {".": 0.35, "(": 0.35, ")": 0.31}
    - weight_adjust = 0.45
    - stem_continue_boost = 0.95
    - stop_prob = 0.3
    - open_discourage = 0.35
    - hairpin_weight = 0.50
    - trailing_dot_chance = 0.6
    - end_internal_loop_chance = 0.10
    - end_weights = [0.4, 0.4, 0.2]
    - trailing = True
    - internal_loop_bias = 7
    - multiloop_force = True

#### Older Settings

- ~Gen 7 (Not really recommended)
    - lengthmin = 15
    - base_weights = {".": 0.30, "(": 0.35, ")": 0.4}
    - weight_adjust = 0.6
    - stem_continue_boost = 1.8
    - stop_prob = 0.5
    - open_discourage = 0.55
    - hairpin_weight = 0.50
    - trailing_dot_chance = 0.4
    - end_internal_loop_chance = 0.10
    - end_weights = [0.4, 0.4, 0.2]
    - trailing = True
    - internal_loop_bias = 7
    - multiloop_force = False

- ~Gen 3-6 (Not recommended)
    - lengthmin = 8
    - base_weights = {".": 0.35, "(": 0.33, ")": 0.31}
    - weight_adjust = 0.45
    - stem_continue_boost = 1.0
    - stop_prob = 0.6
    - open_discourage = 0.35
    - hairpin_weight = 0.50
    - trailing_dot_chance = 0.6
    - end_internal_loop_chance = 0.10
    - end_weights = [0.4, 0.4, 0.2]
    - trailing = True
    - internal_loop_bias = 7
    - multiloop_force = False
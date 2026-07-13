# Parameter datatypes and explanations
## Template Generation
- tempchances -> Float list
  - [Chance for ( if ( before, chance for ( if ) before] during template generation
- temprange -> Integer list
  - Minimum [0]/2 stacks, maximum [1]/2 stacks in the template
- bias -> Float 
  - Bias towards closing (subtracts from tempchances[0])
- rerollchance -> Float
  - Chance to continue after a valid template is generated
- user_template -> Balanced Template List
  - Template runtime variable, set to your template if using your own, set to [] if not using premade
  - Needs to be balanced and have *s for hairpins


## Template Length Assignment
- assigntype -> Integer
  - 0 -> Normally distributed, 1 -> Uniformly distributed, 2 -> User-made probabilites
- mean -> Float / Integer
   - Mean of stack lengths (option 0)
- stdev -> Float / Integer 
  - Standard deviation of stack lengths (option 0)
- lengthrange -> Integer list
  - Range of stack lengths (option 1+2)
- probabilities -> Float list (normalized)
  - Individual stack length probabilities from lengthrange[0] to lengthrange[1] (option 2)
- min_stack_size -> Integer
  - Minimum size of a stack

## Loop making
- looprange -> Integer list
  - [Min internal loop size, max internal loop size]

## Stack Generation
- dotratio -> Float
  - Ratio of dots to paired bases before removal of adjacent unpaired bases
- maxcountdiff -> Integer
  - Max difference between unpaired base counts on each side of the generated stack that allows for random unpaired base removal
- maxposdiff -> Integer
  - Max difference between the position of two unpaired bases to warrant removal of one between sides of a stack
- maxonesideposdiff -> Integer
  - Max differece between the position of two unpaired bases to warrant removal of one on the same side of a stack
- onechance -> Float
  - Chance for "." as the inserted unpaired base
- twochance -> Float
  - Same as above, but "..". The remaining chance between the two is the chance that "..." is inserted.
- minloopdots -> Integer
  - Minimum unpaired bases in a hairpin
- maxloopdots -> Integer
  - Maximum unpaired bases in a hairpin

## Pseudoknots
- pseudoknots -> Boolean
  - Enables pseudoknot generation.
- numpseudoknots -> Integer
  - Number of pseudoknots to add
- pkassigntype -> Integer
  - The same as assigntype in Template Length Assignment but for pseudoknot stems
- pkmean -> Float / Integer 
  - The same as mean in Template Length Assignment but for pseudoknot stems
- pkstdev -> Float / Integer 
  - The same as stdev in Template Length Assignment but for pseudoknot stems
- pklengthrange -> Integer list
  - The same as lengthrange in Template Length Assignment but for pseudoknot stems
- pkprobabilities -> Float list (normalized)
  - The same as probabilities in Template Length Assignment but for pseudoknot stems
- pkminsize -> Integer
  - Minimum size of a pseudoknot
- surroundrange -> List
  - Range of bases that can surround a pseudoknot
- hairpinmaxdiff -> Integer
  - Maximum difference between two hairpin locations for a pseudoknot to be generated
- maxpksfromhairpin -> Integer
  - Maximum pseduoknots from a hairpin loop, between 1 and 2 works best
- maxpkgenatt -> Integer
  - Maximum number of tries the pseduoknot generation algorithm tries to generate valid hairpin pairs, to avoid an infinite loop
- crossedmultiloops -> Boolean
  - Whether to force all multiloops to be crossed (have at least one stem be involved in a pseduoknot)

## Runtime variables (don't touch)
- generationContinueFlag -> Boolean
- tempContinueFlag -> Boolean
- stopFlag -> Boolean
- pkcontinueflag -> Boolean
- looplist -> Empty List
- stack -> Empty List
- pairslist -> Empty List
- pseudoknotpairs -> Empty List
- crossedmultis -> Integer (0)
- nummultis -> Integer (0)

## Other
- debug -> Boolean
  - Print more stuff to help with debugging
- visualize_template -> Boolean
  - Visualize the template structure, with stacks as two base pairs, internal loops as 1 pair of unpaired bases, and hairpins as tetraloops.
- visualize_structure -> Boolean
  - Visualize the RNA structure. **Does** work with psuedoknots. (close the window to continue)
- template_stats -> Boolean
  - Set to True to show full stats about the generated template
- full_stats -> Boolean
  - Set to True to show full stats about the given structure
- export_file -> Filepath
  - Insert the file export location here. To disable file export, set to "".
- write_or_append -> String ("a" or "w")
  - "a" appends to the end of the export file, "w" overwrites previous contents
- seed -> Integer
  - To generate the same sequence every time, set to a certain seed instead of None

# Stat Explanations
## Template
- Length
  - Number of paired stacks (one stack counts as 2)
- Hairpins
  - Number of hairpins ("*"s)
- Stacks
  - Number of stacks (half of length)
- Multiloops
  - Number of multiloops

## Full Structure
- Length
  - Number of bases, paired and unpaired
- Base Pairs
  - Number of pairs of paired bases
- Unpaired bases
  - Number of unpaired bases
- Average Stack Length
  - Average length of a stack **i.e. average distance between internal loops**
- Smallest and Largest stack
  - Smallest and largest length of a stack **i.e. smallest and largest distance between internal loops**
- Hairpins
  - Number of hairpin loops (excludes cases like (((.[[...))))
- Largest Hairpin
  - Largest hairpin, set to 0 if all hairpins have pseudoknots
- Internal Loops
  - Number of internal loops in the structure
- Bulges
  - Number of bulges in the structure
- Pseudoknots
  - Number of pseudoknkots in the structure
- Pseudoknot Density
  - Proportion of the structure that is pseudoknots
- Pair density
  - Proportion of the structure that is base pairs (includes pseudoknots)
- Proportion Invloved in Pseudoknots
  - The proportion of bases that are "contained" within a pseudoknot in dot-bracket notation, such as the bold here:
  ((((..**[[[[[[.))))((((..]]]]]]**.))))
- Multiloops
  - Number of multiloops in the structure
- Proportion of Crossed Multiloops
  - Proportion of multiloops that have at least one stack that is involved in a pseudoknot

# Parameters and Other Things
## Good Starting Parameters
```
tempchances = [0.85, 0.4]
temprange = [4,12]
bias = 0.025
reroll_chance = 0.25
user_template = []

assigntype = 0
mean = 6
stdev = 2
lengthrange = [3,10]
probabilities = [0.05, 0.05, 0.1, 0.3, 0.3, 0.1, 0.05, 0.05]
min_stack_size = 2

looprange = [1,2]

dotratio = 0.23
maxcountdiff = 2
maxposdiff = 1
maxonesideposdiff = 1
onechance = 0.6
twochance = 0.35
minloopdots = 3
maxloopdots = 6

pseudoknots = False
numpseudoknots = 2
pkassigntype = 0
pkmean = 6
pkstdev = 1
pklengthrange = [3,10]
pkprobabilities = [0.05, 0.05, 0.1, 0.3, 0.3, 0.1, 0.05, 0.05]
pkminsize = 2
surroundrange = [1,2]
hairpinmaxdiff = 1

debug = False,
visualize_template = True
visualize_structure = True
template_stats = True
full_stats = True
export_file = "structure_export.txt"
write_or_append = "a"
seed = None
```
## [PK 240 Lab](https://eternagame.org/labs/14333719)
```
tempchances = [0.85, 0.45]
temprange = [18,22]
bias = 0.025
reroll_chance = 0.25
user_template = []

assigntype = 0
mean = 8.5
stdev = 2 
lengthrange = [3,10]
probabilities = [0.05, 0.05, 0.1, 0.3, 0.3, 0.1, 0.05, 0.05]
min_stack_size = 2

looprange = [3,5]

dotratio = 0.05
maxcountdiff = 2
maxposdiff = 1
maxonesideposdiff = 1
onechance = 0.6
twochance = 0.35
minloopdots = 4
maxloopdots = 5

pseudoknots = True
numpseudoknots = 4
pkassigntype = 0
pkmean = 9 
pkstdev = 1.5 
pklengthrange = [3,10]
pkprobabilities = [0.05, 0.05, 0.1, 0.3, 0.3, 0.1, 0.05, 0.05]
pkminsize = 2
surroundrange = [1,2]
hairpinmaxdiff = 1
maxpksfromhairpin = 2
maxpkgenatt = 1000
crossedmultiloops = True

debug = False
visualize_template = True
visualize_structure = True
template_stats = True
full_stats = True
export_file = "structure_export.txt"
write_or_append = "a"
seed = None
```
## Good Starting Templates
```
["(", "(", "(", "(", "*", ")", ")", "(", "*", ")", ")", ")"]
["(", "(", "(", "*", ")", ")", "(", "*", ")", ")"]
["(", "(", "*", ")", ")", "(", "*", ")"]
["(", "(", "*", ")", "(", "*", ")", ")"]
```
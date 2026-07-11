# Parameter datatypes
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
  - 0 = Normally distributed, 1 = Uniformly distributed, 2 = User-made probabilites
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

## Runtime variables (don't touch)
- generationContinueFlag -> Boolean
- looplist -> Empty List
- stack -> Empty List
- pairslist -> Empty List
- tempContinueFlag -> Boolean
- stopFlag -> Boolean

## Other
- debug -> Boolean
  - Print more stuff to help with debugging
- visualize_structure -> Boolean
  - Visualize the RNA structure (close the window to continue)
- seed -> Integer
  - To generate the same sequence every time, set to a certain seed instead of None
- export_file -> Filepath
  - Insert the file export location here. To disable file export, set to "".
- full_stats -> Boolean
  - Set to True to show full stats about the given structure
- write_or_append -> String ("a" or "w")
  - "a" appends to the end of the export file, "w" overwrites previous contents
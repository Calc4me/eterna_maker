# Parameter datatypes
## Template Generation
- tempchances -> Float list
- temprange -> Integer list
- bias -> Float
- rerollchance -> Float
- user_template -> Balanced Template List


## Template Length Assignment
- assigntype -> Integer
- mean -> Float / Integer
- stdev -> Float / Integer 
- lengthrange -> Integer list
- probabilities -> Float list (normalized)
- min_stack_size -> Integer

## Loop making
- looprange -> Integer list

## Stack Generation
- dotratio -> Float
- maxcountdiff -> Integer
- maxposdiff -> Integer
- maxonesideposdiff -> Integer
- onechance -> Float
- twochance -> Float
- minloopdots -> Integer
- maxloopdots -> Integer

## Runtime variables (don't touch)
- generationContinueFlag -> Boolean
- looplist -> Empty List
- stack -> Empty List
- pairslist -> Empty List
- tempContinueFlag -> Boolean
- stopFlag -> Boolean

## Other
- debug -> Boolean
- visualize_structure -> Boolean
- seed -> Integer
- export_file -> Filepath
- full_stats -> Boolean
- write_or_append -> String ("a" or "w")
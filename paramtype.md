# Parameter datatypes
## Template Generation
- tempchances -> Float list
- temprange -> Integer list
- bias -> Float
- rerollchance -> Float
- user_template -> List


## Template Length Assignment
- assigntype -> Integer
- mean -> Integer
- stdev -> Float / Integer 
- lengthrange -> Integer list
- probabilities -> Float list (normalized)

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
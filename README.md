# EteRNA Structre Generator!

The **second** (yay!) iteration program designed by [Calc4me](https://eternagame.org/players/460832) to randomly generate valid secondary structures for [EteRNA](https://eternagame.org/) puzzles.

If you have a change that will improve this, you can either fork this and make the change yourself, or message me on EteRNA, and I'll see what I can do. Any suggestions are very much welcome, and any issues you find can be reported in the issues on GitHub.

If you are looking for the older model, see the folder labeled "old vers". All the old files are kept there but will not be maintained.
For an explanation of the new model, see introduction.md, and for paramater types, see paramtype.md.

More updates coming soon!

## Current Generations:

- Gen 1
  - First generation, simple and very rigid.
  - Generated very messy seqences because of ) spam.
- Gen 2
  - Second generation, improved on Gen 1.
  - More customizable, but still was messy over 30 nt.
- Gen 3
  - Third generation, improved on Gen 2 w/ new logic.
  - Mainly cleaned up generation and made it more stable in the 20-40 nt range.
- Gen 4
  - Fourth generation, overhauled Gen 3.
  - Improved customization and cleaned up generation to 50-60 nts (with well-tuned paramaters)
- Gen 5
  - Fifth generation, improved on Gen 4.
  - More customization and both cleaned up generation massively, to the point where 200 nts are good.
- Gen 6
  - Sixth generation, cleaned up Gen 5.
  - Added more explanation, and cleaned up code, and added more comments and better logic.
- Gen 7
  - Seventh generation, cleaned up Gen 6.
  - Added internal loops and a few other minor improvements
- Gen 8
  - Eighth gen, improved Gen 7.
  - More variance (has gone down, less internal loops, etc.), presets, multiloop forcing, and small changes.
- Gen 8 v2
  - Add more comments for readability
  - Cleaned up the code and fixed some logic errors, and added full_debug
- Gen v2 1
  - Redid everything from the ground up using a more natural algorithm that gives more natural control over the output.
  - Added a more user-friendly UI
- Gen v2 1.1
  - Added structure visualization and "neighbor removal"
  - Fixed spelling
- Gen v2 1.2
  - Fixed major bugs in the code
  - Cleaned it up and added a slightly better UI and more stats
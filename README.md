# MC Recipe Randomizer
This tool can randomize either the outputs, the ingredients, or both, for every recipe there is in the game, including crafting, smelting, stonecutting, etc.\
Based upon the [MCRecipeScrambler](https://gitlab.com/UltraWelfare/mcrecipescrambler/) by George Tsomlektsis.

### Requirements
- Git.
- Python3 (Tested on 3.7.3, should practically work with any 3.x version newer than 3.5).
### Usage
- Clone the repo `git clone https://github.com/DVD8084/mcreciperandomizer.git`.
- Create a folder in the root of the script named `recipes`.
- Place all the vanilla JSON files for the recipes inside that folder.
- Run the script `python [...]_randomizer.py name.zip`.
- Put zip file that is generated into a folder named `datapacks` inside your world folder.
#### Blacklist
- Recipe blacklist needs a filename (without the extension) per line.  
Input and Output blacklists need an item ID (or tag, for inputs) per line.  
- If you don't want a blacklist, leave the file empty.
#### Notes
- When playing with these randomized recipes, be sure to unlock the recipe book from the start. It may prove to be rather useful.  
- `ultimate_randomizer.py` generates two different recipes per file to increase the amount of items you can get.
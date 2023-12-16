# AI-Climbing
# Overview of repository
images:
- contains images that were used for testing, not important for user
pytorch:
- used for training, not important for user
runs:
- images that were used for training/testing purposes

src:
- Contains files that were used for training model and solving route

In order to run our code, you can use the hold_finder.py and route_setter.py scripts in src. You can run the hold_finder script to preview what the wall looks
like, and observe where the start holds are. This script is run by inputting the hsv and r values for color, and the image file name. Next, you can run the 
route setter script, which actually sets the route. This script can be run by passing in the list of holds from the previous script, the index of two start holds
in the list, and your height.



## How to use
Fork this repository, and 

### Color to HSV, Range
- Red: 0 20 30 10 
- Yellow: 60 20 30 40 
- Green: 120 10 20 40 
- Blue: 210 10 30 30 
- Purple: 270 5 5 508
- Pink: 320 40 50 40 
- Black: 0 0 0 0 
- White: 0 0 100 0 

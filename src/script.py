
import argparse
import get_holds
import shutil 
from get_holds import getHoldsArray
import importlib
importlib.reload(get_holds)


def main(file, color):
#     - Red: 0 20 30 10 
# - Yellow: 60 20 30 40 
# - Green: 120 10 20 40 
# - Blue: 210 10 30 30 
# - Purple: 270 5 5 50
# - Pink: 320 40 50 40 
# - Black: 0 0 0 0 
# - White: 0 0 100 0 
    hsv = []
    r = 0
    if color.lower() == 'red':
        hsv = [0, 20, 30]
        r = 10
    elif color.lower() == 'yellow':
        hsv = [60, 20, 30]
        r = 40
    elif color.lower() == 'green':   
        hsv = [120, 10, 20]
        r = 40
    elif color.lower() == 'blue':
        hsv = [210, 10, 30]
        r = 30
    elif color.lower() == 'purple':
        hsv = [270, 5, 5]
        r = 50
    elif color.lower() == 'pink':
        hsv = [320, 40, 50]
        r = 40
    elif color.lower() == 'black':
        hsv = [0, 0, 0]
        r = 0
    elif color.lower() == 'white':
        hsv = [0, 0, 100]
        r = 0
    else:
        'please enter a different color'
        return
  
    # Source path 
    source = file
    
    # Destination path 
    destination = '../images/traverse.jpg'
    
    # Move the content of 
    # source to destination 
    dest = shutil.move(source, destination, copy_function = shutil.copytree) 
  

    holds = getHoldsArray(dest, hsv, r)

    holds.sort()
    print(holds)
    print(len(holds))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f',
        '--file',
        help='image file name',
        required=True,
        type=str
    )
    parser.add_argument(
        '-c',
        '--color',
        help='Color of rock to indentify',
        required=True,
        type=str
    )
    args = parser.parse_args()

    file = str(args.file)
    color = str(args.color)
    main(file, color)

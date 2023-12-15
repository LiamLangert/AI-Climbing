import argparse
import get_holds
import shutil 
from get_holds import getHoldsArray
import importlib
importlib.reload(get_holds)
import RouteFinder
from RouteFinder import uniformCostSearch, Limb, State, Person, Route, moveToText, LimbName 


def main(file, h, s, v, r):

    source = file
    
    # Destination path 
    destination = '../images/'
    dest = shutil.move(source, destination, copy_function = shutil.copytree) 
    hsv = [h, s, v]
    holds = []
    try: 
        holds = getHoldsArray(dest, hsv, r)

    except:
        print('invalid color')
        holds = getHoldsArray(dest, [], r)
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
        '-h',
        '--h',
        help='h value',
        required=True,
        type=int
    )
    parser.add_argument(
        '-s',
        '--s',
        help='s value',
        required=True,
        type=int
    )

    parser.add_argument(
        '-v',
        '--v',
        help='v value',
        required=True,
        type=int
    )
    parser.add_argument(
        '-r',
        '--r',
        help='r value',
        required=True,
        type=int
    )

    args = parser.parse_args()
    file = str(args.file)
    h = int(args.h)
    s = int(args.s)
    v = int(args.v)
    r = int(args.r)
    main(file, h, s, v, r)

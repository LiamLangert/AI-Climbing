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

    i1 = int(input("enter index of first start hold"))
    i2 = int(input("enter index of second start hold"))

    route = Route(holds = holds, start1 = holds[i1], start2 = holds[i2], finish = holds[0])
    lh = Limb(LimbName.LEFT_HAND, 2.5, 8, route.start_hold1)
    rh = Limb(LimbName.RIGHT_HAND, 2.5, 8, route.start_hold2)
    lf = Limb(LimbName.LEFT_LEG, 8, 5, route.holds[-1])
    rf = Limb(LimbName.RIGHT_LEG, 8, 5, route.holds[-1])
    height = int(input('how tall are you (in inches)'))
    human = Person(height)

    state1 = State(lf, rf, lh, rh, human, route)
    rf = RouteFinder(state=state1)
    results1 = rf.uniformCostSearch()

    for action in results1:
        print(moveToText(action, route))

    print(len(holds))
    for i in range(len(holds)):
        print(f"{i}: {holds[i].x}, {holds[i].y}, {holds[i].diff}")

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

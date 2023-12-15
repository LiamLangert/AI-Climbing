import argparse
import get_holds
import shutil 
from get_holds import getHoldsArray
import importlib
importlib.reload(get_holds)
import RouteFinder
from RouteFinder import uniformCostSearch, Limb, State, Person, Route, moveToText, LimbName 

def main(holds, i1, i2, height):

    route = Route(holds = holds, start1 = holds[i1], start2 = holds[i2], finish = holds[0])
    lh = Limb(LimbName.LEFT_HAND, 2.5, 8, route.start_hold1)
    rh = Limb(LimbName.RIGHT_HAND, 2.5, 8, route.start_hold2)
    lf = Limb(LimbName.LEFT_LEG, 8, 5, route.holds[-1])
    rf = Limb(LimbName.RIGHT_LEG, 8, 5, route.holds[-1])
    human = Person(height)

    state1 = State(lf, rf, lh, rh, human, route)
    a_srftar1 = RouteFinder(state=state1)
    results1 = rf.uniformCostSearch()

    for action in results1:
        print(moveToText(action, route))

    print(len(holds))
    for i in range(len(holds)):
        print(f"{i}: {holds[i].x}, {holds[i].y}, {holds[i].diff}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('holds', metavar='N', type=Hold, nargs='*',
                    help='a list of strings')
    parser.add_argument(
        '-o',
        '--index1',
        help='start hold 1 index',
        required=True,
        type=str
    )

    parser.add_argument(
        '-t',
        '--index2',
        help='start hold 2 index',
        required=True,
        type=int
    )
    parser.add_argument(
        '-h',
        '--height',
        help='height',
        required=True,
        type=int
    )
    args = parser.parse_args()

    holds = str(args.holds)
    i1 = int(args.index1)
    i2 = int(args.index2)
    height = int(args.height)
    main(holds, i1, i2, height)

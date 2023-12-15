import hold_finder, diff_angle
from hold_finder import predictHolds, getBoxAsImage, getHoldsNearColor, dispResults, removeEdges
from diff_angle import predictDiff, getResults, getIdealRotation
import importlib
importlib.reload(diff_angle)
importlib.reload(hold_finder)
import numpy as np
import sys

class Hold:
    def __init__(self, x: int, y: int, diff: float, width: float, height: float, angle: int):
        #Coords = top left corner
        self.x = x
        self.y = y
        self.diff = diff
        self.width = width
        self.height = height
        self.angle = angle
    def getCenter(self):
        return (self.coords[0] + self.width/2, self.coords[1] + self.height/2)
    def __eq__(self, other):
        if other == None:
            return False
        return self.x == other.x and self.y == other.y
    def __gt__(self, other):
        return self.y > other.y
    def __lt__(self, other):
        return self.y < other.y
    def __ge__(self, other):
        return self.y >= other.y
    def __le__(self, other):
        return self.y <= other.y
    
    def __repr__(self):
        return (f"""Hold: Top left at {self.x}, {self.y}
                Width = {self.width}, Height = {self.height}
                Difficulty = {round(self.diff, 2)}/10, Angle = {self.angle} degrees\n""")
    
def getHoldsArray(path, color, close):
    results = predictHolds(path)
    results = removeEdges(results)
    results = getHoldsNearColor(results, color, close)
    
    dispResults(results)
    for r in results:
        holds = []
        boxes_data = np.array(r.boxes.xywh)
        for i in range(len(boxes_data)):
            hold = getBoxAsImage(results, i)
            angle, diff = getIdealRotation(hold)
            if diff != "tag" and diff != "bolt" and diff != "downclimb":
                holds.append(Hold(x=boxes_data[i][0], y=boxes_data[i][1], width=boxes_data[i][2], height=boxes_data[i][3], diff=float(diff), angle=int(angle)))
            else:
                print(f"FOUND {diff} at {boxes_data[i][0]}, {boxes_data[i][1]}")
    return holds

def main(argv):
    print(getHoldsArray(argv[0], np.array([int(argv[1]), int(argv[2]), int(argv[3])]), int(argv[4])))
    return 0

if __name__ == "__main__":
   main(sys.argv[1:])
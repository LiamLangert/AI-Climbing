import hold_finder, diff_angle
from hold_finder import predictHolds, getBoxAsImage, getHoldsNearColor, dispResults, removeEdges
from diff_angle import predictDiff, getResults, getIdealRotation
import numpy as np
import sys

class Hold:
    def __init__(self, coords, width, height, diff, angle):
        #Coords = top left corner
        self.coords = coords
        self.diff = diff
        self.width = width
        self.height = height
        self.angle = angle
    
    def __repr__(self):
        return (f"""Hold: Top left at {self.coords[0]}, {self.coords[1]}
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
                holds.append(Hold((boxes_data[i][0], boxes_data[i][1]), boxes_data[i][2], boxes_data[i][3], float(diff), int(angle)))
    return holds

def main(argv):
    print(getHoldsArray(argv[0], np.array([int(argv[1]), int(argv[2]), int(argv[3])]), int(argv[4])))
    return 0

if __name__ == "__main__":
   main(sys.argv[1:])
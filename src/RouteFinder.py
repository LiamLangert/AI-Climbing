import heapq, random
import math
from copy import copy
from enum import Enum
from PIL import Image


class PriorityQueue:
    """
    Implements a priority queue data structure. Each inserted item
    has a priority associated with it and the client is usually interested
    in quick retrieval of the lowest-priority item in the queue. This
    data structure allows O(1) access to the lowest-priority item.
    """

    def __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)


class Person:
    def __init__(self, height: int) -> None:
        """
        Represents a person class to get their
        height: height in inches rounded to nearest whole number
        """
        self.height = height
        self.wingspan = height * 1.06
        self.reach = height * 1.35
        self.leg_length = height * 0.5


class Hold:
    """
    Represents a hold in the route
    Has an x,y coordinate, a difficulty rating obtained from the model, a width and height, and an angle obtained from another model.
    """

    def __init__(
        self, x: int, y: int, diff: float, width: float, height: float, angle: int
    ):
        # Coords = middle of the bounding box
        self.x = x
        self.y = y
        self.diff = diff
        self.width = width
        self.height = height
        self.angle = angle

    def get_top_left(self):
        return (self.coords[0] - self.width / 2, self.coords[1] - self.height / 2)

    def __eq__(self, other):
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
        return f"""Hold: Top left at {self.x}, {self.y}
                Width = {self.width}, Height = {self.height}
                Difficulty = {round(self.diff, 2)}/10, Angle = {self.angle} degrees\n"""


from enum import Enum


class LimbName(Enum):
    """
    Class for limb names
    """

    LEFT_HAND = "Left Hand"
    RIGHT_HAND = "Right Hand"
    LEFT_LEG = "Left Leg"
    RIGHT_LEG = "Right Leg"


class Limb:
    def __init__(self, name: LimbName, strength: int, flexibility: int, hold: Hold):
        self.name, self.strength, self.flexibility, self.hold = (
            name,
            strength,
            flexibility,
            hold,
        )

    def __repr__(self):
        return f"{self.name} at {self.hold}"


class Route:
    def __init__(self, holds: Hold, start1: Hold, start2: Hold, finish: Hold):
        self.holds = holds
        self.start_hold1 = start1
        self.start_hold2 = start2
        self.finish_hold = finish


class ImageAttributes:
    def __init__(self, path):
        self.path = path
        img = Image.open(path)
        self.width = img.width
        self.height = img.height


class State:
    def __init__(
        self,
        lf: Limb,
        rf: Limb,
        lh: Limb,
        rh: Limb,
        person: Person,
        route: Route,
        image_attributes: ImageAttributes,
    ):
        self.lf, self.rf, self.lh, self.rh = lf, rf, lh, rh
        self.person = person
        self.moves = []
        self.costs = []
        self.route = route
        self.wall_height_inches = (
            180  # Represents real height of wall <- need to measure
        )
        self.image_attributes = image_attributes
        self.wall_height_pixels = (
            self.image_attributes.height
        )  # placeholder <- Need to extract from image

    # Not sure where to put this
    def inches_to_pixels(self, inches: int):
        return (self.wall_height_pixels / self.wall_height_inches) * inches

    def __eq__(self, other):
        return (
            self.lf.hold == other.lf.hold
            and self.rf.hold == other.rf.hold
            and self.rh.hold == other.rh.hold
            and self.lh.hold == other.lh.hold
        ) or (
            self.lf.hold == other.rf.hold
            and self.rf.hold == other.lf.hold
            and self.rh.hold == other.lh.hold
            and self.lh.hold == other.rh.hold
        )

    def __repr__(self):
        return f"{self.moves}"

    def get_successors(self):
        succs = []
        limbs = [self.lf, self.rf, self.lh, self.rh]
        for i in range(len(limbs)):
            neighs = self.get_neighbors(limbs[i])
            for neigh in neighs:
                # print("Hi neighbor")
                new_state = copy(self)
                if i == 0:
                    new_state.lf = Limb(LimbName.LEFT_LEG, 2.5, 8, neigh)
                    action = (self.lf, neigh)
                if i == 1:
                    new_state.rf = Limb(LimbName.RIGHT_LEG, 2.5, 8, neigh)
                    action = (self.rf, neigh)
                if i == 2:
                    new_state.lh = Limb(LimbName.LEFT_HAND, 8, 2, neigh)
                    action = (self.lh, neigh)
                if i == 3:
                    new_state.rh = Limb(LimbName.RIGHT_HAND, 8, 2, neigh)
                    action = (self.rh, neigh)
                succs.append((new_state, action))
        # print(succs)
        return succs

    def get_neighbors(self, limb):
        neighbors = []
        for hold in self.route.holds:
            if not hold == limb.hold:
                if limb.name in [LimbName.LEFT_LEG, LimbName.RIGHT_LEG]:
                    # print("Checking leg neighbors")
                    # print(f"Height diff: {abs(hold.y - limb.hold.y)}")
                    # print(f"Leg length: {self.inches_to_pixels(self.person.leg_length)}")
                    # low_arm is max because pixels go from top to bottom
                    low_arm = max([self.lh.hold.y, self.rh.hold.y])
                    if (
                        0
                        < limb.hold.y - hold.y
                        < self.inches_to_pixels(self.person.leg_length)
                        and abs(hold.x - limb.hold.x)
                        < self.inches_to_pixels(self.person.leg_length)
                        and hold.y > low_arm
                    ):
                        neighbors.append(hold)
                elif limb.name in [LimbName.LEFT_HAND, LimbName.RIGHT_HAND]:
                    # print("Checking arm neighbors")
                    # print("HAND TIME 1")
                    upper_leg, lower_leg = sorted([self.lf.hold.y, self.rf.hold.y])
                    if (
                        abs(hold.x - limb.hold.x)
                        < self.inches_to_pixels(self.person.wingspan)
                        and lower_leg - hold.y
                        < self.inches_to_pixels(self.person.height * 0.8)
                        and hold.y < upper_leg
                        and 0 < limb.hold.y - hold.y
                    ):
                        neighbors.append(hold)
        return neighbors


def state_difficulty(state: State):
    """
    Finds the difficulty of a certain state
    state: the state that is being evaluated for difficulty
    """
    if state.lh.hold != None and state.rh.hold != None:
        average_hands_x = (state.lh.hold.x + state.rh.hold.x) / 2
        average_hands_y = (state.lh.hold.y + state.rh.hold.y) / 2
    else:
        if state.rh.hold == None:
            average_hands_x = state.lh.hold.x
            average_hands_y = state.lh.hold.y
        else:
            average_hands_y = state.rh.hold.y
            average_hands_x = state.rh.hold.x
    if state.lf.hold != None and state.rf.hold != None:
        average_legs_x = (state.lf.hold.x + state.rf.hold.x) / 2
        average_legs_y = (state.lf.hold.y + state.rf.hold.y) / 2
    else:
        if state.rf.hold == None:
            average_legs_x = state.lf.hold.x
            average_legs_y = state.lf.hold.y
        else:
            average_legs_y = state.rf.hold.y
            average_legs_x = state.rf.hold.x

    hands_difference_x = (
        abs(state.rh.hold.x - state.lh.hold.x)
        if state.lh.hold != None and state.rh.hold != None
        else 0
    )
    hands_difference_y = (
        abs(state.rh.hold.y - state.lh.hold.y)
        if state.lh.hold != None and state.rh.hold != None
        else 0
    )

    legs_difference_x = (
        abs(state.rf.hold.x - state.lf.hold.x)
        if state.lf.hold != None and state.rf.hold != None
        else 0
    )
    legs_difference_y = (
        abs(state.lf.hold.y - state.rf.hold.y)
        if state.lf.hold != None and state.rf.hold != None
        else 0
    )
    hands_difference_raw_x = (
        state.rh.hold.x - state.lh.hold.x
        if state.lh.hold != None and state.rh.hold != None
        else 0
    )
    legs_difference_raw_x = (
        state.rf.hold.x - state.lf.hold.x
        if state.lf.hold != None and state.rf.hold != None
        else 0
    )

    leg_match_diff = 0
    if (
        state.lf.hold != None
        and state.rf.hold != None
        and state.lf.hold.x - state.rf.hold.x == 0
    ):
        leg_match_diff = 25

    cross_diff = 0
    if hands_difference_raw_x < 0:
        cross_diff += 2 * abs(hands_difference_raw_x / 88)
    if legs_difference_raw_x < 0:
        cross_diff += 100
    if hands_difference_raw_x < 0 and legs_difference_raw_x < 0:
        cross_diff *= 3

    diff = 0
    center_diff = abs(average_hands_x - average_legs_x) ** 2

    target_distance = state.inches_to_pixels(state.person.height * 0.95)
    distance_diff = target_distance - abs(average_legs_y - average_hands_y)
    scrunched_up_diff = distance_diff**2

    limb_strength_diff = 0
    angle_diff = 0

    # Check each limb and find the strength ratio for the holds
    for limb in [state.lh, state.rh, state.lf, state.rf]:
        if limb.hold != None:
            limb_strength_diff += limb.hold.diff / limb.strength
            if limb.name == LimbName.LEFT_HAND:
                if 315 >= limb.hold.angle >= 270:
                    angle_diff += 2
                elif 90 >= limb.hold.angle or limb.hold.angle > 315:
                    angle_diff += 1
                elif 180 >= limb.hold.angle > 90:
                    angle_diff += 2.5
                else:
                    angle_diff += 3
            if limb.name == LimbName.RIGHT_HAND:
                if 90 >= limb.hold.angle >= 45:
                    angle_diff += 2
                elif 45 >= limb.hold.angle or limb.hold.angle > 270:
                    angle_diff += 1
                elif 270 >= limb.hold.angle > 180:
                    angle_diff += 2.5
                else:
                    angle_diff += 3
            if limb.name in [LimbName.LEFT_LEG, LimbName.RIGHT_LEG]:
                if 90 <= limb.hold.angle <= 270:
                    angle_diff += 2
        else:
            limb_strength_diff += 6
    separation_diff = 0
    separation_diff += 0.1 * hands_difference_y
    separation_diff += 0.1 * legs_difference_y

    # If separated too far, make it harder
    if hands_difference_x > state.inches_to_pixels(0.8 * state.person.wingspan):
        separation_diff += 0.5 * hands_difference_x
    separation_diff += 0.5 * legs_difference_y
    if legs_difference_x > state.inches_to_pixels(0.6 * state.person.wingspan):
        separation_diff += 0.5 * legs_difference_x

    # Weight all of the different difficulties to balance them out
    center_diff *= 0.04
    scrunched_up_diff *= 0.05
    angle_diff *= 1
    limb_strength_diff *= 30
    separation_diff *= 0.5
    cross_diff *= 1
    leg_match_diff *= 20
    diff += (
        center_diff
        + scrunched_up_diff
        + angle_diff
        + limb_strength_diff
        + separation_diff
        + leg_match_diff
        + cross_diff
    )
    # print(f"center = {center_diff}, scaled = {scrunched_up_diff}, angle = {angle_diff}, strength = {limb_strength_diff}, cross = {cross_diff}")
    return diff


def move_difficulty(state: State, limb: Limb, next_hold: Hold):
    """
    Evaluates the difficulty of a move
    state: the state that is being evaluated
    """
    distance = math.sqrt(
        ((limb.hold.x - next_hold.x) ** 2) + ((limb.hold.y - next_hold.y) ** 2)
    )
    distance_diff = distance

    new_state = State(
        copy(state.lf),
        copy(state.rf),
        copy(state.lh),
        copy(state.rh),
        state.person,
        state.route,
        state.wall_height_pixels,
    )
    new_state_limbs = [new_state.lh, new_state.rh, new_state.lf, new_state.rf]
    for new_state_limb in new_state_limbs:
        if new_state_limb.name == limb.name:
            new_state_limb.hold = None
    state_without_limb_difficulty = 0.3 * state_difficulty(new_state)
    distance_diff *= 0.1
    move_diff = distance_diff + state_without_limb_difficulty
    # print( distance_diff)
    return move_diff


class RouteFinder:
    """
    Class to find the route of a wall
    Takes in a state and gets the person's reach from that
    """

    WALL_HEIGHT = 180

    def __init__(self, state):
        self.state = state
        self.reach = state.person.reach

    def get_cost_value(self, costs):
        """
        Helper function used to square the costs in the list of costs
        """
        return sum([cost for cost in costs]) + 250 * len(costs)

    def uniform_cost_search(self):
        """
        Search function to find the best route
        """
        explored = []
        frontier = PriorityQueue()
        num = 0
        frontier.push(self.state, 0)
        while not frontier.isEmpty():
            cur_state = frontier.pop()
            explored.append(cur_state)
            if (
                cur_state.lh.hold == self.state.route.finish_hold
                and cur_state.rh.hold == self.state.route.finish_hold
            ):
                # What every good rock climber says at the top
                print("TAAAAAAAAAAAAAAKE")
                print(cur_state.costs)
                print(self.get_cost_value(cur_state.costs))
                return cur_state.moves
            for next_state, action in cur_state.getStateSuccessors():
                if next_state not in explored:
                    num += 1
                    if num % 500 == 0:
                        print(
                            f"Checking state #{num} with move length {len(cur_state.moves)}"
                        )
                    next_state.costs = copy(cur_state.costs)
                    next_state.costs.append(
                        state_difficulty(next_state)
                        + move_difficulty(cur_state, action[0], action[1])
                    )
                    next_state.moves = copy(cur_state.moves)
                    next_state.moves.append(action)
                    if next_state in [tup[2] for tup in frontier.heap]:
                        frontier.update(
                            next_state, self.get_cost_value(next_state.costs)
                        )
                    else:
                        frontier.push(next_state, self.get_cost_value(next_state.costs))
        return []

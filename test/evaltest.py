import math
import unittest

class Person:
    def __init__(self, height: int) -> None:
        """
        height: height in inches rounded to nearest whole number
        """
        self.height = height
        self.wingspan = height * 1.06
        self.reach = height * 1.35

class Hold:
    def __init__(self, coords, dif, width, height, orientation):
        #Coords = top left corner
        self.coords = coords
        self.dif = dif
        self.width = width
        self.height = height
        self.orientation = orientation
    def getCenter(self):
        return (self.coords[0] + self.width/2, self.coords[1] + self.height/2)

class Limb:
    def __init__(self, name: str, strength: float, flexibility: float, hold: Hold) -> None:
        self.name, self.strength, self.flexibility, self.hold = name, strength, flexibility, hold

class State:
    def __init__(self, lf: Limb, rf: Limb, lh: Limb, rh: Limb, person: Person):
        self.lf, self.rf, self.lh, self.rh, self.person = lf, rf, lh, rh, person
        self.wall_height_inches = 180 # Represents real height of wall <- need to measure
        self.wall_height_pixels = 1920 #placeholder <- Need to extract from image

    # Not sure where to put this
    def inches_to_pixels(self, inches: float) -> float:
        return (self.wall_height_pixels / self.wall_height_inches) * inches
    
    def move_difficulty(self, limb: str, next_hold: Hold) -> float:

        """
        limb is a limb that makes the move
        next_hold is the hold the limb is going to
        Returns a number from 1-10 for the difficulty of the move
        """
        move_diff = 0

        distance = math.sqrt(((limb.hold.x - next_hold.x) ** 2) + ((limb.hold.y - next_hold.y) ** 2))
        return move_diff

    def state_difficulty(self) -> float:
        """
        Returns a number 1-10 for the difficulty of the state
        """
        diff = 0
        average_hands_x = (self.lf.x + self.rf.x) / 2
        average_legs_x = (self.lh.x + self.rh.x) / 2
        average_hands_y = (self.lf.y + self.rf.y) / 2
        average_legs_y = (self.lh.y + self.rh.y) / 2

        hands_difference_x = abs(self.lh.x - self.rh.x)
        hands_difference_y = abs(self.lh.y - self.rh.y)

        legs_difference_x = abs(self.lf.x - self.rf.x)
        legs_difference_y = abs(self.lf.y - self.rf.y)

        # Add this to diff
        center_diff = 0.5*abs(average_hands_x - average_legs_x)

        target_distance = self.inches_to_pixels(self.person.height * 0.8)
        scaling_factor = 0.1
        distance_diff = abs(average_legs_y - average_hands_y) + target_distance

        raw_difficulty_score = (scaling_factor * (distance_diff ** 2))

        # Add this to diff. Scales the difficulty score linearly between 1 and 10
        scaled_difficulty_score = 1 + 9 * ((raw_difficulty_score) / (1 + scaling_factor * target_distance ** 2))

        # Add this to diff
        limb_strength_diff = 0
        # Add this to diff
        orientation_diff = 0
        for limb in [self.lh, self.rh, self.lf, self.rf]:
            limb_strength_diff += limb.hold.diff / limb.strength
            if limb.name == 'left hand':
                if 315 >= limb.hold.orientation >= 270:
                    orientation_diff += 2
                elif 90 >= limb.hold.orientation or limb.hold.orientation > 315:
                    orientation_diff += 1
                elif 270 > limb.hold.orientation >= 180:
                    orientation_diff += 2.5
                else:
                    diff += 3
            if limb.name == 'right hand':
                if 90 >= limb.hold.orientation >= 45:
                    orientation_diff += 2
                elif 45 > limb.hold.orientation or limb.hold.orientation >= 270:
                    orientation_diff += 1
                elif 180 >= limb.hold.orientation > 90:
                    orientation_diff += 2.5
                else:
                    diff += 3
            if limb.name in ['left leg', 'right leg']:
                if 270 >= limb.hold.orientation >= 180:
                    orientation_diff += 1.5

        if hands_difference_y > self.inches_to_pixels(self.person.wingspan * 0.7): 
            diff += 0.5 * hands_difference_y 
        if hands_difference_x > self.inches_to_pixels(self.person.wingspan * 0.8):
            diff += 0.5 * hands_difference_x
        if legs_difference_y > self.inches_to_pixels(self.person.height * .2):
            diff += 0.5 * legs_difference_y
        if legs_difference_x > self.inches_to_pixels(self.person.wingspan * 0.7):
            diff += 0.5 * legs_difference_x
        diff += center_diff + scaled_difficulty_score + orientation_diff + limb_strength_diff
        return diff

class Test(unittest.TestCase):
    Rowan = Person(67)
    Rachel = Person(66)
    Liam = Person(68)
    def test_person_attributes(self, person: Person):
        self.assertEqual(person.height, person.height)
        self.assertEqual(person.reach, person.height * 1.35)
        self.assertEqual(person.wingspan, person.height * 1.06)

    def test_state_difficulty(self):
        holdlh = Hold(coords=())
        holdrh
        holdlf
        holdrf

        lh
        rh
        lf
        rf

        Liam = Person(68)
        state1 = State(person=Liam, lh=lh, )
        self.assertEquals(state1.state_difficulty, 10)




if __name__ == '__main__':
    Rowan = Person(67)
    unittest.main(Rowan)
# Contains functions and classes that compute motion equations and give positions of two objects
import math


class GravityObject:

    def __init__(self, pos, velo, mass):
        self.position = pos
        self.velocity = velo
        self.mass = mass

'''
class GravitySituation:
    
    def __init__(self, pos1, pos2, mass1, mass2, velo1, velo2, distance):
        self.object1 = GravityObject(pos1, velo1, mass1)
        self.object2 = GravityObject(pos2, velo2, mass2)
        self.r = distance
'''


def compute_distance(pos_x1, pos_y1, pos_x2, pos_y2):
    return math.sqrt((pos_x1 - pos_x2) ** 2 + (pos_y1 - pos_y2) ** 2)
'''
def do_all(male_t):
    policz nowa predkosc => v = male_t * G * 
    policz nowe polozenie
    zaktualizuj wartosci

'''
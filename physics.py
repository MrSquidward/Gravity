# Contains functions and classes that compute motion equations and give positions of two objects
import math


class GravityObject:

    def __init__(self, pos, velo, mass):
        self.position = pos
        self.velocity = velo
        self.mass = mass


def compute_distance(pos_x1, pos_y1, pos_x2, pos_y2):
    return math.sqrt((pos_x1 - pos_x2) ** 2 + (pos_y1 - pos_y2) ** 2)


def sin_value(r, obj1, obj2):
    y = obj1.pos[1] - obj2.pos[1]
    if y > 0:
        return y / r
    else:
        return ((-1) * y) / r


def cos_value(r, obj1, obj2):
    x = obj1.pos[0] - obj2.pos[0]
    if x > 0:
        return x / r
    else:
        return ((-1) * x) / r


GRAVITY_CONST = 6.674301515E-11


def compute_for_object(obj1, obj2, r, time):
    acceleration_x = (GRAVITY_CONST * obj2.mass * cos_value(r, obj1, obj2)) / (r ** 2)
    obj1.pos[0] = (acceleration_x * (time ** 2) / 2) + obj1.velocity[0] * time + obj1.pos[0]
    obj1.velocity[0] = acceleration_x * time + obj1.velocity[0]

    acceleration_y = (GRAVITY_CONST * obj2.mass * sin_value(r, obj1, obj2)) / (r ** 2)
    obj1.pos[1] = (acceleration_y * (time ** 2) / 2) + obj1.velocity[1] * time + obj1.pos[1]
    obj1.velocity[1] = acceleration_y * time + obj1.velocity[1]
    return obj1


def compute_new_param(obj1, obj2, time):
    r = compute_distance(obj1.pos[0], obj1.pos[1], obj2.pos[0], obj2.pos[1])
    obj1 = compute_for_object(obj1, obj2, r, time)
    obj2 = compute_for_object(obj2, obj1, r, time)
    objects_list = [obj1, obj2]
    return objects_list

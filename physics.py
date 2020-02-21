# Contains functions and classes that compute motion equations and give positions of two objects
import math


class GravityObject:

    def __init__(self, pos, velo, mass):
        self.position = pos
        self.velocity = velo
        self.mass = mass


def compute_distance(pos_x1, pos_y1, pos_x2, pos_y2):
    return math.sqrt((pos_x1 - pos_x2) ** 2 + (pos_y1 - pos_y2) ** 2)


def cos_value_in_y(r, obj1, obj2):
    y = obj1.position[1] - obj2.position[1]
    if y > 0:
        return y / r
    else:
        return ((-1) * y) / r


def cos_value_in_x(r, obj1, obj2):
    x = obj1.position[0] - obj2.position[0]
    if x > 0:
        return x / r
    else:
        return ((-1) * x) / r


GRAVITY_CONST = 6.674301515E-11


def compute_for_object(obj1, obj2, r, time, i):
    acceleration_x = (GRAVITY_CONST * obj2.mass * cos_value_in_x(r, obj1, obj2)) / (r ** 2)
    acceleration_x *= (-1) * i
    obj1.position[0] = (acceleration_x * (time ** 2) / 2) + obj1.velocity[0] * time + obj1.position[0]
    obj1.velocity[0] = acceleration_x * time + obj1.velocity[0]

    acceleration_y = (GRAVITY_CONST * obj2.mass * cos_value_in_y(r, obj1, obj2)) / (r ** 2)
    acceleration_y *= (-1) * i
    obj1.position[1] = (acceleration_y * (time ** 2) / 2) + obj1.velocity[1] * time + obj1.position[1]
    obj1.velocity[1] = acceleration_y * time + obj1.velocity[1]
    return obj1


def compute_center(obj1, obj2):
    cen_x = obj1.position[0] - ((obj1.position[0] - obj2.position[0]) / 2)
    cen_y = obj1.position[1] - ((obj1.position[1] - obj2.position[1]) / 2)
    return [cen_x, cen_y]


def compute_new_param(obj1, obj2, time):
    r = compute_distance(obj1.position[0], obj1.position[1], obj2.position[0], obj2.position[1])
    center_of_objects = compute_center(obj1, obj2)   
    print(center_of_objects[0])
    print(center_of_objects[1])
    if obj1.position[0] < center_of_objects[0]:
        obj1 = compute_for_object(obj1, obj2, r, time, -1)
        obj2 = compute_for_object(obj2, obj1, r, time, 1)
        print("Pierwszy warinat")
    else:
        obj1 = compute_for_object(obj1, obj2, r, time, 1)
        obj2 = compute_for_object(obj2, obj1, r, time, -1)
        print("Drugi wariant")

    objects_list = [obj1, obj2]
    return objects_list

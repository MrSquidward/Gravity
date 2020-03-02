# Contains functions and classes that compute motion equations and give new positions of two objects
# as well as calculating mass enter and geometrical center.
import math


GRAVITY_CONST = 6.674301515E-11


class GravityParameters:
    def __init__(self, list_of_objects):
        self.objects = list_of_objects
        obj1 = self.objects[0]
        obj2 = self.objects[1]
        distance = compute_distance(obj1.position[0], obj1.position[1], obj2.position[0], obj2.position[1])
        signs_obj1 = check_vector_sense(obj1.position[0], obj1.position[1], obj2.position[0], obj2.position[1])

        self.center_of_mass = compute_center_of_mass(obj1, obj2, distance, signs_obj1)
        self.geometrical_center = compute_geometrical_center(obj1, obj2)


    def update_params(self, obj1, obj2, vector_sense, distance):
        self.center_of_mass = compute_center_of_mass(obj1, obj2, distance, vector_sense)
        self.geometrical_center = compute_geometrical_center(obj1, obj2)


class GravityObject:
    def __init__(self, pos, velo, mass):
        self.position = pos
        self.velocity = velo
        self.mass = mass
        self.previous_positions = []


    def update_parameters(self, obj2, r, time, vector_sense):
        self.previous_positions.append((self.position[0], self.position[1]))

        acceleration_x = (GRAVITY_CONST * obj2.mass * cos_value_in_x(r, self.position[0], obj2.position[0])) / (r ** 2)
        acceleration_x *= -vector_sense[0]
        self.position[0] = (acceleration_x * (time ** 2) / 2) + self.velocity[0] * time + self.position[0]
        self.velocity[0] = acceleration_x * time + self.velocity[0]

        acceleration_y = (GRAVITY_CONST * obj2.mass * cos_value_in_y(r, self.position[1], obj2.position[1])) / (r ** 2)
        acceleration_y *= -vector_sense[1]
        self.position[1] = (acceleration_y * (time ** 2) / 2) + self.velocity[1] * time + self.position[1]
        self.velocity[1] = acceleration_y * time + self.velocity[1]


def compute_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def cos_value_in_y(r, y1, y2):
    y = y1 - y2
    return abs(y) / r


def cos_value_in_x(r, x1, x2):
    x = x1 - x2
    return abs(x) / r


def compute_geometrical_center(obj1, obj2):
    cen_x = obj1.position[0] - ((obj1.position[0] - obj2.position[0]) / 2)
    cen_y = obj1.position[1] - ((obj1.position[1] - obj2.position[1]) / 2)
    return cen_x, cen_y


def compute_center_of_mass(obj1, obj2, r, vector_sense):
    obj1_distance_from_mass_center = r * obj2.mass / (obj1.mass + obj2.mass)

    cen_without_shift_x = obj1_distance_from_mass_center * cos_value_in_x(r, obj1.position[0], obj2.position[0])
    cen_x = obj1.position[0] + -1 * vector_sense[0] * cen_without_shift_x

    cen_without_shift_y = obj1_distance_from_mass_center * cos_value_in_y(r, obj1.position[1], obj2.position[1])
    cen_y = obj1.position[1] + -1 * vector_sense[1] * cen_without_shift_y

    return cen_x, cen_y


def check_collision(obj1, obj2, distance):
    delta_x = abs(obj1.position[0] - obj2.position[0])
    delta_y = abs(obj1.position[1] - obj2.position[1])

    return delta_x <= distance and delta_y <= distance


def check_vector_sense(x1, y1, x2, y2):
    if x1 < x2:
        sign_x = -1
    else:
        sign_x = 1

    if y1 < y2:
        sign_y = -1
    else:
        sign_y = 1

    return sign_x, sign_y


def update_objects_positions(obj1, obj2, gravity_params, time):
    r = compute_distance(obj1.position[0], obj1.position[1], obj2.position[0], obj2.position[1])

    vector_sense_obj1 = check_vector_sense(obj1.position[0], obj1.position[1], obj2.position[0], obj2.position[1])
    vector_sense_obj2 = check_vector_sense(obj2.position[0], obj2.position[1], obj1.position[0], obj1.position[1])

    obj1.update_parameters(obj2, r, time, vector_sense_obj1)
    obj2.update_parameters(obj1, r, time, vector_sense_obj2)

    gravity_params.update_params(obj1, obj2, vector_sense_obj1, r)

def is_position_the_same(x1, y1, x2, y2, r):
    delta_x = abs(x1 - x2)
    delta_y = abs(y1 - y2)

    return delta_x <= r and delta_y <= r

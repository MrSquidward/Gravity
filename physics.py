# Contains functions and classes that compute motion equations and give new positions of two objects
# as well as calculating mass enter and geometrical center.
import math


GRAVITY_CONST = 6.674301515E-11
# how often position will be put into list of prev position (once in number below)
PREVIOUS_POSITION_PRECISION = 3


class GravityParameters:
    def __init__(self, list_of_objects):
        self.objects = list_of_objects

        self.center_of_mass = compute_center_of_mass(self.objects)
        self.geometrical_center = compute_geometrical_center(self.objects)

    def update_params(self):
        self.center_of_mass = compute_center_of_mass(self.objects)
        self.geometrical_center = compute_geometrical_center(self.objects)


class GravityObject:
    def __init__(self, pos, velo, mass):
        self.position = pos
        self.velocity = velo
        self.mass = mass
        self.previous_positions = []
        self.previous_positions_iterator = PREVIOUS_POSITION_PRECISION

    def update_parameters(self, objects, time):
        if not self.previous_positions_iterator % PREVIOUS_POSITION_PRECISION:
            self.previous_positions.append((self.position[0], self.position[1]))

        self.previous_positions_iterator += 1

        acceleration_x = acceleration_y = 0
        for obj in objects:

            if is_position_the_same(obj.position[0], obj.position[1], self.position[0], self.position[1], 0):
                continue

            r = compute_distance(self.position[0], self.position[1], obj.position[0], obj.position[1])
            vector_sense = check_vector_sense(self.position[0], self.position[1], obj.position[0], obj.position[1])

            acceleration_x += -vector_sense[0] * (GRAVITY_CONST * obj.mass *
                                                  cos_value_in_x(r, self.position[0], obj.position[0])) / (r ** 2)

            acceleration_y += -vector_sense[1] * (GRAVITY_CONST * obj.mass *
                                                  cos_value_in_y(r, self.position[1], obj.position[1])) / (r ** 2)

        self.position[0] = (acceleration_x * (time ** 2) / 2) + self.velocity[0] * time + self.position[0]
        self.velocity[0] = acceleration_x * time + self.velocity[0]

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


def compute_geometrical_center(obj_list):
    cen_x = cen_y = 0
    for obj in obj_list:
        cen_x += obj.position[0]
        cen_y += obj.position[1]

    cen_x /= len(obj_list)
    cen_y /= len(obj_list)

    return cen_x, cen_y


def compute_center_of_mass(obj_list):

    cen_x = cen_y = sum_of_mass = 0
    for obj in obj_list:
        cen_x += obj.position[0] * obj.mass
        cen_y += obj.position[1] * obj.mass
        sum_of_mass += obj.mass

    cen_x /= sum_of_mass
    cen_y /= sum_of_mass

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


def update_objects_positions(gravity_params, time):
    for obj in gravity_params.objects:
        obj.update_parameters(gravity_params.objects, time)

    gravity_params.update_params()


def is_position_the_same(x1, y1, x2, y2, r):
    delta_x = abs(x1 - x2)
    delta_y = abs(y1 - y2)

    return delta_x <= r and delta_y <= r

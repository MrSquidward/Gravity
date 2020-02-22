# Contains functions and classes that compute motion equations and give positions of two objects
import math


GRAVITY_CONST = 6.674301515E-11


class GravityObject:
    def __init__(self, pos, velo, mass):
        self.position = pos
        self.velocity = velo
        self.mass = mass
        self.list_of_previous_position = [self.position]#todo nie dziala wyswietlanie linii, ale tablica pozcyji jest ok
        self.center_of_mass = [0, 0] #todo zrobic aby to nie bylo elementem obiektu

    def update_parameters(self, obj2, r, time, signs):
        acceleration_x = (GRAVITY_CONST * obj2.mass * cos_value_in_x(r, self.position[0], obj2.position[0])) / (r ** 2)
        acceleration_x *= -signs[0]
        self.position[0] = (acceleration_x * (time ** 2) / 2) + self.velocity[0] * time + self.position[0]
        self.velocity[0] = acceleration_x * time + self.velocity[0]

        acceleration_y = (GRAVITY_CONST * obj2.mass * cos_value_in_y(r, self.position[1], obj2.position[1])) / (r ** 2)
        acceleration_y *= -signs[1]
        self.position[1] = (acceleration_y * (time ** 2) / 2) + self.velocity[1] * time + self.position[1]
        self.velocity[1] = acceleration_y * time + self.velocity[1]

        self.list_of_previous_position.append(self.position)


def compute_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def cos_value_in_y(r, y1, y2):
    y = y1 - y2
    return abs(y) / r


def cos_value_in_x(r, x1, x2):
    x = x1 - x2
    return abs(x) / r


def compute_center(obj1, obj2):
    cen_x = obj1.position[0] - ((obj1.position[0] - obj2.position[0]) / 2)
    cen_y = obj1.position[1] - ((obj1.position[1] - obj2.position[1]) / 2)
    return [cen_x, cen_y]


def compute_center_of_mass(obj1, obj2, r, signs_1):
    obj1_distance_from_mass_center = r * obj2.mass / (obj1.mass + obj2.mass)

    cen_without_shift_x = obj1_distance_from_mass_center * cos_value_in_x(r, obj1.position[0], obj2.position[0])
    cen_x = obj1.position[0] + -1 * signs_1[0] * cen_without_shift_x

    cen_without_shift_y = obj1_distance_from_mass_center * cos_value_in_y(r, obj1.position[1], obj2.position[1])
    cen_y = obj1.position[1] + -1 * signs_1[1] * cen_without_shift_y

    return cen_x, cen_y


def check_collision(obj1, obj2, distance):
    return abs(obj1.position[0] - obj2.position[0]) <= distance and abs(obj1.position[1] - obj2.position[1]) <= distance


def check_quadrants(x, y, center_x, center_y):
    if x < center_x:
        sign_x = -1
    else:
        sign_x = 1

    if y < center_y:
        sign_y = -1
    else:
        sign_y = 1

    return sign_x, sign_y


def update_objects_positions(obj1, obj2, time):
    r = compute_distance(obj1.position[0], obj1.position[1], obj2.position[0], obj2.position[1])
    middle_point = compute_center(obj1, obj2)

    signs_obj1 = check_quadrants(obj1.position[0], obj1.position[1], middle_point[0], middle_point[1])
    signs_obj2 = check_quadrants(obj2.position[0], obj2.position[1], middle_point[0], middle_point[1])

    obj1.center_of_mass = compute_center_of_mass(obj1, obj2, r, signs_obj1)

    obj1.update_parameters(obj2, r, time, signs_obj1)
    obj2.update_parameters(obj1, r, time, signs_obj2)

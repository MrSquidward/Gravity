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
    def __init__(self, pos, velocity, mass):
        self.position = pos
        self.velocity = velocity
        self.mass = mass
        self.previous_positions = []
        self.previous_positions_iterator = PREVIOUS_POSITION_PRECISION

    def update_parameters(self, objects, time):
        if not self.previous_positions_iterator % PREVIOUS_POSITION_PRECISION:
            self.previous_positions.append((self.position[0], self.position[1]))

        self.previous_positions_iterator += 1

        acceleration_x = acceleration_y = 0
        for obj in objects:

            if id(obj) == id(self):
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


def check_collision(gravity_params, distance):
    for i in range(len(gravity_params.objects)):
        for j in range(len(gravity_params.objects)):
            if id(gravity_params.objects[i]) != id(gravity_params.objects[j]):
                if is_position_the_same(gravity_params.objects[i].position[0], gravity_params.objects[i].position[1],
                                        gravity_params.objects[j].position[0], gravity_params.objects[j].position[1],
                                        distance):
                    merge_two_objects_during_collision(gravity_params, gravity_params.objects[i],
                                                       gravity_params.objects[j])
                    return


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


def is_position_the_same(x1, y1, x2, y2, r):
    delta_x = abs(x1 - x2)
    delta_y = abs(y1 - y2)

    return delta_x <= r and delta_y <= r


def compute_speed_after_collision(obj1, obj2):
    momentum_obj1 = [obj1.velocity[0] * obj1.mass, obj1.velocity[1] * obj1.mass]
    momentum_obj2 = [obj2.velocity[0] * obj2.mass, obj2.velocity[1] * obj2.mass]
    sum_of_mass = obj1.mass + obj2.mass
    return [(momentum_obj1[0] + momentum_obj2[0]) / sum_of_mass, (momentum_obj1[1] + momentum_obj2[1]) / sum_of_mass]


def merge_two_objects_during_collision(gravity_params, obj1, obj2):
    merged_position = list(compute_geometrical_center([obj1, obj2]))
    merged_velocity = compute_speed_after_collision(obj1, obj2)

    merged_obj = GravityObject(merged_position, merged_velocity, obj1.mass + obj2.mass)
    merged_obj.previous_positions.append((merged_position[0], merged_position[1]))

    gravity_params.objects.remove(obj1)
    gravity_params.objects.remove(obj2)

    gravity_params.objects.append(merged_obj)


def update_objects_positions(gravity_params, time):
    for obj in gravity_params.objects:
        obj.update_parameters(gravity_params.objects, time)

    gravity_params.update_params()


'''
todo
    wyświetlanie drogi dla obiektów które nie istanieją
    ulepszenie wyswietlania drogi
    jednostki
    zależność wielkości obiektu od masy
    zrobic cos aby nie wywalalo bledow przy zamknieciu okna ??
    read_me:
        rozdzial o gui
        dopisac troche do fizyki o centrum masy itp
'''
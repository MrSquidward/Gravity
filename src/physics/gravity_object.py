# Contains functions and classes that compute motion equations and give new positions of two objects
# as well as calculating mass enter and geometrical center.
import math
from math import atan
from src.physics.gravity_parameters import GravityParameters


GRAVITY_CONST = 6.674301515e-11
# how often position will be put into list of prev position (once in number below)
PREVIOUS_POSITION_PRECISION = 10
# size of dot (used in viewing mass and geometrical center)
OBJECT_RADIUS = 20


class GravityObject:
    def __init__(self, pos, velocity, mass):
        self.position = pos
        self.velocity = velocity
        self.mass = mass
        self.radius = OBJECT_RADIUS
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
            r = self.compute_distance(
                self.position[0], self.position[1], obj.position[0], obj.position[1]
            )
            vector_sense = GravityObject.check_vector_sense(
                self.position[0], self.position[1], obj.position[0], obj.position[1]
            )
            acceleration_x += (
                -vector_sense[0]
                * (
                    GRAVITY_CONST
                    * obj.mass
                    * GravityObject.cos_value_in_x(r, self.position[0], obj.position[0])
                )
                / (r ** 2)
            )
            acceleration_y += (
                -vector_sense[1]
                * (
                    GRAVITY_CONST
                    * obj.mass
                    * GravityObject.cos_value_in_y(r, self.position[1], obj.position[1])
                )
                / (r ** 2)
            )
        self.position[0] = (
            (acceleration_x * (time ** 2) / 2)
            + self.velocity[0] * time
            + self.position[0]
        )
        self.velocity[0] = acceleration_x * time + self.velocity[0]
        self.position[1] = (
            (acceleration_y * (time ** 2) / 2)
            + self.velocity[1] * time
            + self.position[1]
        )
        self.velocity[1] = acceleration_y * time + self.velocity[1]

    @staticmethod
    def compute_distance(x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    @staticmethod
    def cos_value_in_y(r, y1, y2):
        y = y1 - y2
        return abs(y) / r

    @staticmethod
    def cos_value_in_x(r, x1, x2):
        x = x1 - x2
        return abs(x) / r

    @staticmethod
    def compute_collision(obj1, obj2, distance):
        delta_x = abs(obj1.position[0] - obj2.position[0])
        delta_y = abs(obj1.position[1] - obj2.position[1])
        return delta_x <= distance and delta_y <= distance

    @staticmethod
    def check_collision(gravity_params, distance):
        for i in range(len(gravity_params.objects)):
            for j in range(len(gravity_params.objects)):
                if id(gravity_params.objects[i]) != id(gravity_params.objects[j]):
                    if GravityObject.is_position_the_same(
                        gravity_params.objects[i].position[0],
                        gravity_params.objects[i].position[1],
                        gravity_params.objects[j].position[0],
                        gravity_params.objects[j].position[1],
                        distance,
                    ):
                        GravityObject.merge_two_objects_during_collision(
                            gravity_params,
                            gravity_params.objects[i],
                            gravity_params.objects[j],
                        )
                        return

    @staticmethod
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

    @staticmethod
    def is_position_the_same(x1, y1, x2, y2, r):
        delta_x = abs(x1 - x2)
        delta_y = abs(y1 - y2)
        return delta_x <= r and delta_y <= r

    @staticmethod
    def compute_speed_after_collision(obj1, obj2):
        momentum_obj1 = [obj1.velocity[0] * obj1.mass, obj1.velocity[1] * obj1.mass]
        momentum_obj2 = [obj2.velocity[0] * obj2.mass, obj2.velocity[1] * obj2.mass]
        sum_of_mass = obj1.mass + obj2.mass
        if sum_of_mass == 0:
            return [
                momentum_obj1[0] + momentum_obj2[0],
                momentum_obj1[1] + momentum_obj2[1],
            ]
        else:
            return [
                (momentum_obj1[0] + momentum_obj2[0]) / sum_of_mass,
                (momentum_obj1[1] + momentum_obj2[1]) / sum_of_mass,
            ]

    @staticmethod
    def merge_two_objects_during_collision(gravity_params, obj1, obj2):
        merged_position = list(
            GravityParameters.compute_geometrical_center([obj1, obj2])
        )
        merged_velocity = GravityObject.compute_speed_after_collision(obj1, obj2)

        merged_obj = GravityObject(
            merged_position, merged_velocity, obj1.mass + obj2.mass
        )
        merged_obj.previous_positions.append((merged_position[0], merged_position[1]))
        merged_obj.radius = GravityObject.change_radius_after_merge(obj1, obj2)
        gravity_params.prev_positions_of_deleted_obj.append(obj1.previous_positions)
        gravity_params.prev_positions_of_deleted_obj.append(obj2.previous_positions)

        gravity_params.objects.remove(obj1)
        gravity_params.objects.remove(obj2)

        gravity_params.objects.append(merged_obj)

    @staticmethod
    def change_radius_after_merge(obj1, obj2):
        if obj1.radius >= obj2.radius:
            new_radius = obj2.radius / 5 + obj1.radius
        else:
            new_radius = obj1.radius / 5 + obj2.radius
        return new_radius

    @staticmethod
    def compute_radius_sizes(list_of_obj):
        average_mass = 0
        list_of_normalized_mass = []
        for obj in list_of_obj:
            average_mass += obj.mass
            list_of_normalized_mass.append(obj.mass)

        if len(list_of_obj) != 0:
            average_mass /= len(list_of_obj)
        else:
            return

        for i in range(len(list_of_obj)):
            list_of_obj[i].radius = OBJECT_RADIUS + 4 * atan(
                list_of_normalized_mass[i] - average_mass
            )

    @staticmethod
    def update_objects_positions(gravity_params, time):
        for obj in gravity_params.objects:
            obj.update_parameters(gravity_params.objects, time)
        gravity_params.update_params()

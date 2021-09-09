import structlog

log = structlog.get_logger(__name__)


class GravityParameters:
    def __init__(self, gravity_objects):
        self.objects = gravity_objects
        self.center_of_mass = self.compute_center_of_mass(self.objects)
        self.geometrical_center = self.compute_geometrical_center(self.objects)
        self.prev_positions_of_deleted_obj = []

    def update_params(self):
        self.center_of_mass = self.compute_center_of_mass(self.objects)

    @staticmethod
    def compute_geometrical_center(gravity_objects):
        cen_x = cen_y = 0
        for gravity_object in gravity_objects:
            cen_x += gravity_object.position[0]
            cen_y += gravity_object.position[1]
        try:
            cen_x /= len(gravity_objects)
            cen_y /= len(gravity_objects)
        except ZeroDivisionError as e:
            log.exception("Zero division error", error_message=e, info="Empty list of objects")
        return cen_x, cen_y

    @staticmethod
    def compute_center_of_mass(gravity_objects):
        cen_x = cen_y = sum_of_mass = 0
        for gravity_object in gravity_objects:
            cen_x += gravity_object.position[0] * gravity_object.mass
            cen_y += gravity_object.position[1] * gravity_object.mass
            sum_of_mass += gravity_object.mass
        try:
            cen_x /= sum_of_mass
            cen_y /= sum_of_mass
        except ZeroDivisionError as e:
            log.exception("Zero division error", error_message=e, info="Empty list of objects or sum of mass is 0")
        return cen_x, cen_y

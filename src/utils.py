from src.physics.gravity_object import GravityObject
from src.physics.gravity_parameters import GravityParameters

import json

# size of dot (used in viewing mass and geometrical center)
DOT_RADIUS = 2


def create_circle(x, y, r, canvas, tag="none", color="black"):
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1, tags=tag, fill=color)


def display_gravity_object(g_object, canvas):
    create_circle(
        g_object.position[0],
        g_object.position[1],
        g_object.radius,
        canvas,
        "g_object",
        "white",
    )


def display_all_gravity_objects(g_objects, canvas):
    for g_obj in g_objects:
        display_gravity_object(g_obj, canvas)


def display_mass_center(gravity_params, canvas):
    x = gravity_params.center_of_mass[0]
    y = gravity_params.center_of_mass[1]
    create_circle(x, y, DOT_RADIUS, canvas, "center", "red")


def display_geometrical_center(gravity, canvas):
    x, y = GravityParameters.compute_geometrical_center(gravity.objects)
    create_circle(x, y, DOT_RADIUS, canvas, "center", "purple")


def display_object_path(list_of_prev_pos, canvas):
    if len(list_of_prev_pos) >= 4:
        canvas.create_line(list_of_prev_pos, smooth=True)


def clear_canvas(canvas):
    canvas.delete("all")


def update_window(master):
    master.update()


def get_presets_from_file(filename):
    with open(filename, "r") as json_file:
        presets = json.load(json_file)
        set_ups = []
        for preset in presets["Presets"]:
            set_up = []
            for _object in preset["objects"]:
                gravity_object = GravityObject([_object["Position"]["x"],
                                                _object["Position"]["y"]],
                                               [_object["Velocity"]["x"],
                                                _object["Velocity"]["y"]],
                                               float(_object["Mass"])
                                               )
                set_up.append(gravity_object)
            set_ups.append(set_up)
    return set_ups

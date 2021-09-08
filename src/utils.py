from src.physics.gravity_object import GravityObject
from src.physics.gravity_parameters import GravityParameters

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
    file = open(filename, "r")
    set_up_list = []

    for line in file:
        s_line = line.split()

        set_up = []
        pos_x = []
        pos_y = []
        velo_x = []
        velo_y = []
        mass = []

        # counter starts at 6, because modulo from a number smaller than 7 is always 0
        counter = 6
        for exp in s_line:
            counter += 1

            if counter % 7 == 0 or counter % 7 == 6:
                # ignoring brackets
                continue
            elif counter % 7 == 1:
                # x position of an object
                pos_x.append(int(exp))
            elif counter % 7 == 2:
                # y position of an object
                pos_y.append(int(exp))
            elif counter % 7 == 3:
                # velocity in x direction of an object
                velo_x.append(float(exp))
            elif counter % 7 == 4:
                # velocity in y direction of an object
                velo_y.append(float(exp))
            elif counter % 7 == 5:
                # mass of an object
                mass.append(float(exp))

        for i in range(len(pos_x)):
            g_object = GravityObject(
                [pos_x[i], pos_y[i]], [velo_x[i], velo_y[i]], mass[i]
            )
            set_up.append(g_object)

        set_up_list.append(set_up)

    file.close()
    return set_up_list

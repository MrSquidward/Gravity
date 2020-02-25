import tkinter as tk
import physics as ph
import time


def create_circle(x, y, r, canvas, tag='none', color='black'):
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1, tags=tag, fill=color)


def display_gravity_objects(g_object1, g_object2, canvas):
    create_circle(g_object1.position[0], g_object1.position[1], 20, canvas, 'object1', 'blue')
    create_circle(g_object2.position[0], g_object2.position[1], 20, canvas, 'object2', 'blue')


def display_mass_center(g_object1, canvas):
    create_circle(g_object1.center_of_mass[0], g_object1.center_of_mass[1], 2, canvas, 'center', 'red')


def display_geometrical_center(g_object1, g_object2, canvas):
    position = ph.compute_center(g_object1, g_object2)
    create_circle(position[0], position[1], 2, canvas, 'center', 'purple')


def display_object_path(g_object, canvas):
        prev_x = int(g_object.previous_positions[0][0])
        prev_y = int(g_object.previous_positions[0][1])

        for idx in range(1, len(g_object.previous_positions)):
            x = int(g_object.previous_positions[idx][0])
            y = int(g_object.previous_positions[idx][1])

            if prev_x == x and prev_y == y:
                continue
            else:
                canvas.create_line(prev_x, prev_y, x, y)
                prev_x = x
                prev_y = y


def clear_canvas(canvas):
    canvas.delete('all')


def update_window(master):
    master.update()


class InputFrame:
    def __init__(self, master, can):
        self.root = master
        self.canvas = can

        self.frame = tk.Frame(self.root, height=600, width=200)
        self.frame.pack(side=tk.RIGHT)

        self.font = ('Arial', 14)

        self.entry_velo1 = tk.Entry(self.root)
        self.entry_mass1 = tk.Entry(self.root)
        self.entry_velo2 = tk.Entry(self.root)
        self.entry_mass2 = tk.Entry(self.root)

        # self.place_entry_fields()
        self.create_start_simulation_button()

    def place_entry_fields(self):
        self.entry_velo1.place(x=10, y=10)
        self.entry_mass1.place(x=10, y=10)
        self.entry_velo2.place(x=10, y=10)
        self.entry_mass2.place(x=10, y=10)

    def cb_start_simulation(self):
        object1 = ph.GravityObject([550, 50], [0, 0], 30E14)
        object2 = ph.GravityObject([50, 50], [0, 5], 10E14)

        while not ph.check_collision(object1, object2, 10):
            clear_canvas(self.canvas)
            ph.update_objects_positions(object1, object2, 0.08)
            display_gravity_objects(object1, object2, self.canvas)
            # display_object_path(object1, self.canvas)
            # display_object_path(object2, self.canvas)
            display_mass_center(object1, self.canvas)
            display_geometrical_center(object1, object2, self.canvas)
            update_window(self.root)
            time.sleep(0.01)

    def create_start_simulation_button(self):
        button = tk.Button(self.frame, text='Start', font=self.font, command=self.cb_start_simulation)
        button.place(x=100, y=100)

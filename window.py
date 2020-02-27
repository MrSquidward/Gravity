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


def display_mass_center(gravity_params, canvas):
    create_circle(gravity_params.center_of_mass[0], gravity_params.center_of_mass[1], 2, canvas, 'center', 'red')


def display_geometrical_center(gravity, canvas):
    create_circle(gravity.geometrical_center[0], gravity.geometrical_center[1], 2, canvas, 'center', 'purple')


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


def canvas_right_click(event):
    print(event.x, event.y)


class InputFrame:
    def __init__(self, master, can):
        self.root = master
        self.canvas = can

        self.frame = tk.Frame(self.root, height=600, width=300)
        self.frame.pack(side=tk.RIGHT)

        self.font = ('Arial', 14)

        self.entry_velo1 = tk.Entry(self.root)
        self.entry_mass1 = tk.Entry(self.root)
        self.entry_velo2 = tk.Entry(self.root)
        self.entry_mass2 = tk.Entry(self.root)

        self.is_checked_mass_center = tk.IntVar()
        self.is_checked_geom_center = tk.IntVar()
        self.is_checked_objects_paths = tk.IntVar()

        # self.place_entry_fields()
        self.create_start_simulation_button()
        self.create_checkboxes()

    def place_entry_fields(self):
        self.entry_velo1.place(x=10, y=10)
        self.entry_mass1.place(x=10, y=10)
        self.entry_velo2.place(x=10, y=10)
        self.entry_mass2.place(x=10, y=10)

    def create_checkboxes(self):
        checkbox_mass_center = tk.Checkbutton(self.frame, text='Display mass center', font=self.font)
        checkbox_geom_center = tk.Checkbutton(self.frame, text='Display geometrical center', font=self.font)
        checkbox_objects_paths = tk.Checkbutton(self.frame, text='Display objects paths', font=self.font)

        checkbox_mass_center.config(variable=self.is_checked_mass_center)
        checkbox_geom_center.config(variable=self.is_checked_geom_center)
        checkbox_objects_paths.config(variable=self.is_checked_objects_paths)

        checkbox_mass_center.place(x=10, y=300)
        checkbox_geom_center.place(x=10, y=350)
        checkbox_objects_paths.place(x=10, y=400)

    def cb_start_simulation(self):
        if self.start_simulation_button['text'] == 'Break':
            self.start_simulation_button.config(text='Start')
            #resetBtn callback here
            return
        else:
            self.start_simulation_button.config(text='Break')

        object1 = ph.GravityObject([300, 300], [0, 2], 30E14)
        object2 = ph.GravityObject([500, 500], [-10, 5], 10E14)
        gravity_params = ph.GravityParameters(object1, object2)

        while not ph.check_collision(object1, object2, 10) and self.start_simulation_button['text'] == 'Break':
            clear_canvas(self.canvas)
            ph.update_objects_positions(object1, object2, gravity_params, 0.08)
            display_gravity_objects(object1, object2, self.canvas)

            if self.is_checked_objects_paths.get():
                display_object_path(object1, self.canvas)
                display_object_path(object2, self.canvas)

            if self.is_checked_mass_center.get():
                display_mass_center(gravity_params, self.canvas)

            if self.is_checked_geom_center.get():
                display_geometrical_center(gravity_params, self.canvas)

            update_window(self.root)
            time.sleep(0.01)

        self.start_simulation_button.config(text='Start')

    def create_start_simulation_button(self):
        self.start_simulation_button = tk.Button(self.frame, font=self.font, command=self.cb_start_simulation)
        self.start_simulation_button.config(text='Start')
        self.start_simulation_button.place(x=100, y=100)

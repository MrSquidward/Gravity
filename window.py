import tkinter as tk
import physics as ph
import time

# distance between two objects that is consider as crash
COLLISION_RADIUS = 20
# radius of objects during viewing it on canvas
OBJECT_RADIUS = 20
# size of dot (used in viewing mass and geometrical center)
DOT_RADIUS = 2
# time after which new position is calculated and movement equations is updated to match distance changes
TIME_FOR_APPROXIMATION = 0.01


def create_circle(x, y, r, canvas, tag='none', color='black'):
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1, tags=tag, fill=color)


def display_gravity_object(g_object, canvas):
    create_circle(g_object.position[0], g_object.position[1], OBJECT_RADIUS, canvas, 'g_object', 'blue')


def display_all_gravity_objects(g_objects, canvas):
    for g_obj in g_objects:
        create_circle(g_obj.position[0], g_obj.position[1], OBJECT_RADIUS, canvas, 'g_object', 'blue')


def display_mass_center(gravity_params, canvas):
    x = gravity_params.center_of_mass[0]
    y = gravity_params.center_of_mass[1]
    create_circle(x, y, DOT_RADIUS, canvas, 'center', 'red')


def display_geometrical_center(gravity, canvas):
    x = gravity.geometrical_center[0]
    y = gravity.geometrical_center[1]
    create_circle(x, y, DOT_RADIUS, canvas, 'center', 'purple')


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
        self.objs_list = []

        self.frame = tk.Frame(self.root, height=600, width=300)
        self.frame.pack(side=tk.RIGHT)

        self.font = ('Arial', 14)

        self.is_checked_mass_center = tk.IntVar()
        self.is_checked_geom_center = tk.IntVar()
        self.is_checked_objects_paths = tk.IntVar()

        self.create_start_simulation_button()
        self.create_checkboxes()

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
            # resetBtn callback here
            return
        else:
            self.start_simulation_button.config(text='Break')

        gravity_params = ph.GravityParameters(self.objs_list)

        while self.start_simulation_button['text'] == 'Break':
            clear_canvas(self.canvas)
            ph.update_objects_positions(gravity_params, TIME_FOR_APPROXIMATION)
            ph.check_collision(gravity_params, COLLISION_RADIUS)

            for obj in gravity_params.objects:
                display_gravity_object(obj, self.canvas)

            if self.is_checked_objects_paths.get():
                for obj in gravity_params.objects:
                    display_object_path(obj, self.canvas)

            if self.is_checked_mass_center.get():
                display_mass_center(gravity_params, self.canvas)

            if self.is_checked_geom_center.get():
                display_geometrical_center(gravity_params, self.canvas)

            update_window(self.root)
            time.sleep(0.01)

        self.start_simulation_button.config(text='Start')

    def canvas_right_click(self, event):
        for obj in self.objs_list:
            if ph.is_position_the_same(event.x, event.y, obj.position[0], obj.position[1], OBJECT_RADIUS):
                ObjectOptions(self.root, obj, self.canvas, self.objs_list)
                return

        # object with default values
        g_object = ph.GravityObject([event.x, event.y], [0, 0], 30E14)
        self.objs_list.append(g_object)

        display_gravity_object(g_object, self.canvas)
        ObjectOptions(self.root, g_object, self.canvas, self.objs_list)

    def create_start_simulation_button(self):
        self.start_simulation_button = tk.Button(self.frame, font=self.font, command=self.cb_start_simulation)
        self.start_simulation_button.config(text='Start')
        self.start_simulation_button.place(x=100, y=100)


class ObjectOptions:
    def __init__(self, m_root, g_obj, canvas, list):
        self.g_object = g_obj
        self.canvas = canvas
        self.obj_list = list

        self.main_root = m_root
        self.root = tk.Toplevel(self.main_root)
        self.root.title('Object properties')

        self.font = ('Arial', 13)

        self.frame = tk.Frame(self.root, height=250, width=300)
        self.frame.pack()

        self.save_button = tk.Button(self.frame, command=self.cb_save)
        self.default_button = tk.Button(self.frame, command=self.cb_default_entry)

        self.entry_posx = tk.Entry(self.frame)
        self.entry_posy = tk.Entry(self.frame)
        self.entry_velox = tk.Entry(self.frame)
        self.entry_veloy = tk.Entry(self.frame)
        self.entry_mass = tk.Entry(self.frame)

        self.place_entry_fields()
        self.place_save_button()
        self.place_default_button()

    def __del__(self):
        clear_canvas(self.canvas)
        display_all_gravity_objects(self.obj_list, self.canvas)

    def place_entry_fields(self):
        lb_velox = tk.Label(self.frame, font=self.font, text='X')
        lb_veloy = tk.Label(self.frame, font=self.font, text='Y')
        lb_position = tk.Label(self.frame, font=self.font, text='Position: ')
        lb_velocity = tk.Label(self.frame, font=self.font, text='Velocity: ')
        lb_mass = tk.Label(self.frame, font=self.font, text='Mass: ')

        lb_velox.place(x=115, y=20)
        lb_veloy.place(x=215, y=20)
        lb_position.place(x=10, y=50)
        lb_velocity.place(x=10, y=100)
        lb_mass.place(x=10, y=150)

        self.entry_posx['font'] = self.font
        self.entry_posy['font'] = self.font
        self.entry_velox['font'] = self.font
        self.entry_veloy['font'] = self.font
        self.entry_mass['font'] = self.font

        self.cb_default_entry()

        self.entry_posx.place(x=100, y=50, width=50)
        self.entry_posy.place(x=200, y=50, width=50)
        self.entry_velox.place(x=100, y=100, width=50)
        self.entry_veloy.place(x=200, y=100, width=50)
        self.entry_mass.place(x=100, y=150, width=100)

    def place_default_button(self):
        self.default_button['text'] = 'Default'
        self.default_button['font'] = self.font

        self.default_button.place(x=60, y=200, width=80)

    def place_save_button(self):
        self.save_button['text'] = 'Save'
        self.save_button['font'] = self.font

        self.save_button.place(x=170, y=200, width=80)

    def cb_default_entry(self):
        self.entry_posx.delete(0, tk.END)
        self.entry_posy.delete(0, tk.END)
        self.entry_velox.delete(0, tk.END)
        self.entry_veloy.delete(0, tk.END)
        self.entry_mass.delete(0, tk.END)

        self.entry_posx.insert(0, self.g_object.position[0])
        self.entry_posy.insert(0, self.g_object.position[1])
        self.entry_velox.insert(0, self.g_object.velocity[0])
        self.entry_veloy.insert(0, self.g_object.velocity[1])
        self.entry_mass.insert(0, format(self.g_object.mass, '10.1E'))

    def cb_save(self):
        self.g_object.position = [int(self.entry_posx.get()), int(self.entry_posy.get())]
        self.g_object.velocity = [int(self.entry_velox.get()), int(self.entry_veloy.get())]
        self.g_object.mass = float(self.entry_mass.get())

        self.root.destroy()

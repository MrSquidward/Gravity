import tkinter as tk
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle

from time import sleep
from copy import deepcopy

import physics as ph

# distance between two objects that is consider as crash
COLLISION_RADIUS = 20
# size of dot (used in viewing mass and geometrical center)
DOT_RADIUS = 2
# time after which new position is calculated and movement equations is updated to match distance changes
APPROXIMATION_TIME = 0.01


def create_circle(x, y, r, canvas, tag='none', color='black'):
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1, tags=tag, fill=color)


def display_gravity_object(g_object, canvas):
    create_circle(g_object.position[0], g_object.position[1], g_object.radius, canvas, 'g_object', 'white')


def display_all_gravity_objects(g_objects, canvas):
    for g_obj in g_objects:
        display_gravity_object(g_obj, canvas)


def display_mass_center(gravity_params, canvas):
    x = gravity_params.center_of_mass[0]
    y = gravity_params.center_of_mass[1]
    create_circle(x, y, DOT_RADIUS, canvas, 'center', 'red')


def display_geometrical_center(gravity, canvas):
    x, y = ph.compute_geometrical_center(gravity.objects)
    create_circle(x, y, DOT_RADIUS, canvas, 'center', 'purple')


def display_object_path(list_of_prev_pos, canvas):
        prev_x = int(list_of_prev_pos[0][0])
        prev_y = int(list_of_prev_pos[0][1])

        for idx in range(1, len(list_of_prev_pos)):
            x = int(list_of_prev_pos[idx][0])
            y = int(list_of_prev_pos[idx][1])

            if prev_x == x and prev_y == y:
                continue
            else:
                canvas.create_line(prev_x, prev_y, x, y, tag='path')
                prev_x = x
                prev_y = y


def clear_canvas(canvas):
    canvas.delete('all')


def update_window(master):
    master.update()


def get_presets_from_file(filename):
    file = open(filename, 'r')
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
                pos_x.append(float(exp))
            elif counter % 7 == 2:
                # y position of an object
                pos_y.append(float(exp))
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
            g_object = ph.GravityObject([pos_x[i], pos_y[i]], [velo_x[i], velo_y[i]], mass[i])
            set_up.append(g_object)

        set_up_list.append(set_up)

    file.close()
    return set_up_list


class InputFrame:
    def __init__(self, master, can):
        self.root = master
        self.canvas = can
        self.objs_list = []
        self.starting_objs_list = []
        self.presets_list = get_presets_from_file('presets.txt')
        print(self.presets_list)

        style = ThemedStyle(self.root)
        style.set_theme('equilux')

        self.frame = ttk.Frame(self.root, height=600, width=300)
        self.frame.pack(side=tk.RIGHT)

        s_btn = ttk.Style()
        s_btn.configure('font.TButton', font=('verdana', 12))
        s_checkbtn = ttk.Style()
        s_checkbtn.configure('font.TCheckbutton', font=('verdana', 12))
        s_combobox = ttk.Style()
        s_combobox.configure('font.TCombobox', font=('verdana', 12))
        s_label = ttk.Style()
        s_label.configure('font.TLabel', font=('verdana', 12))
        s_small_label = ttk.Style()
        s_small_label.configure('small_font.TLabel', font=('verdana', 10))

        self.max_sleep = 0.05

        self.preset_value = tk.StringVar()
        self.speed_scale_bar = tk.DoubleVar()
        self.is_checked_mass_center = tk.IntVar()
        self.is_checked_geom_center = tk.IntVar()
        self.is_checked_objects_paths = tk.IntVar()

        self.start_simulation_button = ttk.Button(self.frame, style='font.TButton')

        self.create_combobox()
        self.create_labels()
        self.create_buttons()
        self.create_scale_bar()
        self.create_checkboxes()

    def create_labels(self):
        preset_lb = ttk.Label(self.frame, style='font.TLabel', text='Choose set up or click on grey\n'
                                                                    'canvas to create an object.')
        start_lb = ttk.Label(self.frame, style='font.TLabel', text='Click on an object to edit it.\n'
                                                                   'Then press start button.')
        restart_lb = ttk.Label(self.frame, style='font.TLabel', text='Clearing all set up and restarting \nsimulation:')
        speed_lb = ttk.Label(self.frame, style='font.TLabel', text='Set up speed of simulation: ')
        slow_lb = ttk.Label(self.frame, style='small_font.TLabel', text='slow')
        quick_lb = ttk.Label(self.frame, style='small_font.TLabel', text='quick')
        display_lb = ttk.Label(self.frame, style='font.TLabel', text='Display options:')

        preset_lb.place(x=10, y=10)
        start_lb.place(x=10, y=125)
        restart_lb.place(x=10, y=235)
        speed_lb.place(x=10, y=340)
        slow_lb.place(x=35, y=372)
        quick_lb.place(x=230, y=372)
        display_lb.place(x=15, y=475)

    def create_combobox(self):
        preset_combobox = ttk.Combobox(self.frame, justify='center', textvariable=self.preset_value,
                                       font=('verdana', 11), state='readonly')
        preset_combobox['values'] = ('None', 'First Preset', 'Second Preset')
        preset_combobox.current(0)
        preset_combobox.bind('<<ComboboxSelected>>', self.cb_preset_combobox)
        preset_combobox.place(x=70, y=65, width=160)

    def create_scale_bar(self):
        # speed is reversed, because it uses time.sleep to slow down simulation
        def_sleep = self.max_sleep - 0.01
        self.speed_scale_bar.set(def_sleep)
        speed_scale = ttk.Scale(self.frame, from_=0.0, to=self.max_sleep, variable=self.speed_scale_bar)
        speed_scale.config(length=150)
        speed_scale.place(x=75, y=370)

    def create_buttons(self):
        self.start_simulation_button.config(command=self.cb_start_simulation)
        self.start_simulation_button.config(text='Start')
        self.start_simulation_button.place(x=100, y=180, width=100)

        clear_simulation_button = ttk.Button(self.frame, style='font.TButton', command=self.cb_clear_button)
        clear_simulation_button.config(text='Clear')
        clear_simulation_button.place(x=33, y=285, width=100)

        restart_simulation_button = ttk.Button(self.frame, style='font.TButton', command=self.cb_restart_button)
        restart_simulation_button.config(text='Restart')
        restart_simulation_button.place(x=166, y=285, width=100)

    def create_checkboxes(self):
        checkbox_mass_center = ttk.Checkbutton(self.frame, text='Display mass center', style='font.TCheckbutton')
        checkbox_geom_center = ttk.Checkbutton(self.frame, text='Display geometrical center', style='font.TCheckbutton')
        checkbox_objects_paths = ttk.Checkbutton(self.frame, text='Display objects paths', style='font.TCheckbutton')

        checkbox_mass_center.config(variable=self.is_checked_mass_center)
        checkbox_geom_center.config(variable=self.is_checked_geom_center)
        checkbox_objects_paths.config(variable=self.is_checked_objects_paths)

        checkbox_mass_center.place(x=10, y=500)
        checkbox_geom_center.place(x=10, y=525)
        checkbox_objects_paths.place(x=10, y=550)

    def cb_preset_combobox(self, event):
        clear_canvas(self.canvas)
        preset_id = 0

        if self.preset_value.get() == 'None':
            self.objs_list = []
            return
        if self.preset_value.get() == 'First Preset':
            preset_id = 0
        if self.preset_value.get() == 'Second Preset':
            preset_id = 1

        self.objs_list = self.presets_list[preset_id]
        display_all_gravity_objects(self.objs_list, self.canvas)

    def cb_start_simulation(self):
        if len(self.starting_objs_list) == 0:
            self.starting_objs_list = deepcopy(self.objs_list)

        if self.start_simulation_button['text'] == 'Pause':
            self.start_simulation_button.config(text='Start')
            return
        else:
            self.start_simulation_button.config(text='Pause')

        gravity_params = ph.GravityParameters(self.objs_list)

        try:
            while self.start_simulation_button['text'] == 'Pause':
                clear_canvas(self.canvas)
                ph.update_objects_positions(gravity_params, APPROXIMATION_TIME)
                ph.check_collision(gravity_params, COLLISION_RADIUS)

                display_all_gravity_objects(gravity_params.objects, self.canvas)

                if self.is_checked_objects_paths.get():
                    for obj in gravity_params.objects:
                        display_object_path(obj.previous_positions, self.canvas)

                    for list_of_prev in gravity_params.prev_positions_of_deleted_obj:
                        display_object_path(list_of_prev, self.canvas)

                if self.is_checked_mass_center.get():
                    display_mass_center(gravity_params, self.canvas)

                if self.is_checked_geom_center.get():
                    display_geometrical_center(gravity_params, self.canvas)

                update_window(self.root)
                sleep_value = self.max_sleep - round(self.speed_scale_bar.get(), 3)
                sleep(sleep_value)

            self.start_simulation_button.config(text='Start')

        except tk.TclError as e:
            print("You have left during a simulation. Error occured: ")
            print(e)

    def cb_clear_button(self):
        self.start_simulation_button.config(text='Pause')
        self.objs_list = []
        self.starting_objs_list = []
        clear_canvas(self.canvas)
        self.start_simulation_button.config(text='Start')

    def cb_restart_button(self):
        self.start_simulation_button.config(text='Pause')
        self.objs_list = self.starting_objs_list
        self.starting_objs_list = []
        clear_canvas(self.canvas)
        display_all_gravity_objects(self.objs_list, self.canvas)
        self.start_simulation_button.config(text='Start')
        update_window(self.root)

    def canvas_right_click(self, event):
        for obj in self.objs_list:
            if ph.is_position_the_same(event.x, event.y, obj.position[0], obj.position[1], obj.radius):
                ObjectOptions(self.root, obj, self.canvas, self.objs_list)
                return

        # object with default values
        g_object = ph.GravityObject([event.x, event.y], [0, 0], 30E14)
        self.objs_list.append(g_object)

        display_gravity_object(g_object, self.canvas)
        ObjectOptions(self.root, g_object, self.canvas, self.objs_list)


class ObjectOptions:
    def __init__(self, m_root, g_obj, canvas, list_of_obj):
        self.g_object = g_obj
        self.canvas = canvas
        self.obj_list = list_of_obj

        self.main_root = m_root
        self.root = tk.Toplevel(self.main_root)
        self.root.title('Object properties')
        self.root.grab_set()

        style = ThemedStyle(self.root)
        style.set_theme('equilux')

        s_btn = ttk.Style()
        s_btn.configure('font.TButton', font=('verdana', 12))
        s_label = ttk.Style()
        s_label.configure('font.TLabel', font=('verdana', 12))

        self.frame = ttk.Frame(self.root, height=250, width=300)
        self.frame.pack()

        self.save_button = ttk.Button(self.frame, command=self.cb_save, style='font.TButton')
        self.default_button = ttk.Button(self.frame, command=self.cb_default_entry, style='font.TButton')

        font = ('verdana', 10)
        self.entry_posx = ttk.Entry(self.frame, font=font)
        self.entry_posy = ttk.Entry(self.frame, font=font)
        self.entry_velox = ttk.Entry(self.frame, font=font)
        self.entry_veloy = ttk.Entry(self.frame, font=font)
        self.entry_mass = ttk.Entry(self.frame, font=font)

        self.place_entry_fields()
        self.place_save_button()
        self.place_default_button()

    def __del__(self):
        clear_canvas(self.canvas)
        ph.compute_radius_sizes(self.obj_list)
        display_all_gravity_objects(self.obj_list, self.canvas)

    def place_entry_fields(self):
        lb_velox = ttk.Label(self.frame, style='font.TLabel', text='X')
        lb_veloy = ttk.Label(self.frame, style='font.TLabel', text='Y')
        lb_position = ttk.Label(self.frame, style='font.TLabel', text='Position: ')
        lb_velocity = ttk.Label(self.frame, style='font.TLabel', text='Velocity: ')
        lb_mass = ttk.Label(self.frame, style='font.TLabel', text='Mass: ')

        lb_velox.place(x=115, y=20)
        lb_veloy.place(x=215, y=20)
        lb_position.place(x=10, y=50)
        lb_velocity.place(x=10, y=100)
        lb_mass.place(x=10, y=150)

        self.cb_default_entry()

        self.entry_posx.place(x=100, y=50, width=50)
        self.entry_posy.place(x=200, y=50, width=50)
        self.entry_velox.place(x=100, y=100, width=50)
        self.entry_veloy.place(x=200, y=100, width=50)
        self.entry_mass.place(x=100, y=150, width=100)

    def place_default_button(self):
        self.default_button['text'] = 'Default'
        self.default_button.place(x=60, y=200, width=100)

    def place_save_button(self):
        self.save_button['text'] = 'Save'
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

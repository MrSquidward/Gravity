import tkinter as tk
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle

from time import sleep
from copy import deepcopy

from src.physics.gravity_parameters import GravityParameters
from src.physics.gravity_object import GravityObject
from src.utils import (
    get_presets_from_file,
    clear_canvas,
    display_all_gravity_objects,
    display_gravity_object,
    update_window,
    display_object_path,
    display_mass_center,
    display_geometrical_center,
)
from src.visuals.object_options_frame import ObjectOptionsFrame

# distance between two objects that is consider as crash
COLLISION_RADIUS = 20
# time after which new position is calculated and movement equations is updated to match distance changes
APPROXIMATION_TIME = 0.01


class InputFrame:
    def __init__(self, master, can):
        self.root = master
        self.canvas = can
        self.objs_list = []
        self.starting_objs_list = []
        self.presets_list = get_presets_from_file("presets.json")
        print(self.presets_list)

        style = ThemedStyle(self.root)
        style.set_theme("equilux")

        self.frame = ttk.Frame(self.root, height=600, width=300)
        self.frame.pack(side=tk.RIGHT)

        s_btn = ttk.Style()
        s_btn.configure("font.TButton", font=("verdana", 12))
        s_checkbtn = ttk.Style()
        s_checkbtn.configure("font.TCheckbutton", font=("verdana", 12))
        s_combobox = ttk.Style()
        s_combobox.configure("font.TCombobox", font=("verdana", 12))
        s_label = ttk.Style()
        s_label.configure("font.TLabel", font=("verdana", 12))
        s_small_label = ttk.Style()
        s_small_label.configure("small_font.TLabel", font=("verdana", 10))

        self.max_sleep = 0.05

        self.preset_value = tk.StringVar()
        self.speed_scale_bar = tk.DoubleVar()
        self.is_checked_mass_center = tk.IntVar()
        self.is_checked_geom_center = tk.IntVar()
        self.is_checked_objects_paths = tk.IntVar()

        self.start_simulation_button = ttk.Button(self.frame, style="font.TButton")

        self.create_combobox()
        self.create_labels()
        self.create_buttons()
        self.create_scale_bar()
        self.create_checkboxes()

    def create_labels(self):
        preset_lb = ttk.Label(
            self.frame,
            style="font.TLabel",
            text="Choose set up or click on grey\n" "canvas to create an object.",
        )
        start_lb = ttk.Label(
            self.frame,
            style="font.TLabel",
            text="Click on an object to edit it.\n" "Then press start button.",
        )
        restart_lb = ttk.Label(
            self.frame,
            style="font.TLabel",
            text="Clearing all set up and restarting \nsimulation:",
        )
        speed_lb = ttk.Label(
            self.frame, style="font.TLabel", text="Set up speed of simulation: "
        )
        slow_lb = ttk.Label(self.frame, style="small_font.TLabel", text="slow")
        quick_lb = ttk.Label(self.frame, style="small_font.TLabel", text="quick")
        display_lb = ttk.Label(self.frame, style="font.TLabel", text="Display options:")

        preset_lb.place(x=10, y=10)
        start_lb.place(x=10, y=125)
        restart_lb.place(x=10, y=235)
        speed_lb.place(x=10, y=340)
        slow_lb.place(x=35, y=372)
        quick_lb.place(x=230, y=372)
        display_lb.place(x=15, y=475)

    def create_combobox(self):
        preset_combobox = ttk.Combobox(
            self.frame,
            justify="center",
            textvariable=self.preset_value,
            font=("verdana", 11),
            state="readonly",
        )
        preset_combobox["values"] = ("None", "First Preset", "Second Preset")
        preset_combobox.current(0)
        preset_combobox.bind("<<ComboboxSelected>>", self.cb_preset_combobox)
        preset_combobox.place(x=70, y=65, width=160)

    def create_scale_bar(self):
        # speed is reversed, because it uses time.sleep to slow down simulation
        def_sleep = self.max_sleep - 0.01
        self.speed_scale_bar.set(def_sleep)
        speed_scale = ttk.Scale(
            self.frame, from_=0.0, to=self.max_sleep, variable=self.speed_scale_bar
        )
        speed_scale.config(length=150)
        speed_scale.place(x=75, y=370)

    def create_buttons(self):
        self.start_simulation_button.config(command=self.cb_start_simulation)
        self.start_simulation_button.config(text="Start")
        self.start_simulation_button.place(x=100, y=180, width=100)

        clear_simulation_button = ttk.Button(
            self.frame, style="font.TButton", command=self.cb_clear_button
        )
        clear_simulation_button.config(text="Clear")
        clear_simulation_button.place(x=33, y=285, width=100)

        restart_simulation_button = ttk.Button(
            self.frame, style="font.TButton", command=self.cb_restart_button
        )
        restart_simulation_button.config(text="Restart")
        restart_simulation_button.place(x=166, y=285, width=100)

    def create_checkboxes(self):
        checkbox_mass_center = ttk.Checkbutton(
            self.frame, text="Display mass center", style="font.TCheckbutton"
        )
        checkbox_geom_center = ttk.Checkbutton(
            self.frame, text="Display geometrical center", style="font.TCheckbutton"
        )
        checkbox_objects_paths = ttk.Checkbutton(
            self.frame, text="Display objects paths", style="font.TCheckbutton"
        )

        checkbox_mass_center.config(variable=self.is_checked_mass_center)
        checkbox_geom_center.config(variable=self.is_checked_geom_center)
        checkbox_objects_paths.config(variable=self.is_checked_objects_paths)

        checkbox_mass_center.place(x=10, y=500)
        checkbox_geom_center.place(x=10, y=525)
        checkbox_objects_paths.place(x=10, y=550)

    def cb_preset_combobox(self, event):
        clear_canvas(self.canvas)
        preset_id = 0

        if self.preset_value.get() == "None":
            self.objs_list = []
            return
        if self.preset_value.get() == "First Preset":
            preset_id = 0
        if self.preset_value.get() == "Second Preset":
            preset_id = 1

        self.objs_list = self.presets_list[preset_id]
        display_all_gravity_objects(self.objs_list, self.canvas)

    def cb_start_simulation(self):
        if len(self.starting_objs_list) == 0:
            self.starting_objs_list = deepcopy(self.objs_list)

        if self.start_simulation_button["text"] == "Pause":
            self.start_simulation_button.config(text="Start")
            return
        else:
            self.start_simulation_button.config(text="Pause")

        gravity_params = GravityParameters(self.objs_list)

        try:
            while self.start_simulation_button["text"] == "Pause":
                clear_canvas(self.canvas)
                GravityObject.update_objects_positions(
                    gravity_params, APPROXIMATION_TIME
                )
                GravityObject.check_collision(gravity_params, COLLISION_RADIUS)

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

            self.start_simulation_button.config(text="Start")

        except tk.TclError as e:
            print("You have left during a simulation. Error occured: ")
            print(e)

    def cb_clear_button(self):
        self.start_simulation_button.config(text="Pause")
        self.objs_list = []
        self.starting_objs_list = []
        clear_canvas(self.canvas)
        self.start_simulation_button.config(text="Start")

    def cb_restart_button(self):
        self.start_simulation_button.config(text="Pause")
        self.objs_list = self.starting_objs_list
        self.starting_objs_list = []
        clear_canvas(self.canvas)
        display_all_gravity_objects(self.objs_list, self.canvas)
        self.start_simulation_button.config(text="Start")
        update_window(self.root)

    def canvas_right_click(self, event):
        for obj in self.objs_list:
            if GravityObject.is_position_the_same(
                event.x, event.y, obj.position[0], obj.position[1], obj.radius
            ):
                ObjectOptionsFrame(self.root, obj, self.canvas, self.objs_list)
                return

        # object with default values
        g_object = GravityObject([event.x, event.y], [0.0, 0.0], 30e14)
        self.objs_list.append(g_object)

        display_gravity_object(g_object, self.canvas)
        ObjectOptionsFrame(self.root, g_object, self.canvas, self.objs_list)

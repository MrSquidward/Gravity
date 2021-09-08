import tkinter as tk
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle

from src.physics.gravity_object import GravityObject
from src.utils import clear_canvas, display_all_gravity_objects


class ObjectOptionsFrame:
    def __init__(self, m_root, g_obj, canvas, list_of_obj):
        self.g_object = g_obj
        self.canvas = canvas
        self.obj_list = list_of_obj

        self.main_root = m_root
        self.root = tk.Toplevel(self.main_root)
        self.root.title("Object properties")
        self.root.grab_set()

        style = ThemedStyle(self.root)
        style.set_theme("equilux")

        s_btn = ttk.Style()
        s_btn.configure("font.TButton", font=("verdana", 12))
        s_label = ttk.Style()
        s_label.configure("font.TLabel", font=("verdana", 12))

        self.frame = ttk.Frame(self.root, height=250, width=300)
        self.frame.pack()

        self.save_button = ttk.Button(
            self.frame, command=self.cb_save, style="font.TButton"
        )
        self.default_button = ttk.Button(
            self.frame, command=self.cb_default_entry, style="font.TButton"
        )

        font = ("verdana", 10)
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
        GravityObject.compute_radius_sizes(self.obj_list)
        display_all_gravity_objects(self.obj_list, self.canvas)

    def place_entry_fields(self):
        lb_velox = ttk.Label(self.frame, style="font.TLabel", text="X")
        lb_veloy = ttk.Label(self.frame, style="font.TLabel", text="Y")
        lb_position = ttk.Label(self.frame, style="font.TLabel", text="Position: ")
        lb_velocity = ttk.Label(self.frame, style="font.TLabel", text="Velocity: ")
        lb_mass = ttk.Label(self.frame, style="font.TLabel", text="Mass: ")

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
        self.default_button["text"] = "Default"
        self.default_button.place(x=60, y=200, width=100)

    def place_save_button(self):
        self.save_button["text"] = "Save"
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
        self.entry_mass.insert(0, format(self.g_object.mass, "10.1E"))

    def cb_save(self):
        self.g_object.position = [
            int(self.entry_posx.get()),
            int(self.entry_posy.get()),
        ]
        self.g_object.velocity = [
            float(self.entry_velox.get()),
            float(self.entry_veloy.get()),
        ]
        self.g_object.mass = float(self.entry_mass.get())

        self.root.destroy()

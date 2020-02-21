import tkinter as tk

def create_circle(x, y, r, canvas, tag='none', color='black'):
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1, tags=tag, fill=color)

def display_gravity_objects(g_object1, g_object2, canvas):
    create_circle(g_object1.position[0], g_object1.position[1], 20, canvas, 'object1', 'blue')
    create_circle(g_object2.position[0], g_object2.position[1], 20, canvas, 'object2', 'blue')

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

        self.entry_x1 = tk.Entry(self.root)
        self.entry_y1 = tk.Entry(self.root)
        self.entry_velo1 = tk.Entry(self.root)
        self.entry_mass1 = tk.Entry(self.root)

        self.entry_x2 = tk.Entry(self.root)
        self.entry_y2 = tk.Entry(self.root)
        self.entry_velo2 = tk.Entry(self.root)
        self.entry_mass2 = tk.Entry(self.root)

        self.place_entry_fields()
        self.create_start_simulation_button()

    def place_entry_fields(self):
        self.entry_x1.place(x=50, y=50)
        self.entry_y1.place(x=200, y=50)
        self.entry_velo1.place(x=10, y=10)
        self.entry_mass1.place(x=10, y=10)

        self.entry_x2.place(x=10, y=10)
        self.entry_y2.place(x=10, y=10)
        self.entry_velo2.place(x=10, y=10)
        self.entry_mass2.place(x=10, y=10)

    def cb_start_simulation(self):
        pass

    def create_start_simulation_button(self):
        button = tk.Button(self.frame, text='Start', font=self.font, command=self.cb_start_simulation)
        button.place(x=100, y=100)

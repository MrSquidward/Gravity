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

        self.create_start_simulation_button()

    def create_entries_fields(self):
        self.entry_x1 = tk.Entry(self.root)

    def cb_start_simulation(self):
        pass

    def create_start_simulation_button(self):
        button = tk.Button(self.frame, text='Start', font=self.font, command=self.cb_start_simulation)
        button.place(x=100, y=100)

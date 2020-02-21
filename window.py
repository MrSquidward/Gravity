import tkinter as tk
import physics as ph

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
        object1 = ph.GravityObject([150, 150], [0, 0], 10E14)
        object2 = ph.GravityObject([550, 550], [-10, 0], 10E14)
        list_of_objects = [object1, object2]
        for i in range(10000):
            list_of_objects = ph.compute_new_param(list_of_objects[0], list_of_objects[1], 0.08)
            #print(list_of_objects[0].position[0], list_of_objects[0].position[1])
            #print(list_of_objects[1].position[0], list_of_objects[1].position[1])
            #clear_canvas(self.canvas)
            display_gravity_objects(list_of_objects[0], list_of_objects[1], self.canvas)
            update_window(self.root)
            #print(i)

    def create_start_simulation_button(self):
        button = tk.Button(self.frame, text='Start', font=self.font, command=self.cb_start_simulation)
        button.place(x=100, y=100)

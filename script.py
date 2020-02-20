import window as win
import tkinter as tk
import physics as ph

master = tk.Tk()
master.title("Gravity simulator")

draw_frame = tk.Frame(master, height=600, width=800)
draw_frame.pack(side=tk.RIGHT)

canvas = tk.Canvas(draw_frame, bg='white', height=600, width=800)
canvas.pack()

time_step = 100
object1 = ph.GravityObject([10, 10], [0, 0], 100)
object2 = ph.GravityObject([20, 20], [0, 0], 100)
objects_list = [object1, object2]
while True:
    objects_list = ph.compute_new_param(objects_list[0], objects_list[1], time_step)


tk.mainloop()

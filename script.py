import window as win
import tkinter as tk

master = tk.Tk()
master.title("Gravity simulator")

draw_frame = tk.Frame(master, height=600, width=800)
draw_frame.pack(side=tk.RIGHT)

canvas = tk.Canvas(draw_frame, bg='white', height=600, width=800)
canvas.pack()

tk.mainloop()

import tkinter as tk
import physics


def create_circle(x, y, r, canvas, tag, color='black'):
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1, tags=tag, fill=color)


import tkinter as tk
import tkinter.ttk as ttk
import window as win


def main():
    master = tk.Tk()
    master.title("Gravity simulator")

    draw_frame = ttk.Frame(master, height=600, width=800)
    draw_frame.pack(side=tk.LEFT)

    canvas = tk.Canvas(draw_frame, bg='grey', height=600, width=800)
    canvas.pack()

    input_frame = win.InputFrame(master, canvas)

    canvas.bind("<Button-1>", input_frame.canvas_right_click)

    tk.mainloop()


if __name__ == "__main__":
    main()

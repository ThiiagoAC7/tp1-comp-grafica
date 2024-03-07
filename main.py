import tkinter as tk
from event_handler import *


class Screen():

    def __init__(self):
        self._width = 1280
        self._height = 720

        self.root = tk.Tk()
        self.menu = tk.Menu(self.root)

        self.root.title("main")
        self.root.geometry(f"{self._width}x{self._height}")

    def build_canvas(self):
        canvas_width, canvas_height = 800, 600

        center_x = (self._width - canvas_width) // 2
        center_y = (self._height - canvas_height) // 2

        canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height, bg="light grey")

        canvas.place(x=center_x, y=center_y)
        canvas.bind('<Button-1>', on_canvas_click)


    def build_menu(self):
        _menu = tk.Menu(self.menu, tearoff=0)
        _menu.add_command(label="Option 1", command=on_menu_option_1_click)
        _menu.add_command(label="Option 2", command=on_menu_option_2_click)
        _menu.add_command(label="Option 3", command=on_menu_option_3_click)
        # _menu.add_separator()
        self.menu.add_cascade(label="File", menu=_menu)
        self.root.config(menu=self.menu)

    def run(self):
        self.build_canvas()
        self.build_menu()
        self.root.mainloop()


screen = Screen()
screen.run()

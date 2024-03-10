import tkinter as tk
from tkinter import simpledialog, messagebox

from utils import DDA, bresenham, draw_pixel, circ_bresenham
from utils import translacao


class Screen():

    def __init__(self):
        self._width = 1280
        self._height = 720

        self._x1 = -1
        self._y1 = -1
        self._x2 = -1
        self._y2 = -1
        self._clicked = 0
        self._count_clk = self._clicked % 2

        self.root = tk.Tk()
        self.menu = tk.Menu(self.root)
        self.canvas = tk.Canvas()

        self.root.title("main")
        self.root.geometry(f"{self._width}x{self._height}")

    def run(self):
        self.build_canvas()
        self.build_clear_button()
        self.build_menu_transf_geo()
        self.build_menu_rasterizacao()
        self.build_menu_recorte()
        self.root.mainloop()

    # BUILDERS

    def build_canvas(self):
        cv_width, cv_height = 800, 600

        center_x = (self._width - cv_width) // 2
        center_y = (self._height - cv_height) // 2

        _canvas = tk.Canvas(self.root, width=cv_width,
                            height=cv_height, bg="light grey")

        self.canvas = _canvas

        _canvas.place(x=center_x, y=center_y)
        _canvas.bind('<Button-1>', self.on_canvas_click)

    def build_menu_transf_geo(self):
        transf_menu = tk.Menu(self.menu, tearoff=0)
        transf_menu.add_command(label="Translacao",
                                command=self.on_translacao_click)
        transf_menu.add_command(label="Rotacao",
                                command=self.on_rotacao_click)
        transf_menu.add_command(label="Escala",
                                command=self.on_escala_click)
        transf_menu.add_command(label="Reflexoes",
                                command=self.on_reflexoes_click)

        self.menu.add_cascade(label="Transformacoes Geometricas 2D",
                              menu=transf_menu)

        self.root.config(menu=self.menu)

    def build_menu_rasterizacao(self):
        rast_menu = tk.Menu(self.menu, tearoff=0)
        rast_menu.add_command(label="DDA", command=self.on_dda_click)
        rast_menu.add_command(label="Bresenham",
                              command=self.on_bresenham_click)
        rast_menu.add_command(label="Circunferencia - Bresenham",
                              command=self.on_circunferencia_click)

        self.menu.add_cascade(label="Rasterizacao", menu=rast_menu)
        self.root.config(menu=self.menu)

    def build_menu_recorte(self):
        rec_menu = tk.Menu(self.menu, tearoff=0)
        rec_menu.add_command(label="Cohen-Sutherland",
                             command=self.on_cohen_sutherland_click)
        rec_menu.add_command(label="Liang-Barsky",
                             command=self.on_liang_barsky_click)

        self.menu.add_cascade(label="Recorte", menu=rec_menu)

        self.root.config(menu=self.menu)

    def build_clear_button(self):
        self.clear_button = tk.Button(self.root,
                                      text="Clear",
                                      command=self.on_clear_button_click)
        self.clear_button.pack(side=tk.BOTTOM)

    # HANDLERS

    def on_translacao_click(self):
        tx, ty = self._popup_menu_vector()
        items = self.canvas.find_all()
        translacao(self, items, tx, ty)

    def on_rotacao_click(self):
        value = self._popup_menu()
        print(f"Rotacao : {value}")

    def on_escala_click(self):
        value = self._popup_menu()
        print(f"Escala : {value}")

    def on_reflexoes_click(self):
        value = self._popup_menu()
        print(f"Reflexoes : {value}")

    def on_dda_click(self):
        if self._x1 >= 0 and self._x2 >= 0:
            DDA(self, self._x1, self._y1, self._x2, self._y2)
        else:
            print("Selecione 02 pontos no Canvas")

    def on_bresenham_click(self):
        if self._x1 >= 0 and self._x2 >= 0:
            bresenham(self, self._x1, self._y1, self._x2, self._y2)
        else:
            print("Selecione 02 pontos no Canvas")

    def on_circunferencia_click(self):

        r = self._popup_menu_int("Valor do Raio :")

        if self._count_clk:
            circ_bresenham(self, self._x1, self._y1, r)
        else:
            circ_bresenham(self, self._x2, self._y2, r)
        self.canvas.delete(f"rect{self._clicked % 2}")

    def on_cohen_sutherland_click(self):
        pass

    def on_liang_barsky_click(self):
        pass

    def on_canvas_click(self, event):
        self._clicked += 1
        x, y = event.x, event.y
        print(f"Mouse clicked at ({x},{y})")

        self._count_clk = self._clicked % 2

        _tag = f"rect{self._count_clk}"

        if self._count_clk:
            if (self._x1 != -1):
                self.canvas.delete(_tag)
            self._x1 = x
            self._y1 = y
        else:
            if (self._x2 != -1):
                self.canvas.delete(_tag)
            self._x2 = x
            self._y2 = y

        draw_pixel(self, x, y, tags=_tag)

    def on_clear_button_click(self):
        self.canvas.delete("all")

    def _popup_menu(self, title="Valor :"):
        return simpledialog.askstring("Input", title)

    def _popup_menu_int(self, title="Valor :"):
        return simpledialog.askinteger("Input", title)

    def _popup_menu_vector(self, title="Translation Vector"):
        input_str = simpledialog.askstring("Input", f"{title} X, Y:")
        values = input_str.split(',')

        tx = 20
        ty = 20

        if len(values) == 2:
            tx = int(values[0].strip())
            ty = int(values[1].strip())

        return tx, ty


if __name__ == "__main__":
    screen = Screen()
    screen.run()

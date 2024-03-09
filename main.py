import tkinter as tk
from tkinter import simpledialog


class Screen():

    def __init__(self):
        self._width = 1280
        self._height = 720

        self._x1 = -1
        self._y1 = -1
        self._x2 = -1
        self._y2 = -1

        self._clicked = -1

        self.root = tk.Tk()
        self.menu = tk.Menu(self.root)
        self.canvas = tk.Canvas()

        self.root.title("main")
        self.root.geometry(f"{self._width}x{self._height}")

    def run(self):
        self.build_canvas()
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
        rast_menu.add_command(
            label="Bresenham", command=self.on_bresenham_click)
        rast_menu.add_command(label="Circunferencia",
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

    # HANDLERS

    def on_translacao_click(self):
        value = self._popup_menu()
        print(f"Translacao : {value}")

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
            self._DDA(self._x1, self._y1, self._x2, self._y2)
        else:
            print("Selecione 02 pontos no Canvas")

    def on_bresenham_click(self):
        if self._x1 >= 0 and self._x2 >= 0:
            self._bresenham(self._x1, self._y1, self._x2, self._y2)
        else:
            print("Selecione 02 pontos no Canvas")

    def on_circunferencia_click(self):
        pass

    def on_cohen_sutherland_click(self):
        pass

    def on_liang_barsky_click(self):
        pass

    def on_canvas_click(self, event):
        self._clicked += 1

        x, y = event.x, event.y

        if self._clicked % 2:
            self._x1 = x
            self._y1 = y
        else:
            self._x2 = x
            self._y2 = y

        self.canvas.create_rectangle(x, y, x+1, y+1)

    def _popup_menu(self):
        return simpledialog.askstring("Input", "Valor :")

    def _DDA(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1

        if abs(dx) > abs(dy):
            passos = abs(dx)
        else:
            passos = abs(dy)

        x_incr = dx / passos
        y_incr = dy / passos

        x = x1
        y = y1

        self.canvas.create_rectangle(x, y, x+1, y+1)

        for _ in range(passos):
            x += x_incr
            y += y_incr

            self.canvas.create_rectangle(x, y, x+1, y+1)

    def _bresenham(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1

        if (dx >= 0):
            incrx = 1
        else:
            incrx = -1
            dx = - dx

        if (dy >= 0):
            incry = 1
        else:
            incry = -1
            dy = -dy

        x = x1
        y = y1

        self.canvas.create_rectangle(x, y, x+1, y+1)

        if (dy < dx):
            p = 2*dy - dx
            c1 = 2 * dy
            c2 = 2*(dy-dx)

            for _ in range(dx):
                x += incrx
                if (p < 0):
                    p += c1
                else:
                    y += incry
                    p += c2

                self.canvas.create_rectangle(x, y, x+1, y+1)
        else:
            p = 2*dx - dy
            c1 = 2*dx
            c2 = 2*(dx - dy)

            for _ in range(dy):
                y += incry

                if (p < 0):
                    p += c1
                else:
                    x += incrx
                    p += c2

                self.canvas.create_rectangle(x, y, x+1, y+1)


if __name__ == "__main__":
    screen = Screen()
    screen.run()

import tkinter as tk
from tkinter import simpledialog


class Screen():

    def __init__(self):
        self._width = 1280
        self._height = 720

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
        _menu = tk.Menu(self.menu, tearoff=0)
        _menu.add_command(label="Translacao",
                          command=self.on_translacao_click)
        _menu.add_command(label="Rotacao",
                          command=self.on_rotacao_click)
        _menu.add_command(label="Escala",
                          command=self.on_escala_click)

        _menu.add_command(label="Reflexoes",
                          command=self.on_reflexoes_click)

        self.menu.add_cascade(label="Transformacoes Geometricas 2D",
                              menu=_menu)

        self.root.config(menu=self.menu)

    def build_menu_rasterizacao(self):
        rast_menu = tk.Menu(self.menu, tearoff=0)
        rast_menu.add_command(label="Retas", command=self.on_retas_click)
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

    def on_retas_click(self):
        pass

    def on_circunferencia_click(self):
        pass

    def on_cohen_sutherland_click(self):
        pass

    def on_liang_barsky_click(self):
        pass

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        print(f"Mouse clicked at coordinates: ({x}, {y})")

        self.canvas.create_rectangle(x, y, x+1, y+1)

    def _popup_menu(self):
        return simpledialog.askstring("Input", "Valor :")


screen = Screen()
screen.run()

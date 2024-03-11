import tkinter as tk
from tkinter import simpledialog, messagebox

from utils import DDA, bresenham, draw_pixel, circ_bresenham
from utils import translacao, escala, rotacao, reflexao


class Screen():

    def __init__(self):
        self._width = 1280
        self._height = 720

        self._x1 = None 
        self._y1 = None
        self._x2 = None
        self._y2 = None
        self._clicked = 0
        self._count_clk = self._clicked % 2

        self.root = tk.Tk()
        self.menu = tk.Menu(self.root)
        self.canvas = tk.Canvas()

        self.root.title("main")
        self.root.geometry(f"{self._width}x{self._height}")

    def run(self):
        self.build_canvas()
        self.build_labels()
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

        self.canvas = tk.Canvas(self.root, width=cv_width,
                                height=cv_height, bg="light grey")

        self.canvas.bind('<Button-1>', self.on_canvas_click)
        self.canvas.place(x=center_x, y=center_y)

        v_scrollbar = tk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.canvas.yview)
        v_scrollbar.place(x=center_x + cv_width, y=center_y, height=cv_height)

        h_scrollbar = tk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.canvas.xview)
        h_scrollbar.place(x=center_x, y=center_y + cv_height, width=cv_width)

        self.canvas.config(scrollregion=(-800, -600, 800, 600),
                           yscrollcommand=v_scrollbar.set,
                           xscrollcommand=h_scrollbar.set)


    def build_labels(self):

        center_y = self._height / 2

        font_style = ("Arial", 13)

        self.label_x1 = tk.Label(self.root, 
                                 text=f"x1, y1: ({self._x1}, {self._y1})",
                                 font=font_style)
        self.label_x1.place(x=10, y=center_y-10)
        self.label_x2 = tk.Label(self.root,
                                 text=f"x2, y2: ({self._x1}, {self._y1})",
                                 font=font_style)
        self.label_x2.place(x=10, y=center_y + 20)


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
                                      font=("Arial",13),
                                      command=self.on_clear_button_click)
        self.clear_button.pack(side=tk.BOTTOM)

    # HANDLERS

    def on_translacao_click(self):
        tx, ty = self._popup_menu_vector("Vetor de Translacao, ")
        if tx and ty:
            items = self.canvas.find_all()
            translacao(self, items, tx, ty)

    def on_rotacao_click(self):
        theta = self._popup_menu_int("Valor do Angulo theta: ")
        if theta:
            items = self.canvas.find_all()
            rotacao(self, items, theta)

    def on_escala_click(self):
        sx, sy = self._popup_menu_vector("Constantes de Escala, ")
        if sx and sy:
            items = self.canvas.find_all()
            escala(self, items, sx, sy)

    def on_reflexoes_click(self):
        ref_type = self._popup_menu("Reflexao X, Y, XY:")
        if ref_type  in ["X", "Y", "XY"]:
            items = self.canvas.find_all()
            reflexao(self,items,ref_type)

    def on_dda_click(self):
        if self._x1 != None and self._x2 != None:
            DDA(self, self._x1, self._y1, self._x2, self._y2)
        else:
            self._popup_warning("Selecione 02 pontos no Canvas")

    def on_bresenham_click(self):
        if self._x1 != None and self._x2 != None:
            bresenham(self, self._x1, self._y1, self._x2, self._y2)
        else:
            self._popup_warning("Selecione 02 pontos no Canvas")

    def on_circunferencia_click(self):
        if self._count_clk == 0:
            self._popup_warning("Selecione um ponto no canvas!")
        else:
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

        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

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
        self._update_labels()

    def on_clear_button_click(self):
        self._x1 = None 
        self._y1 = None
        self._x2 = None
        self._y2 = None
        self._clicked = 0
        self._count_clk = self._clicked % 2
        self._update_labels()
        self.canvas.delete("all")

    def _popup_menu(self, title="Valor :"):
        return simpledialog.askstring("Input", title)

    def _popup_menu_int(self, title="Valor :"):
        return simpledialog.askinteger("Input", title)

    def _popup_menu_vector(self, title=""):
        input_str = str(simpledialog.askstring("Input", f"{title} X, Y:"))

        if input_str == "":
            self._popup_warning("Digite um valor")

        values = input_str.split(',')

        tx = ty = None

        if len(values) == 2:
            tx = float(values[0].strip())
            ty = float(values[1].strip())

        return tx, ty

    def _popup_warning(self, title=""):
        messagebox.showwarning("Warning", title)

    def _update_labels(self):
        self.label_x1.config(text=f"x1, y1: ({self._x1}, {self._y1})")
        self.label_x2.config(text=f"x2, y2: ({self._x2}, {self._y2})")

if __name__ == "__main__":
    screen = Screen()
    screen.run()

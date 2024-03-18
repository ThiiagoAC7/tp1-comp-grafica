import tkinter as tk
from tkinter import simpledialog, messagebox
from line_drawing import DDA, bresenham, circ_bresenham, draw_pixel
from transformations import translacao, escala, rotacao, reflexao
from clipping import cohen_sutherland, liang_barsky


class Screen():

    def __init__(self):
        self._width = 1280
        self._height = 720

        self._xmin = 0
        self._ymin = 0
        self._xmax = 0
        self._ymax = 0

        self._x1 = 0
        self._y1 = 0
        self._x2 = 0
        self._y2 = 0
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
        self.build_buttons()
        self.build_menu_transformations()
        self.build_menu_linedrawing()
        self.build_menu_clipping()
        self.root.mainloop()

    # BUILDERS

    def build_canvas(self):
        """
        Creates a 800x600 canvas on the center of the screen,
        configuring scrollbars to go to the negative coords
        """
        cv_width, cv_height = 800, 600

        center_x = (self._width - cv_width) // 2
        center_y = (self._height - cv_height) // 2

        self.canvas = tk.Canvas(self.root, width=cv_width,
                                height=cv_height, bg="light grey")

        self.canvas.bind('<Button-1>', self.on_canvas_click)
        self.canvas.bind('<Button-3>', self.on_canvas_click)
        self.canvas.place(x=center_x, y=center_y)

        v_scrollbar = tk.Scrollbar(self.root, orient=tk.VERTICAL,
                                   command=self.canvas.yview)
        v_scrollbar.place(x=center_x + cv_width, y=center_y, height=cv_height)

        h_scrollbar = tk.Scrollbar(self.root, orient=tk.HORIZONTAL,
                                   command=self.canvas.xview)
        h_scrollbar.place(x=center_x, y=center_y + cv_height, width=cv_width)

        self.canvas.config(scrollregion=(-800, -600, 800, 600),
                           yscrollcommand=v_scrollbar.set,
                           xscrollcommand=h_scrollbar.set)

    def build_labels(self):
        """
        Creates labels for x1,y1,x2,y2
        labels for clipping window points
            xmax, ymax, xmin, ymin
        """

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

        self.label_xmin = tk.Label(self.root,
                                   text=f"xmin, ymin: ({self._xmin}, {self._ymin})",
                                   font=font_style)
        self.label_xmin.place(x=10, y=center_y + 50)

        self.label_xmax = tk.Label(self.root,
                                   text=f"xmax, ymax: ({self._xmax}, {self._ymax})",
                                   font=font_style)
        self.label_xmax.place(x=10, y=center_y + 80)

    def build_menu_transformations(self):
        """
        Creates a cascade menu for the 2d Transformation algorithms
            - translation
            - rotation
            - scale
            - reflexion
        """
        transf_menu = tk.Menu(self.menu, tearoff=0)
        transf_menu.add_command(label="Translacao",
                                command=self.on_translation_click)
        transf_menu.add_command(label="Rotacao",
                                command=self.on_rotation_click)
        transf_menu.add_command(label="Escala",
                                command=self.on_scale_click)
        transf_menu.add_command(label="Reflexoes",
                                command=self.on_reflexion_click)

        self.menu.add_cascade(label="Transformacoes Geometricas 2D",
                              menu=transf_menu)

        self.root.config(menu=self.menu)

    def build_menu_linedrawing(self):
        """
        Creates a cascade menu for the line drawing algorithms:
            - DDA
            - Bresenham
            - circular Bresenham
        """
        rast_menu = tk.Menu(self.menu, tearoff=0)
        rast_menu.add_command(label="DDA", 
                              command=self.on_dda_click)
        rast_menu.add_command(label="Bresenham",
                              command=self.on_bresenham_click)
        rast_menu.add_command(label="Circunferencia - Bresenham",
                              command=self.on_circ_bresenham_click)

        self.menu.add_cascade(label="Rasterizacao", menu=rast_menu)
        self.root.config(menu=self.menu)

    def build_menu_clipping(self):
        """
        Creates a cascade menu for the line clipping algorithms:
            - Cohen-Sutherland
            - Liang-Barsky
        """
        rec_menu = tk.Menu(self.menu, tearoff=0)
        rec_menu.add_command(label="Cohen-Sutherland",
                             command=self.on_cohen_sutherland_click)
        rec_menu.add_command(label="Liang-Barsky",
                             command=self.on_liang_barsky_click)

        self.menu.add_cascade(label="Recorte", menu=rec_menu)

        self.root.config(menu=self.menu)

    def build_buttons(self):
        """
        Creates button to clear the screen 
        """
        self.clear_button = tk.Button(self.root,
                                      text="Clear",
                                      font=("Arial", 13),
                                      command=self.on_clear_button_click)
        self.clear_button.pack(side=tk.BOTTOM)

    # HANDLERS

    def on_translation_click(self):
        """
        calls the 2d translation transformation algorithm
        """
        tx, ty = self._popup_menu_vector("Distancia de Translacao, ")
        if tx and ty:
            items = self.canvas.find_all()
            translacao(self, items, tx, ty)

    def on_rotation_click(self):
        """
        calls the rotation transformation algorithm
        """
        theta = self._popup_menu_int("Valor do Angulo theta: ")
        if theta:
            items = self.canvas.find_all()
            rotacao(self, items, theta)

    def on_scale_click(self):
        """
        calls the 2d scale transformation algorithm
        """
        sx, sy = self._popup_menu_vector("Constantes de Escala, ")
        if sx and sy:
            items = self.canvas.find_all()
            escala(self, items, sx, sy)

    def on_reflexion_click(self):
        """
        calls the 2d reflexion transformation algorithm
        """
        ref_type = self._popup_menu("Reflexao X, Y, XY:")
        if ref_type in ["X", "Y", "XY"]:
            items = self.canvas.find_all()
            reflexao(self, items, ref_type)
        else:
            self._popup_warning("Digite X, Y ou XY")

    def on_dda_click(self):
        """
        calls the DDA line drawing algorithm
        """
        if self._x1 != 0 and self._x2 != 0:
            DDA(self, self._x1, self._y1, self._x2, self._y2)
        else:
            self._popup_warning("Selecione 02 pontos no Canvas")

    def on_bresenham_click(self):
        """
        calls the bresenham line drawing algorithm
        """
        if self._x1 != 0 and self._x2 != 0:
            bresenham(self, self._x1, self._y1, self._x2, self._y2)
        else:
            self._popup_warning("Selecione 02 pontos no Canvas")

    def on_circ_bresenham_click(self):
        """
        calls the circular bresenham line drawing algorithm
        """
        if self._clicked == 0:
            self._popup_warning("Selecione um ponto no canvas!")
        else:
            r = self._popup_menu_int("Valor do Raio :")

            if self._count_clk:
                circ_bresenham(self, self._x1, self._y1, r)
            else:
                circ_bresenham(self, self._x2, self._y2, r)

            # deletes the center point of the circle
            self.canvas.delete(f"rect{self._clicked % 2}")

    def on_cohen_sutherland_click(self):
        """
        calls the Cohen-Sutherland algorithm
        """
        # clears the number of clicks, to replace the clipping window if clicked > 2
        self._clear_count_clicks()

        if self._xmin != 0:
            cohen_sutherland(self,
                             self._xmin, self._ymin, self._xmax, self._ymax,
                             self._x1, self._y1, self._x2, self._y2)
        else:
            self._popup_warning("Selecione a janela de recorte com o botao direito")

    def on_liang_barsky_click(self):
        """
        calls the Liang-Barsky algorithm
        """
        # clears the number of clicks, to replace the clipping window if clicked > 2
        self._clear_count_clicks()

        if self._xmin != 0:
            liang_barsky(self,
                         self._xmin, self._ymin, self._xmax, self._ymax,
                         self._x1, self._y1, self._x2, self._y2)
        else:
            self._popup_warning("Selecione a janela de recorte com o botao direito")

    def on_canvas_click(self, event):
        """
        Click handler for the canvas
        """

        # to handle wich point (p1 or p2) is clicked
        self._clicked += 1
        self._count_clk = self._clicked % 2

        button = event.num

        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        _tag = f"rect{self._count_clk}"

        if self._count_clk:
            # point 01 clicked
            self.canvas.delete(_tag)  # deletes the previous point
            self._x1 = x
            self._y1 = y
        else:
            # point 02 clicked
            self.canvas.delete(_tag)  # deletes the previous point
            self._x2 = x
            self._y2 = y

            if button == 3:  # right button click
                self._clipping_window_update()

        draw_pixel(self, x, y, tags=_tag)
        self._update_labels()

    def on_clear_button_click(self):
        """
        clears the private variables, 
        resets the canvas
        """
        self._clear_p1_p2()
        self._clear_pmax_pmin()
        self._clear_count_clicks()
        self._update_labels()
        self.canvas.delete("all")

    def _clear_p1_p2(self):
        """
        clears p1 and p2
        """
        self._x1 = 0
        self._y1 = 0
        self._x2 = 0
        self._y2 = 0

    def _clear_pmax_pmin(self):
        """
        clears pmax and pmin, clipping window points
        """
        self._xmin = 0
        self._ymin = 0
        self._xmax = 0
        self._ymax = 0

    def _clear_count_clicks(self):
        """
        clears the number of clicks on the canvas 
        """
        self._clicked = 0
        self._count_clk = self._clicked % 2

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
        else:
            self._popup_warning("Digite no formato X,Y")

        return tx, ty

    def _popup_warning(self, title=""):
        messagebox.showwarning("Warning", title)

    def _update_labels(self):
        self.label_x1.config(text=f"x1, y1: ({self._x1}, {self._y1})")
        self.label_x2.config(text=f"x2, y2: ({self._x2}, {self._y2})")
        self.label_xmin.config(
            text=f"xmin, ymin: ({self._xmin}, {self._ymin})")
        self.label_xmax.config(
            text=f"xmax, ymax: ({self._xmax}, {self._ymax})")

    def _clipping_window_update(self):
        """
        draws clipping window and updates points 
        """
        if self._clicked > 2:
            self.canvas.delete("clip")

        self._xmin = min(self._x1, self._x2)
        self._ymin = min(self._y1, self._y2)
        self._xmax = max(self._x1, self._x2)
        self._ymax = max(self._y1, self._y2)

        self.canvas.create_rectangle(self._x1,
                                     self._y1,
                                     self._x2,
                                     self._y2,
                                     outline="red",
                                     tags="clip")

        self._clear_p1_p2()


if __name__ == "__main__":
    screen = Screen()
    screen.run()

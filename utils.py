import math


def draw_pixel(screen, x, y, tags="default"):
    screen.canvas.create_rectangle(x, y, x+1, y+1, tags=tags)


def DDA(screen, x1, y1, x2, y2):
    dx = int(x2 - x1)
    dy = int(y2 - y1)

    if abs(dx) > abs(dy):
        passos = abs(dx)
    else:
        passos = abs(dy)

    x_incr = dx / passos
    y_incr = dy / passos

    x = x1
    y = y1

    draw_pixel(screen, x, y)

    for _ in range(passos):
        x += x_incr
        y += y_incr

        draw_pixel(screen, x, y)


def bresenham(screen, x1, y1, x2, y2):
    dx = int(x2 - x1)
    dy = int(y2 - y1)

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

    draw_pixel(screen, x, y)

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

            draw_pixel(screen, x, y)
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

            draw_pixel(screen, x, y)


def _plot_circle_points(screen, xc, yc, x, y):
    draw_pixel(screen, xc+x, yc+y)
    draw_pixel(screen, xc-x, yc+y)
    draw_pixel(screen, xc+x, yc-y)
    draw_pixel(screen, xc-x, yc-y)
    draw_pixel(screen, xc+y, yc+x)
    draw_pixel(screen, xc-y, yc+x)
    draw_pixel(screen, xc+y, yc-x)
    draw_pixel(screen, xc-y, yc-x)


def circ_bresenham(screen, xc, yc, r):
    x = 0
    y = r
    p = 3 - 2*r

    _plot_circle_points(screen, xc, yc, x, y)

    while (x < y):
        if (p < 0):
            p = p + 4*x + 6
        else:
            p = p+4*(x-y) + 10
            y = y-1
        x = x + 1
        _plot_circle_points(screen, xc, yc, x, y)


def translacao(screen, items, tx, ty):

    for item in items:
        item_coords = screen.canvas.coords(item)

        new_coords = [
            item_coords[0] + tx,
            item_coords[1] + ty,
            item_coords[2] + tx,
            item_coords[3] + ty,
        ]

        screen.canvas.coords(item, *new_coords)


def escala(screen, items, sx, sy):

    for item in items:
        item_coords = screen.canvas.coords(item)

        new_coords = [
            item_coords[0] * sx,
            item_coords[1] * sy,
            item_coords[2] * sx,
            item_coords[3] * sy,
        ]

        screen.canvas.coords(item, *new_coords)


def rotacao(screen, items, theta):

    theta = math.radians(theta)

    for item in items:
        item_coords = screen.canvas.coords(item)

        x1 = item_coords[0]
        y1 = item_coords[1]
        x2 = item_coords[2]
        y2 = item_coords[3]

        # x' = x.cos(theta) - y.sen(theta)
        # y' = x.sen(theta) + y.cos(theta)
        new_coords = [
            x1 * math.cos(theta) - y1 * math.sin(theta),
            x1 * math.sin(theta) + y1 * math.cos(theta),
            x2 * math.cos(theta) - y2 * math.sin(theta),
            x2 * math.sin(theta) + y2 * math.cos(theta),
        ]

        screen.canvas.coords(item, *new_coords)


def reflexao(screen, items, ref_type):
    for item in items:
        item_coords = screen.canvas.coords(item)

        x1 = item_coords[0]
        y1 = item_coords[1]
        x2 = item_coords[2]
        y2 = item_coords[3]

        new_coords = []

        if ref_type == "X":
            new_coords = [x1, -y1, x2, -y2]
        elif ref_type == "Y":
            new_coords = [-x1, y1, -x2, y2]
        else:
            new_coords = [-x1, -y1, -x2, -y2]

        screen.canvas.coords(item, *new_coords)


def cohen_sutherland(screen, xmin, ymin, xmax, ymax, x1, y1, x2, y2):

    def _region_code(x, y):
        code = 0

        if (x < xmin): # esq
            code += 1

        if (x > xmax): # dir
            code += 2

        if (y < ymin): # baixo 
            code += 4

        if (y > ymax): # cima
            code += 8

        return code

    accept = done = False

    while (not done):
        c1 = _region_code(x1, y1)
        c2 = _region_code(x2, y2)

        if (c1 == 0) and (c2 == 0): # line is inside 
            accept = True
            done = True
        elif (c1 & c2) != 0: # completely outside
            done = True
        else: # partially inside

            cfora = c1 if c1 else c2

            if (cfora & 1):
                xint = xmin
                yint = y1 + (y2-y1) * (xmin - x1)/(x2-x1)
            elif (cfora & 2):
                xint = xmax
                yint = y1 + (y2-y1) * (xmax - x1)/(x2-x1)
            elif (cfora & 4):
                yint = ymin
                xint = x1 + (x2-x1) * (ymin - y1)/(y2-y1)
            elif (cfora & 8):
                yint = ymax
                xint = x1 + (x2-x1) * (ymax - y1)/(y2-y1)

            if (c1 == cfora):
                x1 = xint
                y1 = yint
            else:
                x2 = xint
                y2 = yint

    if accept:
        DDA(screen, round(x1), round(y1), round(x2), round(y2))

    return accept

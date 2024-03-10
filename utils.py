def draw_pixel(screen, x, y, tags="default"):
    screen.canvas.create_rectangle(x, y, x+1, y+1, tags=tags)


def DDA(screen, x1, y1, x2, y2):
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

    draw_pixel(screen, x, y)

    for _ in range(passos):
        x += x_incr
        y += y_incr

        draw_pixel(screen, x, y)


def bresenham(screen, x1, y1, x2, y2):
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

        new_coors = [
            item_coords[0] + tx,
            item_coords[1] + ty,
            item_coords[2] + tx,
            item_coords[3] + ty,
        ]

        screen.canvas.coords(item,*new_coors)

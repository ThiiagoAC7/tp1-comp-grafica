from line_drawing import DDA


def cohen_sutherland(screen, xmin, ymin, xmax, ymax, x1, y1, x2, y2):

    def _region_code(x, y):
        code = 0

        if (x < xmin):  # esq
            code += 1

        if (x > xmax):  # dir
            code += 2

        if (y < ymin):  # baixo
            code += 4

        if (y > ymax):  # cima
            code += 8

        return code

    accept = done = False

    while (not done):
        c1 = _region_code(x1, y1)
        c2 = _region_code(x2, y2)

        if (c1 == 0) and (c2 == 0):  # line is inside
            accept = True
            done = True
        elif (c1 & c2) != 0:  # completely outside
            done = True
        else:  # partially inside

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


def liang_barsky(screen, xmin, ymin, xmax, ymax, x1, y1, x2, y2):

    def _cliptest(p, q, u1, u2):
        result = True

        if (p < 0):
            r = q/p
            if (r > u2):
                result = False
            elif (r > u1):
                u1 = r
        elif (p > 0):
            r = q/p
            if (r < u1):
                result = False
            elif (r < u2):
                u2 = r
        elif (q < 0):
            result = False

        return result, u1, u2

    u1 = 0
    u2 = 1
    dx = x2 - x1
    dy = y2 - y1

    p = [-dx, dx, -dy, dy]
    q = [
        x1 - xmin,
        xmax - x1,
        y1 - ymin,
        ymax - y1,
    ]

    _esq, u1, u2 = _cliptest(p[0], q[0], u1, u2)
    _dir, u1, u2 = _cliptest(p[1], q[1], u1, u2)
    _cima, u1, u2 = _cliptest(p[2], q[2], u1, u2)
    _baixo, u1, u2 = _cliptest(p[3], q[3], u1, u2)

    if _esq and _dir and _baixo and _cima:
        if u2 < 1:
            x2 = x1 + u2 * dx
            y2 = y1 + u2 * dy
        if u1 > 0:
            x1 = x1 + u1 * dx
            y1 = y1 + u1 * dy

        DDA(screen, round(x1), round(y1), round(x2), round(y2))

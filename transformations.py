import math


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
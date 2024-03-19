import math
from line_drawing import draw


def translacao(screen, items, tx, ty):
    """
    2d translation of the items, 
    screen: screen object
    items: all items drawn in the screen canvas
    tx, ty: distance of translation
    """

    for item in items:
        _p1 = (item["p1"][0] + tx, item["p1"][1] + ty)
        _p2 = (item["p2"][0] + tx, item["p2"][1] + ty)

        item["p1"] = _p1
        item["p2"] = _p2

        draw(screen, item) # drawing recalculated items


def escala(screen, items, sx, sy):
    """
    Scale of the items, 
    screen: screen object
    items: all items drawn in the screen canvas
    sx, sy: scaling constants 
    """
    for item in items:
        _p1 = (item["p1"][0] * sx, item["p1"][1] * sy)
        _p2 = (item["p2"][0] * sx, item["p2"][1] * sy)
        _r = item["r"] * max(sx, sy)

        item["p1"] = _p1
        item["p2"] = _p2
        item["r"] = _r

        draw(screen, item)


def rotacao(screen, items, theta):
    """
    Rotation of the items, 
    screen: screen object
    items: all items drawn in the screen canvas
    theta: angle of rotation
    """

    theta = math.radians(theta)

    for item in items:
        x1 = item["p1"][0]
        y1 = item["p1"][1]
        x2 = item["p2"][0]
        y2 = item["p2"][1]

        # x' = x.cos(theta) - y.sen(theta)
        # y' = x.sen(theta) + y.cos(theta)
        item["p1"] = (x1 * math.cos(theta) - y1 * math.sin(theta),
                      x1 * math.sin(theta) + y1 * math.cos(theta))
        item["p2"] = (x2 * math.cos(theta) - y2 * math.sin(theta),
                      x2 * math.sin(theta) + y2 * math.cos(theta))

        draw(screen, item)


def reflexao(screen, items, ref_type):
    """
    Reflexion of the items, 
    screen: screen object
    items: all items drawn in the screen canvas
    ref_type: type of reflexion (X,Y,XY) 
    """

    for item in items:
        x1 = item["p1"][0]
        y1 = item["p1"][1]
        x2 = item["p2"][0]
        y2 = item["p2"][1]

        if ref_type == "X":
            item["p1"], item["p2"] = (x1, -y1), (x2, -y2)
        elif ref_type == "Y":
            item["p1"], item["p2"] = (-x1, y1), (-x2, y2)
        else:
            item["p1"], item["p2"] = (-x1, -y1), (-x2, -y2)

        draw(screen, item)

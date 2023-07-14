from pygame import Vector2
from multipledispatch import dispatch


# Collision checking

@dispatch(tuple, tuple)
@dispatch(list, tuple)
@dispatch(Vector2, tuple)
@dispatch(tuple, list)
@dispatch(list, list)
@dispatch(Vector2, list)
def point_vs_rect(point, rectangle):
    return (rectangle[0] <= point[0] <= rectangle[0] + rectangle[2] and
            rectangle[1] <= point[1] <= rectangle[1] + rectangle[3])

@dispatch(Vector2, Vector2, Vector2)
def point_vs_rect(point, rectangle_position_left_upright_corner, rectangle_size):
    rectangle = (rectangle_position_left_upright_corner[0], rectangle_position_left_upright_corner[1],
                 rectangle_size[0], rectangle_size[1])
    return point_vs_rect(point, rectangle)

@dispatch(tuple, tuple)
@dispatch(list, tuple)
@dispatch(Vector2, tuple)
@dispatch(tuple, list)
@dispatch(list, list)
@dispatch(Vector2, list)
def point_vs_rect_round(point, rectangle):
    return (round(rectangle[0]) <= round(point[0]) <= round(rectangle[0] + rectangle[2]) and
            round(rectangle[1]) <= round(point[1]) <= round(rectangle[1] + rectangle[3]))

@dispatch(Vector2, Vector2, Vector2)
def point_vs_rect_round(point, rectangle_position_left_upright_corner, rectangle_size):
    rectangle = (rectangle_position_left_upright_corner[0], rectangle_position_left_upright_corner[1],
                 rectangle_size[0], rectangle_size[1])
    return point_vs_rect_round(point, rectangle)

@dispatch(tuple, tuple)
@dispatch(list, tuple)
@dispatch(tuple, list)
@dispatch(list, list)
def rect_vs_rect(rectangle_first, rectangle_second):
    x, y, w, h = rectangle_first
    
    points = set()
    points.add((x, y))
    points.add((x + w, y))
    points.add((x + w, y + h))
    points.add((x, y + h))

    for point in points:
        if point_vs_rect(point, rectangle_second):
            return True

    return False

@dispatch(Vector2, Vector2, Vector2, Vector2)
def rect_vs_rect(position_first, size_first, position_second, size_second):
    return rect_vs_rect((position_first[0], position_first[1], size_first[0], size_second[1]),
                        (position_second[0], position_second[1], size_second[0], size_second[1]))

@dispatch(tuple, tuple)
@dispatch(list, tuple)
@dispatch(tuple, list)
@dispatch(list, list)
def rect_vs_rect_round(rectangle_first, rectangle_second):
    x, y, w, h = rectangle_first
    
    points = set()
    points.add((x, y))
    points.add((x + w, y))
    points.add((x + w, y + h))
    points.add((x, y + h))

    for point in points:
        if point_vs_rect_round(point, rectangle_second):
            return True

    return False

@dispatch(Vector2, Vector2, Vector2, Vector2)
def rect_vs_rect_round(position_first, size_first, position_second, size_second):
    return rect_vs_rect_round((position_first[0], position_first[1], size_first[0], size_second[1]),
                              (position_second[0], position_second[1], size_second[0], size_second[1]))

import pygame


def point_in_polygon(point, polygon, main_display):
    func_1 = (polygon[0][1] - polygon[1][1]) / (polygon[0][0] - polygon[1][0])
    func_2 = (polygon[1][1] - polygon[2][1]) / (polygon[1][0] - polygon[2][0])
    func_3 = (polygon[2][1] - polygon[3][1]) / (polygon[2][0] - polygon[3][0])
    func_4 = (polygon[3][1] - polygon[0][1]) / (polygon[3][0] - polygon[0][0])

    up, down, left, right = 0, 0, 0, 0
    if point[1] > (point[0] - polygon[0][0]) * func_1 + polygon[0][1]:
        up += 1
    else:
        down += 1
    if point[1] > (point[0] - polygon[1][0]) * func_2 + polygon[1][1]:
        up += 1
    else:
        down += 1
    if point[1] > (point[0] - polygon[2][0]) * func_3 + polygon[2][1]:
        up += 1
    else:
        down += 1
    if point[1] > (point[0] - polygon[3][0]) * func_4 + polygon[3][1]:
        up += 1
    else:
        down += 1

    try:
        if point[0] > (point[1] - polygon[0][1]) / func_1 + polygon[0][0]:
            left += 1
        else:
            right += 1
    except ZeroDivisionError:
        pass
    if point[0] > (point[1] - polygon[1][1]) / func_2 + polygon[1][0]:
        left += 1
    else:
        right += 1
    try:
        if point[0] > (point[1] - polygon[2][1]) / func_3 + polygon[2][0]:
            left += 1
        else:
            right += 1
    except ZeroDivisionError:
        pass
    try:
        if point[0] > (point[1] - polygon[3][1]) / func_4 + polygon[3][0]:
            left += 1
        else:
            right += 1
    except ZeroDivisionError:
        pass

    if (left == right == 2 and (down == up == 2 or (down == 1 and up == 3))) or (left == right == down == 1 and up == 3):
        return True
    else:
        return False


def polygon_in_polygon(polygon, polygon_2, main_display):
    for i in polygon:
        if point_in_polygon(i, polygon_2, main_display):
            return True
    '''func_1 = (polygon[0][1] - polygon[1][1]) / (polygon[0][0] - polygon[1][0])
    func_2 = (polygon[1][1] - polygon[2][1]) / (polygon[1][0] - polygon[2][0])
    func_3 = (polygon[2][1] - polygon[3][1]) / (polygon[2][0] - polygon[3][0])
    func_4 = (polygon[3][1] - polygon[0][1]) / (polygon[3][0] - polygon[0][0])
    for k in range(-100, 100, 1):
        pygame.draw.circle(main_display, (255, 255, 255),
                           (k + polygon[0][0], k * func_1 + polygon[0][1]), 2)
        pygame.draw.circle(main_display, (255, 255, 255),
                           (k + polygon[1][0], k * func_2 + polygon[1][1]), 2)
        pygame.draw.circle(main_display, (255, 255, 255),
                           (k + polygon[2][0], k * func_3 + polygon[2][1]), 2)
        pygame.draw.circle(main_display, (255, 255, 255),
                           (k + polygon[3][0], k * func_4 + polygon[3][1]), 2)'''
    pygame.draw.circle(main_display, (0, 0, 0),
                       polygon[0], 2)
    pygame.draw.circle(main_display, (0, 0, 0),
                       polygon[1], 2)
    pygame.draw.circle(main_display, (0, 0, 0),
                       polygon[2], 2)
    pygame.draw.circle(main_display, (0, 0, 0),
                       polygon[3], 2)
    '''for i in polygon_2:
        if point_in_polygon(i, polygon_1, display):
            return True'''
    return False
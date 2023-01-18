import pygame_menu
from pyperclip import copy, paste
import csv
from colise_func import point_in_polygon, polygon_in_polygon
import pygame
from time import time, sleep
import os
import sys
import math

def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


tile_size = 100


class car:
    def __init__(self, path):
        self.degree = 0
        self.coord = [860, 740]
        self.images = []
        self.x_speed = 0
        self.wheel = 0
        self.y_speed = 0
        file = open(path + '\config.txt', 'r')
        file = file.readlines()


        for i in range(0, 360):
            i_coords = file[i][:-3].split('), ')
            i_coords = (tuple(i_coords[0][1:].split(', ')), tuple(i_coords[1][1:].split(', ')),
                        tuple(i_coords[2][1:].split(', ')), tuple(i_coords[3][1:].split(', ')))
            i_coords = ((int(i_coords[0][0]) * 0.185, int(i_coords[0][1]) * 0.185), (int(i_coords[2][0]) * 0.185, int(i_coords[2][1]) * 0.185),
                        (int(i_coords[1][0]) * 0.185, int(i_coords[1][1]) * 0.185), (int(i_coords[3][0]) * 0.185, int(i_coords[3][1]) * 0.185))
            self.images.append((pygame.transform.scale(pygame.image.load(path + '\\' + '0' * (4 - len(str(i))) + str(i) + '.png'), (100, 100)), i_coords))

    def draw(self):
        # i_coord = self.images[int(self.degree)][1]
        main_display.blit(self.images[int(self.degree)][0], (860, 440))

    def move(self, fps):
        deg = 0
        if self.x_speed > 0 and self.y_speed > 0:
            deg = 360 - math.degrees(math.atan(self.y_speed / self.x_speed))
        elif self.x_speed > 0 and self.y_speed < 0:
            deg = math.degrees(math.atan(-self.y_speed / self.x_speed))
        elif self.x_speed < 0 and self.y_speed > 0:
            deg = 180 + math.degrees(math.atan(self.y_speed / -self.x_speed))
        elif self.x_speed < 0 and self.y_speed < 0:
            deg = 180 - math.degrees(math.atan(-self.y_speed / -self.x_speed))

        per_deg = self.degree - 90
        if per_deg >= 180:
            drift_x = round(+ math.cos(math.radians(90 - per_deg - 270)), 5)
            drift_y = round(+ math.sin(math.radians(90 - per_deg - 270)), 5)
        elif 270 > per_deg - 90 >= 180:
            drift_y = round(- math.cos(math.radians(per_deg - 180)), 5)
            drift_x = round(- math.sin(math.radians(per_deg - 180)), 5)
        elif 180 > per_deg - 90 >= 90:
            drift_y = round(+ math.cos(math.radians(90 - per_deg - 90)), 5)
            drift_x = round(- math.sin(math.radians(90 - per_deg - 90)), 5)
        else:
            drift_y = round(+ math.cos(math.radians(per_deg - 90)), 5)
            drift_x = round(+ math.sin(math.radians(per_deg - 90)), 5)
        # pygame.draw.line(main_display, (0, 0, 0), (500, 500), (500 + drift_x * 50, 500 + drift_y * 50), 10)
        # pygame.draw.circle(main_display, (255, 0, 0), self.coord, 5)

        if self.x_speed != 0 or self.y_speed != 0:
            deg = self.degree - deg
            if deg > 180:
                deg -= 360
            elif deg < -180:
                deg += 360
            if deg > 90:
                deg = 90 - (deg - 90)
            elif deg < -90:
                deg = -90 - (90 + deg)
        else:
            deg = 0

        popr_speed_x = 0
        popr_speed_y = 0

        popr_speed_x += (drift_x * (deg / 90) * 0.03) * abs(self.x_speed)
        popr_speed_y += (drift_y * (deg / 90) * 0.03) * abs(self.y_speed)

        self.x_speed *= 0.999
        self.y_speed *= 0.999
        self.x_speed += popr_speed_x
        self.y_speed += popr_speed_y

        self.coord[0] += (self.x_speed * 0.5) / fps
        self.coord[1] += (self.y_speed * 0.5) / fps

    def get_coord(self):
        return self.coord

    def get_wheel(self):
        return self.wheel

    def set_wheel(self, degree):
        self.wheel = degree

    def change_wheel(self, degree):
        if degree > 0:
            if self.wheel + degree >= 1:
                self.wheel = 1
            else:
                self.wheel += degree
        elif degree < 0:
            if self.wheel + degree <= -1:
                self.wheel = -1
            else:
                self.wheel += degree

    def draw_wheel(self):
        pygame.draw.rect(main_display, (255, 255, 0), (20, 20, 150, 40), 5)
        pygame.draw.rect(main_display, (200, 200, 0), (94, 25, 2, 30))
        if self.wheel > 0:
            pygame.draw.rect(main_display, (200, 200, 0), (95, 25, 71 * (self.wheel / 1), 30))
        elif self.wheel < 0:
            pygame.draw.rect(main_display, (200, 200, 0), (95 - 71 * (-self.wheel / 1), 25, 71 * (-self.wheel / 1), 30))

    def change_turn_by_wheel(self, fps):
        deg = (self.degree - (
                    self.wheel * 0.5 * ((mark_2.get_speed()[0] ** 2 + mark_2.get_speed()[1] ** 2) ** 0.5)) / fps) % 360
        if deg == 360:
            deg = 0
        self.degree = deg

    def set_coord(self, coord):
        self.coord = list(coord)

    def change_turn(self, degree):
        deg = (self.degree - degree) % 360
        if deg == 360:
            deg = 0
        self.degree = deg

    def get_4_coords(self):
        return self.images[int(self.degree)][1]

    def get_degree(self):
        return self.degree

    def set_degree(self, degree):
        self.degree = degree

    def change_speed(self, speed):
        if self.degree >= 270:
            self.x_speed -= speed * math.cos(math.radians(90 - self.degree - 270))
            self.y_speed -= speed * math.sin(math.radians(90 - self.degree - 270))
        elif 270 > self.degree >= 180:
            self.x_speed -= speed * math.cos(math.radians(self.degree - 180))
            self.y_speed += speed * math.sin(math.radians(self.degree - 180))
        elif 180 > self.degree >= 90:
            self.x_speed += speed * math.cos(math.radians(90 - self.degree - 90))
            self.y_speed += speed * math.sin(math.radians(90 - self.degree - 90))
        else:
            self.x_speed += speed * math.cos(math.radians(self.degree))
            self.y_speed -= speed * math.sin(math.radians(self.degree))

    def set_speed(self, speed):
        self.x_speed = speed[0]
        self.y_speed = speed[1]

    def get_speed(self):
        ret = (self.x_speed, self.y_speed)
        return ret


mark_2 = car('mark_2')


# online_car = car('mark_2')

def online():
    global connect_type
    global online_car
    if connect_type:
        global server
        global client
    else:
        global client

    while True:
        a = client.recv(1024).decode()
        a = a.split(';')
        for i in a[:-1]:
            s = i.split(':')
            try:
                s = (float(s[0]), float(s[1]), int(s[2]))
                online_car.set_coord((s[0], s[1]))
                online_car.set_degree(s[2])
            except IndexError:
                print(a[0])


class Snow(pygame.sprite.Sprite):
    image = load_image("D:\pythonProject\YANDEXPROJECT_2_feat.Slave\снег (2).jpg")

    def __init__(self, x, y, group):
        super().__init__(group)
        self.image = Snow.image
        self.type = 0
        self.cx = x * tile_size
        self.cy = y * tile_size
        self.rect = self.image.get_rect().move(
            tile_size * x, tile_size * y)
        self.rect.x = x * tile_size
        self.rect.y = y * tile_size


class Road(pygame.sprite.Sprite):
    image = load_image("D:\pythonProject\YANDEXPROJECT_2_feat.Slave\асфальт (2).jpg")

    def __init__(self, x, y, group):
        super().__init__(group)
        self.image = Road.image
        self.type = 1
        self.cx = x * tile_size
        self.cy = y * tile_size
        self.rect = self.image.get_rect().move(
            tile_size * x, tile_size * y)
        self.rect.x = x * tile_size
        self.rect.y = y * tile_size


class Button:
    def __init__(self, x, y, im):
        self.im = pygame.image.load(im)
        self.im_new = pygame.transform.scale(self.im, (200, 200))
        self.rect = self.im_new.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        surface.blit(self.im_new, (self.rect.x, self.rect.y))
        return action


def generate_level(level, all_sprites):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '0':
                Snow(x, y, all_sprites[0])
            '''else:
                Road(x, y, all_sprites[1])'''

    return x, y


class MapMark:
    def __init__(self, lvl_number):
        self.map = []
        self.lvl_path = f'level_{lvl_number}_grid_map_layout.csv'
        with open(self.lvl_path, encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                self.map.append(row)
        self.x_cam = 0
        self.y_cam = 0




'''def start_the_game_off():
    global show_menu
    show_menu = False


def start_the_game_on():
    # Do the job here !
    pass


def start_the_game_serv():
    ip = 'blablabla'
    a.set_title(f'Код ({ip}) был скопирован в буфер обмена!')
    Код ({ip}) был скопирован в буфер обмена!
    copy(ip)
    pass


def menu():
    menu = pygame_menu.Menu('Mark and pillars', 1920, 1080,
                                theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('Играть онлайн', start_the_game_on)
    menu.add.text_input('Код команты: ', default='', maxchar=40, input_underline='_')
    menu.add.vertical_margin(20)
    menu.add.button('Играть оффлайн', start_the_game_off)
    menu.add.button('Запустить сервер', start_the_game_serv)
    a = menu.add.label(f'', max_char=-1, font_size=20
    menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
    menu.add.button('Выйти', pygame_menu.events.EXIT)
    image_path = 'mark_and_pillar_bg.jpg'
    menu.add.image(image_path, scale=(1, 1))

    pygame.display.update()

    while True:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                break
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()'''


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    size = width, height = 1920, 1080
    main_display = pygame.display.set_mode(size)
    main_display.fill('black')
    bg = pygame.image.load("mark_and_pillar_bg.jpg")
    running = True
    display_x_size, display_y_size = pygame.display.get_window_size()
    keys = []
    fps = 60
    map = MapMark(1)
    all_snow = pygame.sprite.Group()
    all_road = pygame.sprite.Group()
    all_sprites = [all_snow, all_road]
    offset_x = 0
    offset_y = 0
    im_start = 'start_btn.png'
    im_end = 'quit_btn.png'
    n = 0
    btn_start = Button(760, 240, im_start)
    btn_quit = Button(760, 560, im_end)
    started = False
    while running:
        tt = time()
        main_display.fill((0, 40, 0))
        pygame.display.update()
        if not started:
            pygame.display.flip()
            main_display.blit(bg, (0, 0))
            if btn_start.draw(main_display):
                started = True
            elif btn_quit.draw(main_display):
                running = False
        else:
            generate_level(map.map, all_sprites)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == 119 and 'W' not in keys:  # W
                        keys.append('W')
                    elif event.key == 97 and 'A' not in keys:  # A
                        keys.append('A')
                    elif event.key == 115 and 'S' not in keys:  # S
                        keys.append('S')
                    elif event.key == 100 and 'D' not in keys:  # D
                        keys.append('D')
                    elif event.key == 32 and ' ' not in keys:  # space
                        keys.append(' ')
                if event.type == pygame.KEYUP:
                    if event.key == 119:  # W
                        keys.remove('W')
                    elif event.key == 97:  # A
                        keys.remove('A')
                    elif event.key == 115:  # S
                        keys.remove('S')
                    elif event.key == 100:  # D
                        keys.remove('D')

            main_display.fill((0, 40, 0))
            if 'A' in keys:
                # mark_2.change_turn((-0.5 * ((mark_2.get_speed()[0] ** 2 + mark_2.get_speed()[1] ** 2) ** 0.5)) / fps)
                # mark_2.change_turn(-0.1)
                mark_2.change_wheel(-0.01)
            if 'D' in keys:
                # mark_2.change_turn((0.5 * ((mark_2.get_speed()[0] ** 2 + mark_2.get_speed()[1] ** 2) ** 0.5)) / fps)
                # mark_2.change_turn(0.1)
                mark_2.change_wheel(0.01)
            if not 'D' in keys and not 'A' in keys:
                if abs(mark_2.get_wheel()) < 0.01:
                    mark_2.set_wheel(0)
                elif mark_2.get_wheel() > 0:
                    mark_2.change_wheel(-0.01)
                elif mark_2.get_wheel() < 0:
                    mark_2.change_wheel(0.01)
            if 'W' in keys:
                mark_2.change_speed(10)
            if 'S' in keys:
                mark_2.change_speed(-10)
            if ' ' in keys:
                mark_2.set_coord((50, 800))
                mark_2.set_speed((0, 0))
                mark_2.set_degree(1)
                # main_display.fill((0, 40, 0))
                keys.remove(' ')
            offset_x = -mark_2.coord[0]
            offset_y = -mark_2.coord[1]
            for group in all_sprites:
                group.update()
                group.draw(main_display)

            for group in all_sprites:
                for elem in group:
                    elem.rect.x = elem.cx + offset_x
                    elem.rect.y = elem.cy + offset_y
                    if elem.type == 0:
                        coords = ((mark_2.get_4_coords()[0][0] + offset_x, mark_2.get_4_coords()[0][1] + offset_y),
                                  (mark_2.get_4_coords()[1][0] + offset_x, mark_2.get_4_coords()[1][1] + offset_y),
                                  (mark_2.get_4_coords()[2][0] + offset_x, mark_2.get_4_coords()[2][1] + offset_y),
                                  (mark_2.get_4_coords()[3][0] + offset_x, mark_2.get_4_coords()[3][1] + offset_y))
                        if polygon_in_polygon(((elem.rect.x, elem.rect.y), (elem.rect.x + 100, elem.rect.y),
                                               (elem.rect.x + 101, elem.rect.y + 100),
                                               (elem.rect.x + 1, elem.rect.y + 100)), coords, main_display):
                            pass

            mark_2.change_turn_by_wheel(fps)
            mark_2.draw()
            mark_2.move(fps)
            mark_2.draw_wheel()
            pygame.display.update()
            clock.tick(66)
            # print(1 / (time() - tt))
            # print(keys)
            try:
                fps = 1 / (time() - tt)
            except:
                fps = 1000
        pygame.quit()
'''while running:
    tt = time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == 119 and 'W' not in keys:  # W
                keys.append('W')
            elif event.key == 97 and 'A' not in keys:  # A
                keys.append('A')
            elif event.key == 115 and 'S' not in keys:  # S
                keys.append('S')
            elif event.key == 100 and 'D' not in keys:  # D
                keys.append('D')
            elif event.key == 32 and ' ' not in keys:  # space
                keys.append(' ')
        if event.type == pygame.KEYUP:
            if event.key == 119:  # W
                keys.remove('W')
            elif event.key == 97:  # A
                keys.remove('A')
            elif event.key == 115:  # S
                keys.remove('S')
            elif event.key == 100:  # D
                keys.remove('D')

    main_display.fill((0, 40, 0))
    if 'A' in keys:
        # mark_2.change_turn((-0.5 * ((mark_2.get_speed()[0] ** 2 + mark_2.get_speed()[1] ** 2) ** 0.5)) / fps)
        # mark_2.change_turn(-0.1)
        mark_2.change_wheel(-0.01)
    if 'D' in keys:
        # mark_2.change_turn((0.5 * ((mark_2.get_speed()[0] ** 2 + mark_2.get_speed()[1] ** 2) ** 0.5)) / fps)
        # mark_2.change_turn(0.1)
        mark_2.change_wheel(0.01)
    if not 'D' in keys and not 'A' in keys:
        if abs(mark_2.get_wheel()) < 0.01:
            mark_2.set_wheel(0)
        elif mark_2.get_wheel() > 0:
            mark_2.change_wheel(-0.01)
        elif mark_2.get_wheel() < 0:
            mark_2.change_wheel(0.01)
    if 'W' in keys:
        mark_2.change_speed(10)
    if 'S' in keys:
        mark_2.change_speed(-10)
    if ' ' in keys:
        mark_2.set_coord((50, 800))
        mark_2.set_speed((0, 0))
        mark_2.set_degree(1)
        # main_display.fill((0, 40, 0))
        keys.remove(' ')
    offset_x = -mark_2.coord[0]
    offset_y = -mark_2.coord[1]
    for group in all_sprites:
        group.update()
        group.draw(main_display)

    for group in all_sprites:
        for elem in group:
            elem.rect.x = elem.cx + offset_x
            elem.rect.y = elem.cy + offset_y
            if elem.type == 0:
                coords = ((mark_2.get_4_coords()[0][0] + offset_x, mark_2.get_4_coords()[0][1] + offset_y),
                          (mark_2.get_4_coords()[1][0] + offset_x, mark_2.get_4_coords()[1][1] + offset_y),
                          (mark_2.get_4_coords()[2][0] + offset_x, mark_2.get_4_coords()[2][1] + offset_y),
                          (mark_2.get_4_coords()[3][0] + offset_x, mark_2.get_4_coords()[3][1] + offset_y))
                if polygon_in_polygon(((elem.rect.x, elem.rect.y), (elem.rect.x + 100, elem.rect.y),
                                       (elem.rect.x + 101, elem.rect.y + 100),
                                       (elem.rect.x + 1, elem.rect.y + 100)), coords, main_display):
                    pass

    mark_2.change_turn_by_wheel(fps)
    mark_2.draw()
    mark_2.move(fps)
    mark_2.draw_wheel()
    pygame.display.update()
    clock.tick(66)
    # print(1 / (time() - tt))
    # print(keys)
    try:
        fps = 1 / (time() - tt)
    except:
        fps = 1000
pygame.quit()'''
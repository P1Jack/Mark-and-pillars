import pygame
import math
import socket
import threading
from time import time, sleep
import pygame_menu
from pyperclip import copy, paste
import sys, os


def point_in_polygon(point, polygon, coord):
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

def polygon_in_polygon(polygon_1, polygon_2):
    for i in polygon_1:
        if point_in_polygon(i, polygon_2):
            return True
    for i in polygon_2:
        if point_in_polygon(i, polygon_1):
            return True
    return False


class car:
    def __init__(self, path):
        self.degree = 0
        self.coord = [500, 500]
        self.images = []
        self.x_speed = 0
        self.y_speed = 0
        file = open(path + '\\config.txt', 'r')
        file = file.readlines()


        for i in range(0, 360):
            i_coords = file[i][:-3].split('), ')
            i_coords = (tuple(i_coords[0][1:].split(', ')), tuple(i_coords[1][1:].split(', ')),
                        tuple(i_coords[2][1:].split(', ')), tuple(i_coords[3][1:].split(', ')))
            i_coords = ((int(i_coords[0][0]) * 0.185, int(i_coords[0][1]) * 0.185), (int(i_coords[2][0]) * 0.185, int(i_coords[2][1]) * 0.185),
                        (int(i_coords[1][0]) * 0.185, int(i_coords[1][1]) * 0.185), (int(i_coords[3][0]) * 0.185, int(i_coords[3][1]) * 0.185))
            self.images.append((pygame.transform.scale(pygame.image.load(path + '\\' + '0' * (4 - len(str(i))) + str(i) + '.png'), (200, 200)), i_coords))

    def draw(self):
        i_coord = self.images[int(self.degree)][1]
        main_display.blit(self.images[int(self.degree)][0], self.coord)
        pygame.draw.polygon(main_display, (0, 0, 0), ((i_coord[0][0] + self.coord[0], i_coord[0][1] + self.coord[1]),
                                                      (i_coord[1][0] + self.coord[0], i_coord[1][1] + self.coord[1]),
                                                      (i_coord[2][0] + self.coord[0], i_coord[2][1] + self.coord[1]),
                                                      (i_coord[3][0] + self.coord[0], i_coord[3][1] + self.coord[1])))

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

        self.coord[0] += self.x_speed / fps
        self.coord[1] += self.y_speed / fps

    def get_coord(self):
        return self.coord

    def set_coord(self, coord):
        self.coord = list(coord)

    def change_turn(self, degree):
        self.degree = (self.degree - degree) % 360

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

"""if input() == 'host':
    server = socket.socket()
    server.bind(('', 9090))
    server.listen(1)

    client, client_ip = server.accept()
    connect_type = True
else:
    print('client_mode')
    client = socket.socket()
    client.connect((input(), 9090))
    connect_type = False"""

def main_game():
    global connect_type
    global client
    mark_2 = car('mark_2')
    if connect_type != 'offline':
        online_car = car('mark_2')

    def online():
        global connect_type
        global online_car
        if connect_type == 'server':
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

    if connect_type != 'offline':
        for online_thread in [threading.Thread(target=online)]:
            online_thread.start()


    game_over = False
    fps = 60
    while not game_over:
        tt = time()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
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
            elif event.type == pygame.KEYUP:
                if event.key == 119:  # W
                    keys.remove('W')
                elif event.key == 97:  # A
                    keys.remove('A')
                elif event.key == 115:  # S
                    keys.remove('S')
                elif event.key == 100:  # D
                    keys.remove('D')

        if 'A' in keys:
            mark_2.change_turn((-0.5 * ((mark_2.get_speed()[0] ** 2 + mark_2.get_speed()[1] ** 2) ** 0.5)) / fps)
            mark_2.change_turn(-1)
        if 'D' in keys:
            mark_2.change_turn((0.5 * ((mark_2.get_speed()[0] ** 2 + mark_2.get_speed()[1] ** 2) ** 0.5)) / fps)
            mark_2.change_turn(1)
        if 'W' in keys:
            mark_2.change_speed(10)
        if 'S' in keys:
            mark_2.change_speed(-10)
        if ' ' in keys:
            # mark_2.set_coord((50, 800))
            mark_2.set_speed((0, 0))
            # mark_2.set_degree(1)
            # main_display.fill((0, 40, 0))
            keys.remove(' ')

        main_display.fill((0, 40, 0))
        mark_2.move(fps)
        mark_2.draw()
        #online_car.draw()
        pygame.display.flip()

        if connect_type != 'offline':
            data = str(mark_2.get_coord()[0]) + ':' + str(mark_2.get_coord()[1]) + ':' + str(mark_2.get_degree()) + ';'
            client.send(data.encode())

        clock.tick(60)
        # print(int(fps))
        try:
            fps = 1 / (time() - tt)
        except:
            fps = 1000

    pygame.quit()

def start_the_game_off():
    connect_type = 'offline'


def start_the_game_on():
    '''connect_type = 'client'
    client = socket.socket()
    client.connect((server_ip.get_value(), 9090))
    client.settimeout(10)
    main_game()'''


def start_the_game_serv():
    '''connect_type = 'server'
    ip = socket.gethostname
    label.set_title(f'Код ({ip}) был скопирован в буфер обмена!')
    Код ({ip}) был скопирован в буфер обмена
    copy(ip)
    server = socket.socket()
    server.bind(('', 9090))
    server.listen(1)
    client, client_ip = server.accept()'''


def menu():

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
            sys.exit()
    main_display.fill('black')
    bg = pygame.image.load("mark_and_pillar_bg.jpg")
    menu = pygame_menu.Menu('Mark and pillars', 1920, 1080, theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('Играть онлайн', start_the_game_on)
    server_ip = menu.add.text_input('Код команты: ', default='', maxchar=40, input_underline='_')
    menu.add.vertical_margin(20)
    menu.add.button('Играть оффлайн', start_the_game_off)
    menu.add.button('Запустить сервер', start_the_game_serv)
    label = menu.add.label(f'', max_char=-1, font_size=20)
    menu.add.button('Выйти', pygame_menu.events.EXIT)
    image_path = 'mark_and_pillar_bg.jpg'
    menu.add.image(image_path, scale=(1, 1))
    menu.mainloop(main_display)
    main_display.blit('bg', (0, 0))
    pygame.display.flip()


pygame.init()
show_menu = True
main_display = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
# main_display = pygame.display.set_mode((1920, 1000))
pygame.display.set_caption('Game')

clock = pygame.time.Clock()
display_x_size, display_y_size = pygame.display.get_window_size()

keys = []
connect_type = ''

if show_menu:
    menu()
    pygame.time.delay(1500)

    show_menu = False

else:
    main_game()
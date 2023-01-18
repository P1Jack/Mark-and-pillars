import pygame
import math
import socket
import threading

if input() == 'host':
    print('host_mode')
    my_ip = socket.gethostname()
    print(my_ip)
    server = socket.socket()
    server.bind(('', 9090))
    server.listen(1)

    client, client_ip = server.accept()
    print('connected')
    connect_type = True
else:
    print('client_mode')
    client = socket.socket()
    client.connect((input(), 9090))
    print('connected')
    connect_type = False

pygame.init()
main_display = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
pygame.display.set_caption('Game')

clock = pygame.time.Clock()
display_x_size, display_y_size = pygame.display.get_window_size()

keys = []

class car:
    def __init__(self, path):
        self.degree = 0
        self.coord = [500, 500]
        self.images = []
        self.x_speed = 0
        self.y_speed = 0
        for i in range(0, 360):
            self.images.append(pygame.transform.scale(pygame.image.load(path + '\\' + '0' * (4 - len(str(i))) + str(i) + '.png'), (200, 200)))

    def draw(self):
        main_display.blit(self.images[self.degree], self.coord)

    def move(self):
        self.coord[0] += self.x_speed
        self.coord[1] += self.y_speed

        deg = 0
        if self.x_speed > 0 and self.y_speed > 0:
            deg = 360 - math.degrees(math.atan(self.y_speed / self.x_speed))
        elif self.x_speed > 0 and self.y_speed < 0:
            deg = math.degrees(math.atan(-self.y_speed / self.x_speed))
        elif self.x_speed < 0 and self.y_speed > 0:
            deg = 180 + math.degrees(math.atan(self.y_speed / -self.x_speed))
        elif self.x_speed < 0 and self.y_speed < 0:
            deg = 180 - math.degrees(math.atan(-self.y_speed / -self.x_speed))


        self.x_speed *= 0.99 - abs(deg - self.degree) * 0.0002
        self.y_speed *= 0.99 - abs(deg - self.degree) * 0.0002

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

mark_2 = car('mark_2')
online_car = car('mark_2')

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
                s = (float(s[0]), float(s[1]), float(s[2]))
                online_car.set_coord((s[0], s[1]))
                online_car.set_degree(int(s[2]))
            except IndexError:
                print(s)


for online_thread in [threading.Thread(target=online)]:
    online_thread.start()


game_over = False
while not game_over:

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
        mark_2.change_turn(-3)
    if 'D' in keys:
        mark_2.change_turn(3)
    if 'W' in keys:
        mark_2.change_speed(0.2)
    if 'S' in keys:
        mark_2.change_speed(-0.2)
    if ' ' in keys:
        mark_2.set_coord((0, 0))
        keys.remove(' ')

    mark_2.move()

    main_display.fill((0, 40, 0))
    mark_2.draw()
    online_car.draw()
    pygame.display.flip()

    data = str(mark_2.get_coord()[0]) + ':' + str(mark_2.get_coord()[1]) + ':' + str(mark_2.get_degree()) + ';'
    client.send(data.encode())

    clock.tick(66)

pygame.quit()
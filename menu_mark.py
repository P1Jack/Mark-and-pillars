import pygame
import pygame_menu
from pyperclip import copy, paste


def start_the_game_off():
    # Do the job here !
    pass


def start_the_game_on():
    # Do the job here !
    pass


def start_the_game_serv():
    ip = 'blablabla'
    a.set_title(f'Код ({ip}) был скопирован в буфер обмена!')
    '''Код ({ip}) был скопирован в буфер обмена!'''
    copy(ip)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1920, 1080
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)
    screen.fill('black')
    bg = pygame.image.load("mark_and_pillar_bg.jpg")
    running = True
    menu = pygame_menu.Menu('Mark and pillars', 1920, 1080,
                            theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('Играть онлайн', start_the_game_on)
    menu.add.text_input('Код команты: ', default='', maxchar=40, input_underline='_')
    menu.add.vertical_margin(20)
    menu.add.button('Играть оффлайн', start_the_game_off)
    menu.add.button('Запустить сервер', start_the_game_serv)
    a = menu.add.label(f'', max_char=-1, font_size=20)
    '''menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)'''
    menu.add.button('Выйти', pygame_menu.events.EXIT)
    image_path = 'mark_and_pillar_bg.jpg'
    menu.add.image(image_path, scale=(1, 1))
    ''' while True:
        events = pygame.event.get()
        for event in events:
            if event.type == update_loading:
                progress = loading.get_widget("1")
                progress.set_value(progress.get_value() + 1)
                if progress.get_value() == 100:
                    pygame.time.set_timer(update_loading, 0)
            if event.type == pygame.QUIT:
                exit()

        if menu.is_enabled():
            menu.update(events)
            menu.draw(surface)
            if (mainmenu.get_current().get_selected_widget()):
                arrow.draw(surface, mainmenu.get_current().get_selected_widget())

        pygame.display.update()
        screen.blit('bg', (0, 0))
        pygame.display.flip()
        pygame.quit()
'''
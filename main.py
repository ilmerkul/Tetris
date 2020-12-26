import os
import sys

import pygame
import pygame_gui

import history

pygame.init()
pygame.display.set_caption('Tetris')
SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
manager = pygame_gui.UIManager(SIZE)
FPS = 60


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def start_screen():
    line = 'Tetris'

    fon = pygame.transform.scale(load_image('data/startScreenBackground.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(fon, (0, 0))

    font = pygame.font.Font(None, 100)
    string_rendered = font.render(line, True, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 100
    intro_rect.x = SCREEN_WIDTH // 2 - 100
    screen.blit(string_rendered, intro_rect)

    buttonWidth = 300
    buttonHeight = 50
    buttonTop = 250
    buttonSpace = 20
    buttonStartGame = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(((SCREEN_WIDTH - buttonWidth) // 2, buttonTop), (buttonWidth, buttonHeight)),
        text='Start Game',
        manager=manager)
    buttonSettings = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(((SCREEN_WIDTH - buttonWidth) // 2, buttonTop + buttonHeight + buttonSpace),
                                  (buttonWidth, buttonHeight)),
        text='Settings',
        manager=manager)
    buttonHistory = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(((SCREEN_WIDTH - buttonWidth) // 2, buttonTop + 2 * (buttonHeight + buttonSpace)),
                                  (buttonWidth, buttonHeight)),
        text='History',
        manager=manager)
    buttonExit = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(((SCREEN_WIDTH - buttonWidth) // 2, buttonTop + 3 * (buttonHeight + buttonSpace)),
                                  (buttonWidth, buttonHeight)),
        text='Exit',
        manager=manager)

    while True:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == buttonStartGame:
                        print('Start Game!')
                        return
                    if event.ui_element == buttonSettings:
                        print('Settings!')
                    if event.ui_element == buttonHistory:
                        print('History!')

                    if event.ui_element == buttonExit:
                        terminate()

            manager.process_events(event)

        manager.update(time_delta)

        pygame.display.flip()
        manager.draw_ui(screen)
        clock.tick(FPS)


start_screen()


def write_history():
    line = 'History'

    fon = pygame.transform.scale(load_image('data/startScreenBackground.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(fon, (0, 0))

    font = pygame.font.Font(None, 100)
    string_rendered = font.render(line, True, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 50
    intro_rect.x = SCREEN_WIDTH // 2 - 100
    screen.blit(string_rendered, intro_rect)

    with open('history.txt', 'r', encoding='utf-8') as hist:
        file = [line.strip() for line in hist]

    while True:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            manager.process_events(event)

        manager.update(time_delta)

        pygame.display.flip()
        manager.draw_ui(screen)
        clock.tick(FPS)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()

    clock.tick(FPS)
    pygame.display.flip()

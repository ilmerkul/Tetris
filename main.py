import os
import sys
from pprint import pprint
from random import randrange

import pygame
import pygame_gui

pygame.init()
pygame.display.set_caption('Tetris')
SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
manager = pygame_gui.UIManager(SIZE)
FPS = 60

scale = 30
W, H = 10, 20
figuresPos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
              [(0, -1), (-1, -1), (-1, 0), (0, 0)],
              [(-1, 0), (-1, 1), (0, 0), (0, -1)],
              [(0, 0), (-1, 0), (0, 1), (-1, -1)],
              [(0, 0), (0, -1), (0, 1), (-1, -1)],
              [(0, 0), (0, -1), (0, 1), (1, -1)],
              [(0, 0), (0, -1), (0, 1), (-1, 0)]]


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


def write_history():
    manager_hist = pygame_gui.UIManager(SIZE)
    fon = pygame.transform.scale(load_image('historyMenuBackground.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(fon, (0, 0))

    with open('history.txt', 'r', encoding='utf-8') as hist:
        file = [line.strip() for line in hist]
    font = pygame.font.Font(None, 20)

    for i in range(len(file)):
        text = font.render(file[i], True, pygame.Color('white'))
        text_x = SCREEN_WIDTH // 2 - text.get_width() // 2
        text_y = 5
        screen.blit(text, (text_x, text_y + 20 * i))

    buttonWidth = 100
    buttonHeight = 50
    buttonTop = 0
    buttonStartGame = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((buttonTop, buttonTop), (buttonWidth, buttonHeight)),
        text='Back',
        manager=manager_hist)

    while True:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == buttonStartGame:
                        start_screen()
            manager_hist.process_events(event)

        manager_hist.update(time_delta)
        pygame.display.flip()
        manager_hist.draw_ui(screen)
        clock.tick(FPS)


def start_screen():
    manager_screen = pygame_gui.UIManager(SIZE)
    line = 'Tetris'

    fon = pygame.transform.scale(load_image('startScreenBackground.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))
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
        manager=manager_screen)

    buttonSettings = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(((SCREEN_WIDTH - buttonWidth) // 2, buttonTop + buttonHeight + buttonSpace),
                                  (buttonWidth, buttonHeight)),
        text='Settings',
        manager=manager_screen)

    buttonHistory = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(((SCREEN_WIDTH - buttonWidth) // 2, buttonTop + 2 * (buttonHeight + buttonSpace)),
                                  (buttonWidth, buttonHeight)),
        text='History',
        manager=manager_screen)

    buttonExit = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(((SCREEN_WIDTH - buttonWidth) // 2, buttonTop + 3 * (buttonHeight + buttonSpace)),
                                  (buttonWidth, buttonHeight)),
        text='Exit',
        manager=manager_screen)

    while True:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == buttonStartGame:
                        newGame()

                    if event.ui_element == buttonSettings:
                        print('Settings!')

                    if event.ui_element == buttonHistory:
                        write_history()

                    if event.ui_element == buttonExit:
                        terminate()

            manager_screen.process_events(event)

        manager_screen.update(time_delta)

        pygame.display.flip()
        manager_screen.draw_ui(screen)
        clock.tick(FPS)


def newGame():
    grid = Grid(W, H)

    f = Figure(figuresPos[randrange(len(figuresPos))])
    f.draw()

    while True:
        screen.fill('black')
        side = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            keyboard_keys = pygame.key.get_pressed()

            if keyboard_keys[pygame.K_LEFT]:
                side = 'left'

            elif keyboard_keys[pygame.K_RIGHT]:
                side = 'right'

            if keyboard_keys[pygame.K_DOWN]:
                side = 'down'

        if f.move:
            f.update(grid, side)
        else:
            f = Figure(figuresPos[randrange(len(figuresPos))])
            f.draw()
        grid.draw()
        grid.draw_grid()

        clock.tick(FPS)
        pygame.display.flip()


class Figure:
    imageFigure = load_image('alone_sqr.png')

    def __init__(self, structure):
        self.structure = structure
        self.spitesFigure = pygame.sprite.Group()
        self.move = True

        for pos in self.structure:
            dx, dy = pos
            sqr = pygame.sprite.Sprite(self.spitesFigure)
            sqr.image = Figure.imageFigure
            sqr.rect = sqr.image.get_rect()
            sqr.rect.x = W // 2 * scale + dx * scale
            sqr.rect.y = dy * scale

    def draw(self):
        self.spitesFigure.draw(screen)

    def update(self, *args, **kwargs) -> None:
        grid = args[0]
        side = args[1]
        self.collision(grid, side)
        if self.move:
            for spr in self.spitesFigure:
                spr.rect.y += 1
            self.draw()
        else:
            self.destruct(grid)

    def collision(self, grid, side):
        for spr in self.spitesFigure:
            x = spr.rect.x // scale
            y = spr.rect.y // scale + 1
            if y >= H or grid.field[y][x]:
                self.move = False
            if side == 'left' and spr.rect.x > 0:
                spr.rect.x -= scale
            elif side == 'right' and spr.rect.x < SCREEN_WIDTH // 4 + 60:
                spr.rect.x += scale
            if side == 'down' and spr.rect.y < SCREEN_HEIGHT:
                spr.rect.y += scale

    def destruct(self, grid):
        for spr in self.spitesFigure:
            x = spr.rect.x // scale
            y = spr.rect.y // scale
            grid.field[y][x] = 1
            grid.newSprite(spr)
        pprint(grid.field)


class Grid:
    def __init__(self, w, h):
        self.width = w
        self.height = h

        self.field = [[0] * w for i in range(h)]
        self.spritesSqr = pygame.sprite.Group()

    def draw(self):
        self.spritesSqr.draw(screen)

    def draw_grid(self):
        for i in range(H):
            for j in range(W):
                pygame.draw.rect(screen, pygame.Color("white"),
                                 (j * scale, i * scale, scale, scale), 1)

    def update(self):
        for y in range(self.height):
            for x in range(self.width):
                sqr = pygame.sprite.Sprite(self.spritesSqr)
                sqr.image = Figure.imageFigure
                sqr.rect = sqr.image.get_rect()
                sqr.rect.x = x * scale
                sqr.rect.y = y * scale

    def newSprite(self, sprite):
        self.spritesSqr.add(sprite)


start_screen()

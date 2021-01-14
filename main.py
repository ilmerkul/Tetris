import os
import sys
from random import randrange, choice
from CONSTANTS import *

pygame.init()
pygame.display.set_caption('Tetris')

clear_stage = pygame.mixer.Sound(music[0][2])
game_over = pygame.mixer.Sound(music[1][2])
main_menu = music[2][2]
game_music = music[3][2]


def terminate():
    pygame.quit()
    cur.close()
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
    fon = pygame.transform.scale(load_image
                                 (hist_backg),
                                 (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(fon, (0, 0))

    with open('data/history.txt', 'r', encoding='utf-8') as hist:
        file = [line.strip() for line in hist]
    font = pygame.font.Font(None, 21)

    for i in range(len(file)):
        text = font.render(file[i], True, pygame.Color('white'))
        text_x = SCREEN_WIDTH // 2 - text.get_width() // 2
        text_y = 5
        screen.blit(text, (text_x, text_y + 20 * i))

    buttonWidth = 100
    buttonHeight = 50
    buttonTop = 0
    buttonBackToStart = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((buttonTop, buttonTop),
                                  (buttonWidth, buttonHeight)),
        text='Back',
        manager=manager_hist)

    while True:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == buttonBackToStart:
                        start_screen()
            manager_hist.process_events(event)

        manager_hist.update(time_delta)
        pygame.display.flip()
        manager_hist.draw_ui(screen)
        clock.tick(FPS)


def start_screen():
    manager_screen = pygame_gui.UIManager(SIZE)
    line = 'Tetris'

    fon = pygame.transform.scale(load_image
                                 (start_backg),
                                 (SCREEN_WIDTH, SCREEN_HEIGHT))
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
        relative_rect=pygame.Rect(((SCREEN_WIDTH - buttonWidth) // 2,
                                   buttonTop),
                                  (buttonWidth, buttonHeight)),
        text='Start Game',
        manager=manager_screen)

    buttonSettings = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(((SCREEN_WIDTH - buttonWidth)
                                   // 2, buttonTop +
                                   buttonHeight + buttonSpace),
                                  (buttonWidth, buttonHeight)),
        text='Settings',
        manager=manager_screen)

    buttonHistory = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(((SCREEN_WIDTH - buttonWidth) // 2,
                                   buttonTop + 2 * (buttonHeight
                                                    + buttonSpace)),
                                  (buttonWidth, buttonHeight)),
        text='History',
        manager=manager_screen)

    buttonExit = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(((SCREEN_WIDTH - buttonWidth) // 2,
                                   buttonTop + 3 *
                                   (buttonHeight + buttonSpace)),
                                  (buttonWidth, buttonHeight)),
        text='Exit',
        manager=manager_screen)

    pygame.mixer.music.load(main_menu)
    pygame.mixer.music.play(-1)

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
                        ...

                    if event.ui_element == buttonHistory:
                        write_history()

                    if event.ui_element == buttonExit:
                        terminate()

            manager_screen.process_events(event)
        if not pygame.mixer.music.get_busy:
            pygame.mixer.music.load(main_menu)
            pygame.mixer.music.play(-1)
        manager_screen.update(time_delta)

        pygame.display.flip()
        manager_screen.draw_ui(screen)
        clock.tick(FPS)


def newGame():
    global SCORE, BEST_SCORE
    SCORE = 0
    grid = Grid(W, H, TOP, LEFT)

    pygame.mixer.music.load(game_music)
    pygame.mixer.music.play(-1)

    screen.fill('black')
    f = Figure(figuresPos[randrange(len(figuresPos))])
    f.draw()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            keyboard_keys = pygame.key.get_pressed()

            if keyboard_keys[pygame.K_LEFT]:
                side = -1
                f.moveHorizontal(side, grid)

            elif keyboard_keys[pygame.K_RIGHT]:
                side = 1
                f.moveHorizontal(side, grid)

            elif keyboard_keys[pygame.K_UP]:
                screen.fill('black')
                f.turn_figure(grid)

            if event.type == MOVE_FIGURE:
                screen.fill('black')
                if f.move:
                    f.update(grid)
                else:
                    f = Figure(figuresPos[randrange(len(figuresPos))])
                    f.draw()
            elif keyboard_keys[pygame.K_DOWN]:
                screen.fill('black')
                f.update(grid)
                if f.move:
                    SCORE += JUMPCOST
        grid.draw()
        grid.score(SCORE, BEST_SCORE)
        clock.tick(FPS)
        pygame.display.flip()


class Figure:
    imagesFigure = [load_image(sqr1),
                    load_image(sqr2),
                    load_image(sqr3)]

    def __init__(self, structure):
        self.structure = structure
        self.spitesFigure = pygame.sprite.Group()
        self.move = True
        img = choice(Figure.imagesFigure)

        for pos in self.structure:
            dx, dy = pos
            sqr = pygame.sprite.Sprite(self.spitesFigure)
            sqr.image = img
            sqr.rect = sqr.image.get_rect()
            sqr.rect.x = W // 2 * scale + dx * scale + LEFT
            sqr.rect.y = dy * scale + TOP

    def draw(self):
        self.spitesFigure.draw(screen)

    def turn_figure(self, grid):
        figure = []
        for spr in self.spitesFigure:
            figure.append(spr.rect)
        center = figure[0]
        on_board = 0
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            x1 = center.x - x
            y1 = center.y + y
            if (scale <= x1 + scale <= (W + 1) * scale and
                scale <= x1 <= (W + 1) * scale) and \
                    (scale <= y1 + scale <= (H + 1) * scale and
                     scale <= y1 <= (H + 1) * scale) and \
                    not grid.field[y1 // 30 - 1][x1 // 30 - 1]:
                on_board += 1
            else:
                break
        if on_board == 4:
            for i in range(4):
                x = figure[i].y - center.y
                y = figure[i].x - center.x
                figure[i].x = center.x - x
                figure[i].y = center.y + y
        self.spitesFigure.draw(screen)

    def moveHorizontal(self, side, grid):
        for spr in self.spitesFigure:
            x, y = (spr.rect.x - LEFT) // scale, \
                   (spr.rect.y - TOP) // scale
            if not (0 <= x + side < W) or grid.field[y][x + side]:
                return

        for spr in self.spitesFigure:
            spr.rect.x += scale * side
        screen.fill('black')
        self.draw()

    def update(self, grid):
        self.collision(grid)
        if self.move:
            for spr in self.spitesFigure:
                spr.rect.y += scale
            self.draw()
        else:
            self.destruct(grid)

    def collision(self, grid):
        global BEST_SCORE
        for spr in self.spitesFigure:
            x = (spr.rect.x - LEFT) // scale
            y = (spr.rect.y - TOP) // scale
            if y + 1 >= H or grid.field[y + 1][x]:
                self.move = False
                if y <= 0:
                    cur.execute(f"""INSERT INTO SCORES(score)
                     VALUES({SCORE})""").fetchall()
                    con.commit()
                    game_over.play()
                    BEST_SCORE = \
                        cur.execute(f"""SELECT MAX(score)
                         FROM SCORES""").fetchone()[0]
                    newGame()
                return

    def destruct(self, grid):
        for spr in self.spitesFigure:
            x = (spr.rect.x - LEFT) // scale
            y = (spr.rect.y - TOP) // scale
            grid.field[y][x] = 1
            grid.newSprite(spr)
        grid.update()


class Grid:
    def __init__(self, w, h, top, left):
        self.width = w
        self.height = h
        self.top = top
        self.left = left

        self.field = [[0] * w for _ in range(h)]
        self.spritesSqr = pygame.sprite.Group()

    def draw(self):
        for x in range(self.width):
            for y in range(self.height):
                pygame.draw.rect(screen, 'white', ((x * scale + self.left,
                                                    y * scale + self.top),
                                                   (scale, scale)),
                                 width=1)
        self.spritesSqr.draw(screen)

    def update(self):
        global SCORE
        lineCount = 0
        for y in range(self.height):
            if all(self.field[y]):
                self.field = [[0] * self.width] + self.field[:y] \
                             + self.field[y + 1:]

                coord = y * scale + TOP
                for spr in self.spritesSqr:
                    if spr.rect.y == coord:
                        self.spritesSqr.remove(spr)
                    elif spr.rect.y < coord:
                        spr.rect.y += scale
                lineCount += 1
        if lineCount:
            SCORE += LINECOST[lineCount - 1]
            clear_stage.play()
        screen.fill('black')
        self.draw()

    def newSprite(self, sprite):
        self.spritesSqr.add(sprite)

    def score(self, score, best_score):
        texts = ["SCORE", score, "BEST SCORE", best_score]
        for i in range(4):
            font = pygame.font.Font(None, 50)
            text = font.render(str(texts[i]), True,
                               pygame.Color('grey'))
            text_x = SCREEN_WIDTH // 2 + 100
            text_y = 200 + i * 50
            screen.blit(text, (text_x, text_y))


start_screen()

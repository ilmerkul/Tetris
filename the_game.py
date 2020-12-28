import os
import sys

import pygame

pygame.init()
pygame.display.set_caption('Tetris')
SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
FPS = 60
pygame.key.set_repeat(200, 70)

all_sprites = pygame.sprite.Group()
all_figures = pygame.sprite.Group()
all_borders = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_borders)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Figure(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_figures)
        self.image = load_image('alone_sqr.png')
        self.rect = self.image.get_rect()
        self.rect.size = 40, 40
        self.rect.x = 200
        self.rect.y = 0

    def update(self, *args, **kwargs) -> None:
        if pygame.sprite.groupcollide(
                all_figures, horizontal_borders, False, False):
            pass
        else:
            self.rect = self.rect.move(0, 2.5)
            if args[0] == 'left' and self.rect.x > 0:
                self.rect.x -= 40
            if args[0] == 'right' and self.rect.x < SCREEN_WIDTH // 2 - 41:
                self.rect.x += 40
            if args[0] == 'down' and self.rect.y < SCREEN_HEIGHT - 55:
                self.rect.y += 10
        if pygame.sprite.groupcollide(all_figures, vertical_borders, False, False):
            pass


Border(0, SCREEN_HEIGHT - 5, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 5)
Border(0, 0, 0, SCREEN_HEIGHT - 5)
Border(SCREEN_WIDTH // 2, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 5)


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


Figure()

while True:
    screen.fill('white')
    side = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        keyboard_keys = pygame.key.get_pressed()
        if keyboard_keys[pygame.K_LEFT]:
            side = 'left'
        elif keyboard_keys[pygame.K_RIGHT]:
            side = 'right'
        elif keyboard_keys[pygame.K_DOWN]:
            side = 'down'
    all_figures.draw(screen)
    all_borders.draw(screen)
    all_figures.update(side)
    clock.tick(FPS)
    pygame.display.flip()

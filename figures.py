import pygame

pygame.init()
size = WIDTH, HEIGHT = 260, 350
screen = pygame.display.set_mode(size)


def draw_smashboy():
    pygame.draw.rect(screen, pygame.Color('yellow'),
                     (10, 10, 25, 25), 0)
    pygame.draw.rect(screen, pygame.Color('yellow'),
                     (40, 10, 25, 25), 0)
    pygame.draw.rect(screen, pygame.Color('yellow'),
                     (10, 40, 25, 25), 0)
    pygame.draw.rect(screen, pygame.Color('yellow'),
                     (40, 40, 25, 25), 0)


def draw_line():
    pygame.draw.rect(screen, pygame.Color('turquoise'),
                     (10, 100, 25, 25))
    pygame.draw.rect(screen, pygame.Color('turquoise'),
                     (10, 130, 25, 25))
    pygame.draw.rect(screen, pygame.Color('turquoise'),
                     (10, 160, 25, 25))
    pygame.draw.rect(screen, pygame.Color('turquoise'),
                     (10, 190, 25, 25))


def draw_orange_ricky():
    pygame.draw.rect(screen, pygame.Color('orange'),
                     (100, 10, 25, 25))
    pygame.draw.rect(screen, pygame.Color('orange'),
                     (100, 40, 25, 25))
    pygame.draw.rect(screen, pygame.Color('orange'),
                     (100, 70, 25, 25))
    pygame.draw.rect(screen, pygame.Color('orange'),
                     (130, 70, 25, 25))


def draw_zig_zag_from_left():
    pygame.draw.rect(screen, pygame.Color('green'),
                     (100, 120, 25, 25))
    pygame.draw.rect(screen, pygame.Color('green'),
                     (100, 150, 25, 25))
    pygame.draw.rect(screen, pygame.Color('green'),
                     (130, 150, 25, 25))
    pygame.draw.rect(screen, pygame.Color('green'),
                     (130, 180, 25, 25))


def draw_blue_ricky():
    pygame.draw.rect(screen, pygame.Color('blue'),
                     (220, 10, 25, 25))
    pygame.draw.rect(screen, pygame.Color('blue'),
                     (220, 40, 25, 25))
    pygame.draw.rect(screen, pygame.Color('blue'),
                     (220, 70, 25, 25))
    pygame.draw.rect(screen, pygame.Color('blue'),
                     (190, 70, 25, 25))


def draw_zig_zag_from_right():
    pygame.draw.rect(screen, pygame.Color('red'),
                     (40, 250, 25, 25))
    pygame.draw.rect(screen, pygame.Color('red'),
                     (10, 280, 25, 25))
    pygame.draw.rect(screen, pygame.Color('red'),
                     (40, 280, 25, 25))
    pygame.draw.rect(screen, pygame.Color('red'),
                     (10, 310, 25, 25))


def draw_t_like():
    pygame.draw.rect(screen, pygame.Color('purple'),
                     (120, 250, 25, 25))
    pygame.draw.rect(screen, pygame.Color('purple'),
                     (120, 280, 25, 25))
    pygame.draw.rect(screen, pygame.Color('purple'),
                     (120, 310, 25, 25))
    pygame.draw.rect(screen, pygame.Color('purple'),
                     (150, 280, 25, 25))


running = True
draw_smashboy()  # квадрат, в левом верхнем углу
draw_line()  # линия, ниже квадрата
draw_orange_ricky()  # уголок вправо, справа от квадрата
draw_zig_zag_from_left()  # зиг заг слеве направо, справа от линии
draw_blue_ricky()  # уголок влево, справа от уголка вправо
draw_zig_zag_from_right()  # зиг заг справа налево, под линией
draw_t_like()  # т образная фигурка, под зигзагами

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
pygame.quit()

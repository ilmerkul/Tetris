import pygame
import pygame_gui

SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 650
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
manager = pygame_gui.UIManager(SIZE)
FPS = 60

SCORE = 0
BEST_SCORE = 0
LINECOST = [100, 300, 700, 1500]
JUMPCOST = 10


scale = 30
W, H = 10, 20
TOP = 30
LEFT = 30

figuresPos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
              [(0, -1), (-1, -1), (-1, 0), (0, 0)],
              [(-1, 0), (-1, 1), (0, 0), (0, -1)],
              [(0, 0), (-1, 0), (0, 1), (-1, -1)],
              [(0, 0), (0, -1), (0, 1), (-1, -1)],
              [(0, 0), (0, -1), (0, 1), (1, -1)],
              [(0, 0), (0, -1), (0, 1), (-1, 0)]]

MOVE_FIGURE = pygame.USEREVENT + 1

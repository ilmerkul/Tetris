import sqlite3
import pygame
import pygame_gui

SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 650
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
manager = pygame_gui.UIManager(SIZE)
FPS = 60

SCORE = 0
LINECOST = [100, 300, 700, 1500]
JUMPCOST = 10

scale = 30
W, H = 10, 20
TOP = 30
LEFT = 30

time_delta = clock.tick(60) / 1000.0

figuresPos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
              [(0, -1), (-1, -1), (-1, 0), (0, 0)],
              [(-1, 0), (-1, 1), (0, 0), (0, -1)],
              [(0, 0), (-1, 0), (0, 1), (-1, -1)],
              [(0, 0), (0, -1), (0, 1), (-1, -1)],
              [(0, 0), (0, -1), (0, 1), (1, -1)],
              [(0, 0), (0, -1), (0, 1), (-1, 0)]]

MOVE_FIGURE = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_FIGURE, 400)

db_name = "data/data bases/main_db.db"
con = sqlite3.connect(db_name)
cur = con.cursor()

music = cur.execute("SELECT * FROM SOUNDS").fetchall()
sprites_and_jpgs = cur.execute("SELECT * FROM SPRITES").fetchall()

BEST_SCORE = scores = cur.execute(f"SELECT MAX(score) FROM SCORES").fetchone()[0]

sprs = sprites_and_jpgs[:-3]
sprites = []
for i in range(0, len(sprs), 3):
    sprites.append((sprs[i][2], sprs[i + 1][2], sprs[i + 2][2]))
hist_backg = sprites_and_jpgs[-3][2]
start_backg = sprites_and_jpgs[-2][2]
settings_backg = sprites_and_jpgs[-1][2]



con.commit()

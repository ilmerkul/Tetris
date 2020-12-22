import pygame

pygame.init()
size = WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode(size)


class StartMenu:
    def __init__(self):
        for name in WORDS:
            pygame.draw.rect(screen, 'grey', (200, WORDS[name], 200, 50), 0, 5)
            font = pygame.font.Font(None, 50)
            text = font.render(f"{name}", True, (255, 255, 255))
            text_x = 200
            text_y = WORDS[name]
            screen.blit(text, (text_x + 7, text_y + 7))

    def game(self, event):
        Game().update(event)

    def history(self):
        pass

    def settings(self):
        pass

    def exit_program(self):
        exit()


class Settings:
    pass


class History:
    pass


class Game:
    def __init__(self):
        pass

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if (200 <= x <= 400) and (200 <= y <= 250):
                print('Start Game')
            if (200 <= x <= 400) and (260 <= y <= 310):
                print('Settings')
            if (200 <= x <= 400) and (320 <= y <= 370):
                print('Exit')


WORDS = {
    'Start Game': 200,
    'Settings': 260,
    'Exit': 320
}

StartMenu()

running = True
menu = StartMenu()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        menu.game(event)
    pygame.display.flip()
pygame.quit()

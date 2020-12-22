import pygame

if __name__ == '__main__':
    pygame.init()
    size = WIDTH, HEIGHT = 1620, 980
    screen = pygame.display.set_mode(size)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()

    pygame.quit()

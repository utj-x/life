import pygame
import random


class Settings:
    screen_width = 800
    screen_height = 600

    def __init__(self):
        raise AttributeError("Attempt to initialize an abstract class")


pygame.init()
screen = pygame.display.set_mode(
    (Settings.screen_width, Settings.screen_height)
    )
clock = pygame.time.Clock()

game_map = [
    [
        random.choice([0, 1]) for y in range(Settings.screen_height // 10)
    ]
    for x in range(Settings.screen_width // 10)
]

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill("white")

    for y in range(0, Settings.screen_height+1, 10):
        pygame.draw.line(screen, "black", (0, y), (Settings.screen_width, y))

    for x in range(0, Settings.screen_width+1, 10):
        pygame.draw.line(screen, "black", (x, 0), (x, Settings.screen_height))

    for x in range(Settings.screen_width // 10):
        for y in range(Settings.screen_height // 10):
            if game_map[x][y] == 1:
                pygame.draw.rect(screen, "black", (x * 10, y * 10, 10, 10))

    # do something here
    pygame.display.flip()
    clock.tick(60)


pygame.quit()

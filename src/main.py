import pygame
from pygame.locals import *
from start import draw_parallax_background

pygame.init()
screen = pygame.display.set_mode((600, 750))
pygame.display.set_caption('SkyDodo')
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    draw_parallax_background()  # Draw background from start.py
    pygame.display.update()
    clock.tick(60)

pygame.quit()

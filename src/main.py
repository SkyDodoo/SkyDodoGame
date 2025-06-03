# main.py
import pygame
from pygame.locals import *
from start import load_parallax, draw_parallax

# Init
pygame.init()
screen_width, screen_height = 600, 750
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('SkyDodo')
clock = pygame.time.Clock()

# Load parallax layers
layers = load_parallax(screen_width)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    draw_parallax(screen, layers)
    pygame.display.update()
    clock.tick(60)

pygame.quit()

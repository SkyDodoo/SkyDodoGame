import pygame
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((600, 750))
pygame.display.set_caption('SkyDodo')

running = True
while running:
    for  event in pygame.event.get():
        if event.type == QUIT:
            running = False

pygame.quit()

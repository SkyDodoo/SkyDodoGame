import pygame
from pygame.locals import *
import random

pygame.init()

screen_width, screen_height = 600, 750
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('SkyDodo')
clock = pygame.time.Clock()

#Class for Platforms
class Platform:
    def __init__(self, x, y, width=100, height=25):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.width, self.height))

def generate_platforms(num=8):
    platforms = []

    ground = Platform(x=0, y=screen_height - 20, width=screen_width, height=25)
    platforms.append(ground)

    platform_width = 110
    for i in range(num):
        x = random.randint(10, screen_width-platform_width)
        y = screen_height - i * 90
        platforms.append(Platform(x, y))
    return platforms

def scroll_platforms(platforms, scroll_amount):
    for p in platforms:
        p.y += scroll_amount

#delete platforms that are out of the screen and append new ones
def recycle_platforms(platforms):
    platform_width = 110
    platform_height = 25
    max_attempts = 10
    min_vertical_distance = 80

    for p in platforms[:]:
        if p.y > screen_height:
            platforms.remove(p)

            #try to search for a new position if something overlaps
            for i in range(max_attempts):
                new_x = random.randint(0, screen_width - platform_width -80)
                new_y = random.randint(-100, -10)
                if not is_too_close_vertically(new_y, platforms, min_vertical_distance) and \
                    not is_overlapping(new_x, new_y, platform_width, platform_height, platforms):
                    platforms.append(Platform(new_x, new_y, platform_width, platform_height))
                    break

#Checking if platforms are overlapping
def is_overlapping(new_x, new_y, width, height, platforms):
    for p in platforms:
        if (new_x < p.x + p.width and
            new_x + width > p.x and
            new_y < p.y + p.height and
            new_y + height > p.y):
            return True
    return False

def is_too_close_vertically(new_y, platforms, min_distance):
    for p in platforms:
        if abs(new_y - p.y) < min_distance:
            return True
    return False


platforms = generate_platforms()

running = True
scroll_speed = 2

while running:
    clock.tick(60)
    screen.fill((255,255,255))

    scroll_platforms(platforms, scroll_speed)
    recycle_platforms(platforms)

    for p in platforms:
        p.draw(screen)

    pygame.display.update()

    for  event in pygame.event.get():
        if event.type == QUIT:
            running = False

pygame.quit()

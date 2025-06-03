import pygame
import random

#Class for Platforms
class Platform:
    def __init__(self, x, y, width=100, height=25, moving=False, move_range=100, move_speed=2):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.moving = moving
        self.move_range = move_range
        self.move_speed = move_speed
        self.start_x = x
        self.direction = 1 #1 = right, -1 = left
        self.movement_delta = 0

    def update(self):
        if self.moving:
            old_x = self.x
            self.x += self.move_speed * self.direction
            self.movement_delta = self.x - old_x  # Bewegung speichern
            if self.x > self.start_x + self.move_range:
                self.direction = -1
            elif self.x < self.start_x:
                self.direction = 1
        else:
            self.movement_delta = 0

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.width, self.height))

def generate_platforms(screen_width, screen_height, num=8):
    platforms = []

    ground = Platform(x=0, y=screen_height - 20, width=screen_width, height=25, moving=False)
    platforms.append(ground)

    platform_width = 110
    for i in range(num):
        x = random.randint(10, screen_width - platform_width)
        y = screen_height - i * 90

        moving = True  # immer beweglich
        move_range = random.randint(50, 150)
        move_speed = random.randint(1, 3)

        platforms.append(Platform(x, y, platform_width, 25, moving, move_range, move_speed))
    return platforms

def scroll_platforms(platforms, scroll_amount):
    for p in platforms:
        p.y += scroll_amount
        p.update()

#delete platforms that are out of the screen and append new ones
def recycle_platforms(platforms, screen_width, screen_height):
    platform_width = 110
    platform_height = 25
    max_attempts = 10
    min_vertical_distance = 70
    max_vertical_distance = 90
    max_horizontal_distance = 120

    for p in platforms[:]:
        if p.y > screen_height:
            platforms.remove(p)

            for i in range(max_attempts):
                new_x = random.randint(0, screen_width - platform_width - 80)
                new_y = random.randint(-100, -10)
                if (not is_too_close_vertically(new_y, platforms, min_vertical_distance) and
                    not is_overlapping(new_x, new_y, platform_width, platform_height, platforms) and
                    is_within_max_horizontal_distance(new_x, platforms, max_horizontal_distance) and
                    is_within_max_vertical_distance(new_y, platforms, max_vertical_distance)
                ):
                    move_range = random.randint(50, 150)
                    move_speed = random.randint(1, 3)
                    platforms.append(Platform(new_x, new_y, platform_width, platform_height, True, move_range, move_speed))
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

def is_within_max_vertical_distance(new_y, platforms, max_distance):
    for p in platforms:
        if abs(new_y - p.y) > max_distance:
            return True
    return False

def is_within_max_horizontal_distance(new_x, platforms, max_distance):
    for p in platforms:
        p_center_x = p.x +  p.width / 2
        new_center_x = new_x + 110 / 2
        if abs(new_center_x - p_center_x) < max_distance:
            return True
    return False

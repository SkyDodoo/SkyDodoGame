import pygame
import random

platform_img = pygame.image.load("assets/images/platform.png")

#Class for Platforms
class Platform:
    def __init__(self, x, y, width=100, height=25, moving=False, move_range=100, move_speed=2, image=None, is_ground=False):
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
        self.image = image
        self.is_ground = is_ground

        if image:
            self.image = pygame.transform.scale(image, (self.width, self.height))

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
        #pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.width, self.height))
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.width, self.height))

        if self.y >= screen.get_height() - 30:
            ground_img = pygame.image.load("assets/images/ground_new.png").convert_alpha()
            ground_img = pygame.transform.scale(ground_img, (screen.get_width(), ground_img.get_height()))
            screen.blit(ground_img, (0, 750 - 80))

def generate_platforms(screen_width, screen_height, num=8):
    platforms = []

    ground = Platform(x=0, y=screen_height - 20, width=screen_width, height=25, moving=False)
    platforms.append(ground)

    platform_width = 100
    for i in range(num):
        x = random.randint(10, screen_width - platform_width)
        y = screen_height - i * 90

        platforms.append(Platform(x, y, platform_width, 25, image=platform_img))
    return platforms

def scroll_platforms(platforms, scroll_amount):
    for p in platforms:
        p.y += scroll_amount
        p.update()

#delete platforms that are out of the screen and append new ones
def recycle_platforms(platforms, screen_width, screen_height):
    platform_width = 100
    platform_height = 25
    max_attempts = 10
    min_vertical_distance = 50
    max_vertical_distance = 80
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
                    moving = random.random() > 0.8
                    if moving:
                        max_range_left = new_x
                        max_range_right = screen_width - (new_x + platform_width)

                        if max_range_left < 50 or max_range_right < 50:
                            move_range = random.randint(150, 300)
                        else:
                            move_range = int(min(max_range_left, max_range_right) * random.uniform(0.8, 1.0))
                    else:
                        move_range = 0

                    move_speed = random.randint(2, 4) if moving else 0

                    platforms.append(Platform(new_x, new_y, platform_width, platform_height, True, move_range, move_speed, image=platform_img))
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
        new_center_x = new_x + 100 / 2
        if abs(new_center_x - p_center_x) < max_distance:
            return True
    return False

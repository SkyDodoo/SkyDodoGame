import pygame
import os

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 750

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Image directory
IMAGE_DIR = os.path.join("assets", "images")

# Load and scale images
def load_image(filename):
    path = os.path.join(IMAGE_DIR, filename)
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, (SCREEN_WIDTH, image.get_height()))

# Load background layers
sky_img = load_image("blueback2.jpg")
clouds_img = load_image("clouds.png")

# Scroll positions
sky_y = 0
clouds_y = 0

# Scroll speeds
sky_speed = 0.2
clouds_speed = 0.5

# Draw a vertically looping background layer
def draw_layer(img, y):
    height = img.get_height()
    y = y % height
    screen.blit(img, (0, y - height))
    screen.blit(img, (0, y))

# Function to update and draw the parallax background
def draw_parallax_background():
    global sky_y, clouds_y
    sky_y += sky_speed
    clouds_y += clouds_speed

    draw_layer(sky_img, sky_y)
    draw_layer(clouds_img, clouds_y)

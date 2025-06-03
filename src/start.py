import pygame
import os
import random

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 750

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Parallax Sky with Non-Overlapping Clouds and Trees")
clock = pygame.time.Clock()

# Image directory
IMAGE_DIR = os.path.join("assets", "images")

# Load images
def load_image(filename):
    path = os.path.join(IMAGE_DIR, filename)
    return pygame.image.load(path).convert_alpha()

sky_img = pygame.transform.scale(load_image("blueback.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
cloud_img_original = load_image("clouds.png")
tree_img_original = load_image("tree.png")

# Sky scroll
sky_y = 0
sky_speed = 0.2

# Check for overlap
def check_overlap(new_rect, others):
    return any(new_rect.colliderect(
        pygame.Rect(o["x"], o["y"], o["image"].get_width(), o["image"].get_height())
    ) for o in others)

# Create a non-overlapping cloud
def create_cloud(existing_clouds, max_attempts=100, allow_on_screen=True):
    for _ in range(max_attempts):
        scale = random.uniform(0.4, 0.9)
        width = int(cloud_img_original.get_width() * scale)
        height = int(cloud_img_original.get_height() * scale)

        image = pygame.transform.scale(cloud_img_original, (width, height))
        if random.choice([True, False]):
            image = pygame.transform.flip(image, True, False)

        y = random.randint(0, SCREEN_HEIGHT // 2) if allow_on_screen and len(existing_clouds) < 3 else random.randint(-600, -100)
        x = random.randint(0, SCREEN_WIDTH - width)
        new_rect = pygame.Rect(x, y, width, height)

        if not check_overlap(new_rect, existing_clouds):
            return {"image": image, "x": x, "y": y, "speed": random.uniform(0.5, 2.5)}
    return None

# Create a falling tree
def create_tree():
    scale = random.uniform(0.3, 0.7)
    width = int(tree_img_original.get_width() * scale)
    height = int(tree_img_original.get_height() * scale)

    image = pygame.transform.scale(tree_img_original, (width, height))
    x = random.randint(0, SCREEN_WIDTH - width)
    y = random.randint(-800, -100)
    speed = random.uniform(1.5, 3.5)

    return {"image": image, "x": x, "y": y, "speed": speed}

# Initialize clouds and trees
clouds = []
trees = []

while len(clouds) < 5:
    cloud = create_cloud(clouds)
    if cloud:
        clouds.append(cloud)

while len(trees) < 5:
    trees.append(create_tree())

# Draw vertically looping sky background
def draw_layer(img, y):
    height = img.get_height()
    y = y % height
    screen.blit(img, (0, y - height))
    screen.blit(img, (0, y))

# Draw and update background with clouds and trees
def draw_parallax_background():
    global sky_y
    sky_y += sky_speed
    draw_layer(sky_img, sky_y)

    # Draw and update clouds
    for cloud in clouds[:]:
        cloud["y"] += cloud["speed"]
        screen.blit(cloud["image"], (cloud["x"], cloud["y"]))

        if cloud["y"] > SCREEN_HEIGHT:
            clouds.remove(cloud)
            new_cloud = create_cloud(clouds, allow_on_screen=False)
            if new_cloud:
                clouds.append(new_cloud)

    # Draw and update trees
    for tree in trees[:]:
        tree["y"] += tree["speed"]
        screen.blit(tree["image"], (tree["x"], tree["y"]))

        if tree["y"] > SCREEN_HEIGHT:
            trees.remove(tree)
            trees.append(create_tree())

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_parallax_background()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

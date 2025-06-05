import pygame
import os
import random
from typing import Optional, List, Dict, Any

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 750

# Assets
sky_img: Optional[pygame.Surface] = None
cloud_img_original: Optional[pygame.Surface] = None
fh_img: Optional[pygame.Surface] = None

# Background state
sky_y = 0
sky_speed = 0.2
clouds: List[Dict[str, Any]] = []

# Function: load_assets
# -------------------------------
# Loads and prepares all required image assets for the game.
# Sets global variables:
# - sky_img: background sky image, scaled to screen size
# - cloud_img_original: o
# riginal cloud layer image
# - fh_img: foreground hill or object image, scaled to fixed size
# Raises FileNotFoundError if any asset is missing.
# Asserts that all images are successfully loaded.

def load_assets():
    """Load and prepare all image assets."""
    global sky_img, cloud_img_original, fh_img

    base_dir = os.path.dirname(__file__)
    image_dir = os.path.join(base_dir, "..", "assets", "images")

    def load_image(name: str) -> pygame.Surface:
        path = os.path.join(image_dir, name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Image not found: {path}")
        return pygame.image.load(path).convert_alpha()

    sky_img = pygame.transform.scale(load_image("blueback.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
    cloud_img_original = load_image("clouds.png")
    original_fh = load_image("fh.png")
    fh_img = pygame.transform.scale(original_fh, (155, 67))

    assert sky_img and cloud_img_original and fh_img, "All images must be loaded."


# Function: reset_background
# -------------------------------
# Clears the current cloud list and regenerates cloud objects for the background.
# This helps reset the visual background when restarting or resetting the game.
#
# Globals modified:
# - clouds: list of cloud positions, cleared and re-filled.

def reset_background():
    """Clear and regenerate clouds for the background."""
    global clouds
    clouds.clear()
    for i in range(3):
        clouds.append(create_cloud(y=i * 100))


# Function: create_cloud
# y - Optional[int]: specific vertical position for the cloud (default: random above screen)
# -------------------------------
# Creates and returns a dictionary representing a cloud object with:
# - Random horizontal position
# - Random speed
# - Scaled and optionally flipped image
# Used to populate or reset background elements dynamically.

def create_cloud(y: Optional[int] = None) -> Dict[str, Any]:
    """Create a new cloud with random properties."""
    assert cloud_img_original is not None

    scale = random.uniform(0.4, 0.9)
    width = int(cloud_img_original.get_width() * scale)
    height = int(cloud_img_original.get_height() * scale)
    image = pygame.transform.scale(cloud_img_original, (width, height))

    if random.choice([True, False]):
        image = pygame.transform.flip(image, True, False)

    x = random.randint(0, SCREEN_WIDTH - width)
    y = y if y is not None else random.randint(-600, -100)

    return {"image": image, "x": x, "y": y, "speed": random.uniform(0.5, 2.5)}


# Function: draw_layer
# surface - pygame.Surface: the target surface to draw on (e.g., screen)
# img - pygame.Surface: the image to use as the scrolling layer
# y - float: vertical scroll offset
# ------------------------------------------------------------
# Draws a vertically scrolling image layer that wraps seamlessly.
# Useful for backgrounds like sky, parallax layers, etc.
# The image is drawn twice: once above and once at the current offset,
# creating a continuous scroll effect when the offset exceeds the image height.

def draw_layer(surface: pygame.Surface, img: pygame.Surface, y: float):
    """Draw a vertically scrolling layer that wraps."""
    height = img.get_height()
    y %= height
    surface.blit(img, (0, y - height))
    surface.blit(img, (0, y))


# Function: draw_background
# surface - pygame.Surface: the screen or surface to draw everything on
# ------------------------------------------------------------
# Draws the animated background, which includes:
# 1. A vertically scrolling sky layer.
# 2. Animated, randomly moving clouds that regenerate when off-screen.
# 3. A static image/logo ("fh.jpg") placed in the top-right corner.

def draw_background(surface: pygame.Surface):
    """Draw the animated background including sky, clouds, and static logo."""
    global sky_y
    assert sky_img is not None

    # Scroll the sky
    sky_y += sky_speed
    draw_layer(surface, sky_img, sky_y)

    # Move and draw clouds
    for cloud in clouds[:]:
        cloud["y"] += cloud["speed"]
        surface.blit(cloud["image"], (cloud["x"], cloud["y"]))
        if cloud["y"] > SCREEN_HEIGHT:
            clouds.remove(cloud)
            clouds.append(create_cloud())

    # Draw fh.jpg in the top-right corner
    if fh_img:
        fh_rect = fh_img.get_rect(topright=(SCREEN_WIDTH - 0, 0))
        surface.blit(fh_img, fh_rect)

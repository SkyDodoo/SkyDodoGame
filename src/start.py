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


def reset_background():
    """Clear and regenerate clouds for the background."""
    global clouds
    clouds.clear()
    for i in range(3):
        clouds.append(create_cloud(y=i * 100))


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


def draw_layer(surface: pygame.Surface, img: pygame.Surface, y: float):
    """Draw a vertically scrolling layer that wraps."""
    height = img.get_height()
    y %= height
    surface.blit(img, (0, y - height))
    surface.blit(img, (0, y))


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
        fh_rect = fh_img.get_rect(topright=(SCREEN_WIDTH - 5, 30))
        surface.blit(fh_img, fh_rect)

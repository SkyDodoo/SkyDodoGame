# src/start.py
import pygame
import os
import random
from typing import Optional, List, Dict, Any

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 750

# Assets (with type hints)
sky_img: Optional[pygame.Surface] = None
cloud_img_original: Optional[pygame.Surface] = None
tree_img_original: Optional[pygame.Surface] = None

# Background state
sky_y = 0
sky_speed = 0.2
clouds: List[Dict[str, Any]] = []
trees: List[Dict[str, Any]] = []


def load_assets():
    """Load and prepare image assets."""
    global sky_img, cloud_img_original, tree_img_original
    base_dir = os.path.dirname(__file__)
    image_dir = os.path.join(base_dir, "..", "assets", "images")

    def load_image(name: str) -> pygame.Surface:
        path = os.path.join(image_dir, name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Image not found: {path}")
        return pygame.image.load(path).convert_alpha()

    sky_img = pygame.transform.scale(load_image("blueback.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
    cloud_img_original = load_image("clouds.png")
    tree_img_original = load_image("tree.png")

    # Help IDEs know these are not None after this point
    assert sky_img is not None
    assert cloud_img_original is not None
    assert tree_img_original is not None


def reset_background():
    """Reset and randomly generate initial background objects."""
    global clouds, trees
    clouds.clear()
    trees.clear()

    while len(clouds) < 5:
        cloud = create_cloud(clouds)
        if cloud:
            clouds.append(cloud)
        else:
            break  # Could not place non-overlapping cloud

    while len(trees) < 5:
        trees.append(create_tree())


def check_overlap(new_rect: pygame.Rect, others: List[Dict[str, Any]]) -> bool:
    """Check if new_rect overlaps with any other object in the list."""
    return any(new_rect.colliderect(
        pygame.Rect(o["x"], o["y"], o["image"].get_width(), o["image"].get_height())
    ) for o in others)


def create_cloud(existing_clouds: List[Dict[str, Any]], max_attempts=100, allow_on_screen=True) -> Optional[Dict[str, Any]]:
    """Create a new cloud dictionary object."""
    assert cloud_img_original is not None, "Cloud image not loaded"

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

    print("[DEBUG] Could not place a cloud after", max_attempts, "attempts.")
    return None


def create_tree() -> Dict[str, Any]:
    """Create a new tree dictionary object."""
    assert tree_img_original is not None, "Tree image not loaded"

    scale = random.uniform(0.3, 0.7)
    width = int(tree_img_original.get_width() * scale)
    height = int(tree_img_original.get_height() * scale)
    image = pygame.transform.scale(tree_img_original, (width, height))

    x = random.randint(0, SCREEN_WIDTH - width)
    y = random.randint(-800, -100)
    speed = random.uniform(1.5, 3.5)

    return {"image": image, "x": x, "y": y, "speed": speed}


def draw_layer(surface: pygame.Surface, img: pygame.Surface, y: float):
    """Draw a scrolling layer that loops vertically."""
    height = img.get_height()
    y %= height
    surface.blit(img, (0, y - height))
    surface.blit(img, (0, y))


def draw_background(surface: pygame.Surface):
    """Draw the entire animated background (sky, clouds, trees)."""
    global sky_y
    assert sky_img is not None, "Sky image not loaded"

    sky_y += sky_speed
    draw_layer(surface, sky_img, sky_y)

    for cloud in clouds[:]:
        cloud["y"] += cloud["speed"]
        surface.blit(cloud["image"], (cloud["x"], cloud["y"]))
        if cloud["y"] > SCREEN_HEIGHT:
            clouds.remove(cloud)
            new_cloud = create_cloud(clouds, allow_on_screen=False)
            if new_cloud:
                clouds.append(new_cloud)

    for tree in trees[:]:
        tree["y"] += tree["speed"]
        surface.blit(tree["image"], (tree["x"], tree["y"]))
        if tree["y"] > SCREEN_HEIGHT:
            trees.remove(tree)
            trees.append(create_tree())

import pygame
import os
import random
from typing import Optional, List, Dict, Any

from src.player import Player

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 750

# Assets
sky_img: Optional[pygame.Surface] = None
cloud_img_original: Optional[pygame.Surface] = None
fh_img: Optional[pygame.Surface] = None
logo_img: Optional[pygame.Surface] = None

# Background state
sky_y = 0
sky_speed = 0.2
clouds: List[Dict[str, Any]] = []

# UI State
privacy_accepted = False
show_dev_info = False
show_privacy_popup = False
privacy_scroll_offset = 0

PRIVACY_TEXT = [
    "This game collects no personal data.",
    "By continuing, you agree to the gameplay terms.",
    "We do not track your activity or location.",
    "Cookies are not used in any part of this game.",
    "All rights reserved © 2025 SkyDodo Developers."
]

def load_assets():
    global sky_img, cloud_img_original, fh_img, logo_img

    base_dir = os.path.dirname(__file__)
    image_dir = os.path.join(base_dir, "..", "assets", "images")

    def load_image(name: str) -> pygame.Surface:
        path = os.path.join(image_dir, name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Image not found: {path}")
        return pygame.image.load(path).convert_alpha()

    sky_img = pygame.transform.scale(load_image("blueback.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
    cloud_img_original = load_image("clouds.png")
    fh_img = pygame.transform.scale(load_image("fh.png"), (155, 67))
    logo_img = pygame.transform.smoothscale(load_image("logo.webp"), (250, 180))

    assert sky_img and cloud_img_original and fh_img and logo_img, "All images must be loaded."

def reset_background():
    global clouds
    clouds.clear()
    for i in range(3):
        clouds.append(create_cloud(y=i * 100))

def create_cloud(y: Optional[int] = None) -> Dict[str, Any]:
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
    height = img.get_height()
    y %= height
    surface.blit(img, (0, y - height))
    surface.blit(img, (0, y))

def draw_background(surface: pygame.Surface):
    global sky_y
    assert sky_img is not None

    sky_y += sky_speed
    draw_layer(surface, sky_img, sky_y)

    for cloud in clouds[:]:
        cloud["y"] += cloud["speed"]
        surface.blit(cloud["image"], (cloud["x"], cloud["y"]))
        if cloud["y"] > SCREEN_HEIGHT:
            clouds.remove(cloud)
            clouds.append(create_cloud())

    if fh_img:
        fh_rect = fh_img.get_rect(topright=(SCREEN_WIDTH - 0, 0))
        surface.blit(fh_img, fh_rect)

def draw_button(surface, font, text, x, y, width, height):
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, (70, 130, 180), rect, border_radius=10)
    label = font.render(text, True, (255, 255, 255))
    label_rect = label.get_rect(center=rect.center)
    surface.blit(label, label_rect)
    return rect

def draw_overlay_ui(surface: pygame.Surface):
    global privacy_accepted, show_dev_info, show_privacy_popup, privacy_scroll_offset

    font = pygame.font.SysFont("Arial", 20)
    checkbox_rect = pygame.Rect(40, SCREEN_HEIGHT - 60, 20, 20)
    pygame.draw.rect(surface, (0, 0, 0), checkbox_rect, 2)
    if privacy_accepted:
        pygame.draw.line(surface, (0, 0, 0), checkbox_rect.topleft, checkbox_rect.bottomright, 2)
        pygame.draw.line(surface, (0, 0, 0), checkbox_rect.topright, checkbox_rect.bottomleft, 2)
    surface.blit(font.render("Accept Privacy Policy", True, (0, 0, 0)), (70, SCREEN_HEIGHT - 62))

    info_icon = pygame.Rect(SCREEN_WIDTH - 40, SCREEN_HEIGHT - 40, 25, 25)
    pygame.draw.circle(surface, (50, 50, 255), info_icon.center, 12)
    surface.blit(font.render("i", True, (255, 255, 255)), (info_icon.x + 7, info_icon.y))

    if show_dev_info:
        info_lines = [
            "👨‍💻 Developer Info:",
            "SkyDodo Developers",
            "- GitHub https://github.com/SkyDodoo/SkyDodoGame.git"
        ]
        pygame.draw.rect(surface, (240, 240, 240), (40, 100, 520, 120))
        for i, line in enumerate(info_lines):
            surface.blit(font.render(line, True, (0, 0, 0)), (60, 110 + i * 25))

    if show_privacy_popup:
        popup = pygame.Rect(60, 120, 480, 400)
        pygame.draw.rect(surface, (255, 255, 255), popup)
        pygame.draw.rect(surface, (0, 0, 0), popup, 2)
        for i, line in enumerate(PRIVACY_TEXT):
            surface.blit(font.render(line, True, (0, 0, 0)), (popup.x + 10, popup.y + 10 + i * 30))
        close_btn = pygame.Rect(popup.right - 30, popup.y + 10, 20, 20)
        pygame.draw.rect(surface, (200, 50, 50), close_btn)
        surface.blit(font.render("X", True, (255, 255, 255)), (close_btn.x + 3, close_btn.y - 3))
        return close_btn
    return None

def fade_out(surface: pygame.Surface, speed: int = 10):
    fade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade.fill((0, 0, 0))
    for alpha in range(0, 255, speed):
        fade.set_alpha(alpha)
        draw_background(surface)
        draw_overlay_ui(surface)
        surface.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(30)

def start_menu_loop():
    global privacy_accepted, show_dev_info, show_privacy_popup

    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("SkyDodo")
    pygame.mixer.music.load("assets/sounds/background_music.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 36)

    load_assets()
    reset_background()

    player = Player(x=0, y=0)

    running = True
    while running:
        dt = clock.tick(60) / 1000
        screen.fill((0, 0, 0))
        draw_background(screen)

        logo_rect = logo_img.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(logo_img, logo_rect)

        player.y = logo_rect.bottom + 100
        player.x += player.speed
        player.direction = "fly"
        if player.x > SCREEN_WIDTH:
            player.x = -player.width
        player.update(dt)
        player.draw(screen)

        button_y = player.y + player.height + 100
        start_btn = draw_button(screen, font, "Start Game", 200, button_y, 200, 60)
        exit_btn = draw_button(screen, font, "Exit", 200, button_y + 90, 200, 60)

        close_rect = draw_overlay_ui(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = event.pos
                checkbox_rect = pygame.Rect(40, SCREEN_HEIGHT - 60, 20, 20)
                info_icon_rect = pygame.Rect(SCREEN_WIDTH - 40, SCREEN_HEIGHT - 40, 25, 25)

                if close_rect and close_rect.collidepoint(mouse):
                    show_privacy_popup = False
                elif info_icon_rect.collidepoint(mouse):
                    show_privacy_popup = True
                elif checkbox_rect.collidepoint(mouse):
                    privacy_accepted = not privacy_accepted
                elif start_btn.collidepoint(mouse) and privacy_accepted:
                    fade_out(screen)
                    from src.game import run_game
                    run_game()
                    running = False
                elif exit_btn.collidepoint(mouse):
                    running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    show_dev_info = not show_dev_info

    pygame.quit()

if __name__ == "__main__":
    start_menu_loop()

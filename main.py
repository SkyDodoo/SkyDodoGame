# main.py
import pygame
import sys
import os

import src.start  # background module
from src.game import run_game
from src.player import Player  # Player class

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen settings
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 750
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("SkyDodo")

# Load background music
pygame.mixer.music.load("assets/sounds/background_music.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)  # Loop forever

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 36)

# Load background
src.start.load_assets()
src.start.reset_background()

# Load and scale logo
logo_path = os.path.join("assets", "images", "logo.webp")
logo_img_original = pygame.image.load(logo_path).convert_alpha()
logo_img = pygame.transform.smoothscale(logo_img_original, (250, 180))


def draw_button(text, x, y, width, height):
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, (70, 130, 180), rect, border_radius=10)
    label = font.render(text, True, (255, 255, 255))
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)
    return rect


def main_menu():
    running = True

    # Create player instance, x = 0, y to be adjusted dynamically
    player = Player(x=0, y=0)

    while running:
        dt = clock.tick(60) / 1000  # Time since last frame in seconds

        # Draw background
        screen.fill((0, 0, 0))
        src.start.draw_background(screen)

        # Draw logo centered near top
        logo_rect = logo_img.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(logo_img, logo_rect)

        # Position player between logo and buttons
        player.y = logo_rect.bottom + 100
        player.x += player.speed
        player.direction = "fly"
        if player.x > SCREEN_WIDTH:
            player.x = -player.width
        player.update(dt)
        player.draw(screen)

        # Draw buttons below player
        button_y = player.y + player.height + 100
        start_btn = draw_button("Start Game", 200, button_y, 200, 60)
        exit_btn = draw_button("Exit", 200, button_y + 90, 200, 60)

        # Display everything
        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.collidepoint(event.pos):
                    run_game()
                elif exit_btn.collidepoint(event.pos):
                    running = False

    pygame.quit()
    sys.exit()


# Start the menu
main_menu()

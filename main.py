# main.py
import pygame
import sys
import src.start  # background module
from src.game import run_game
import os

pygame.init()
pygame.mixer.init()

# Background music
pygame.mixer.music.load("./assets/sounds/music.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)  # endless loop

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 750
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('SkyDodo')

font = pygame.font.SysFont("Arial", 36)
clock = pygame.time.Clock()

# Initialize background assets
src.start.load_assets()
src.start.reset_background()

# Load and scale logo image
logo_path = os.path.join("assets", "images", "logo.webp")
logo_img_original = pygame.image.load(logo_path).convert_alpha()

# Set your desired logo size here
LOGO_WIDTH = 250
LOGO_HEIGHT = 200
logo_img = pygame.transform.smoothscale(logo_img_original, (LOGO_WIDTH, LOGO_HEIGHT))


def draw_button(text, x, y, width, height):
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, (70, 130, 180), rect)
    label = font.render(text, True, (255, 255, 255))
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)
    return rect


def main_menu():
    running = True
    while running:
        screen.fill((0, 0, 0))
        src.start.draw_background(screen)

        # Draw resized logo and position it
        logo_rect = logo_img.get_rect(center=(SCREEN_WIDTH // 2, 180))
        screen.blit(logo_img, logo_rect)

        # Adjusted: increase spacing to move buttons lower
        spacing_from_logo = 60  # Increased from 20 to 60
        spacing_between_buttons = 90  # Increased from 80 to 90

        start_btn = draw_button("Start Game", 200, logo_rect.bottom + spacing_from_logo, 200, 60)
        exit_btn = draw_button("Exit", 200, logo_rect.bottom + spacing_from_logo + spacing_between_buttons, 200, 60)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.collidepoint(event.pos):
                    run_game()
                elif exit_btn.collidepoint(event.pos):
                    running = False

        clock.tick(60)

    pygame.quit()
    sys.exit()



main_menu()

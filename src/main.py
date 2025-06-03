# main.py
import pygame
import sys
from src import start  # background module

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 750
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('SkyDodo')

font = pygame.font.SysFont("Arial", 36)
clock = pygame.time.Clock()

# Initialize background assets
start.load_assets()
start.reset_background()

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
        start.draw_background(screen)

        title = font.render("SkyDodo", True, (255, 255, 255))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 120))

        start_btn = draw_button("Start Game", 200, 300, 200, 60)
        exit_btn = draw_button("Exit", 200, 400, 200, 60)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.collidepoint(event.pos):
                    print("Start Game clicked (hook up game here)")
                elif exit_btn.collidepoint(event.pos):
                    running = False

        clock.tick(60)

    pygame.quit()
    sys.exit()

main_menu()

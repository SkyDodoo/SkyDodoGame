# src/game.py
import pygame
from player import Player
from game_platform import generate_platforms, scroll_platforms, recycle_platforms
from start import draw_background

def run_game():
    pygame.init()
    screen_width, screen_height = 600, 750
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    player = Player(300, screen_height - 150)
    platforms = generate_platforms()
    font = pygame.font.SysFont("Arial", 24)

    running = True
    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        player.move(keys, screen_width)
        player.apply_gravity()
        player.update(dt)

        # Scroll screen if player high
        if player.y < screen_height // 3:
            scroll = screen_height // 3 - player.y
            player.y = screen_height // 3
            scroll_platforms(platforms, scroll)
            recycle_platforms(platforms)

        # Collision
        player_rect = player.get_rect()
        for p in platforms:
            plat_rect = pygame.Rect(p.x, p.y, p.width, p.height)
            if player.vel_y > 0 and player_rect.colliderect(plat_rect):
                if player_rect.bottom <= plat_rect.bottom + 10:
                    player.y = p.y - player.height
                    player.vel_y = 0
                    player.is_jumping = False

        draw_background(screen)
        for p in platforms:
            p.draw(screen)
        player.draw(screen)

        pygame.display.update()

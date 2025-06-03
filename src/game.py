# src/game.py
import pygame
from src.player import Player
from src.game_platform import generate_platforms, scroll_platforms, recycle_platforms
from src.start import draw_background

def run_game():
    pygame.init()
    screen_width, screen_height = 600, 750
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    player = Player(300, screen_height - 150)
    platforms = generate_platforms(screen_width, screen_height)
    font = pygame.font.SysFont("Arial", 24)

    back_button_rect = pygame.Rect(screen_width - 110, 10, 100, 40)  # top-right
    start_time = pygame.time.get_ticks()  # Timer starts

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not player.is_jumping:
                    player.jump()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):
                    return  # Back to main menu

        keys = pygame.key.get_pressed()
        player.move(keys, screen_width)
        player.apply_gravity()

        if player.y < screen_height // 3:
            scroll = screen_height // 3 - player.y
            player.y = screen_height // 3
            scroll_platforms(platforms, scroll)
            recycle_platforms(platforms, screen_width, screen_height)

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

        # Draw back button
        pygame.draw.rect(screen, (200, 50, 50), back_button_rect, border_radius=8)
        back_text = font.render("Back", True, (255, 255, 255))
        back_text_rect = back_text.get_rect(center=back_button_rect.center)
        screen.blit(back_text, back_text_rect)

        # Draw MM:SS timer with blue background
        elapsed_ms = pygame.time.get_ticks() - start_time
        minutes = elapsed_ms // 60000
        seconds = (elapsed_ms % 60000) // 1000
        timer_str = f"{minutes:02}:{seconds:02}"

        timer_text = font.render(timer_str, True, (255, 255, 255))
        timer_bg_rect = pygame.Rect(10, 10, 80, 40)  # background box
        pygame.draw.rect(screen, (70, 130, 180), timer_bg_rect, border_radius=8)
        text_rect = timer_text.get_rect(center=timer_bg_rect.center)
        screen.blit(timer_text, text_rect)

        pygame.display.update()



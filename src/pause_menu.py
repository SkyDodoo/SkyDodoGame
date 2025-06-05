

# pause_menu.py
# ---------------------------------
# Pause menu rendering and interaction handler

def show_pause_menu(screen, screen_width, screen_height, pause_font ):
    import pygame
    clock = pygame.time.Clock()
    running = True

    btn_font = pygame.font.SysFont("Arial", 32)
    resume_btn = pygame.Rect(screen_width // 2 - 100, 300, 200, 50)
    quit_btn = pygame.Rect(screen_width // 2 - 100, 380, 200, 50)

    while running:

        # Dim overlay
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        screen.blit(overlay, (0, 0))

        # Title text
        title = pause_font.render("Game Paused", True, (0, 0, 139))
        screen.blit(title, (screen_width // 2 - title.get_width() // 2, 150))

        # Draw buttons
        pygame.draw.rect(screen, (100, 200, 100), resume_btn, border_radius=12)
        pygame.draw.rect(screen, (200, 80, 80), quit_btn, border_radius=12)

        screen.blit(btn_font.render("▶ Resume", True, (255, 255, 255)), (resume_btn.x + 40, resume_btn.y + 10))
        screen.blit(btn_font.render("⏻ Quit", True, (255, 255, 255)), (quit_btn.x + 60, quit_btn.y + 10))

        pygame.display.update()

        # Handle pause menu events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if resume_btn.collidepoint(event.pos):
                    return False  # Resume the game
                elif quit_btn.collidepoint(event.pos):
                    pygame.quit()
                    exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False  # Resume the game with ESC

        clock.tick(60)
    return None

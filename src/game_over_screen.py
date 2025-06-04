# game_over_screen.py
# ---------------------------------
# Game Over screen display logic

def show_game_over(screen, font, score, bg_layers, scroll_offsets, scroll_speeds, save_high_score_func, load_high_score_func, run_game_func, player):
    import pygame
    clock = pygame.time.Clock()
    running = True
    high_score = load_high_score_func()
    if score > high_score:
        save_high_score_func(score)
        high_score = score

    title_font = pygame.font.SysFont("Comic Sans MS", 64, bold=True)
    score_font = pygame.font.SysFont("Comic Sans MS", 32)
    hint_font = pygame.font.SysFont("Comic Sans MS", 24)

    blink = True
    blink_timer = 0
    while running:
        # Animated background
        # screen_height = screen.get_height()
        # for i, layer in enumerate(bg_layers):
        #     scroll_offsets[i] = (scroll_offsets[i] + scroll_speeds[i]) % screen_height
        #     y = -scroll_offsets[i]
        #     screen.blit(layer, (0, y))
        #     screen.blit(layer, (0, y + screen_height))

        # Light blue transparent overlay
        blue_overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        screen.blit(blue_overlay, (0, 0))

        # Title
        title = title_font.render("GAME OVER", True, (255, 0, 0))
        shadow = title_font.render("GAME OVER", True, (0, 0, 0))
        title_x = screen.get_width() // 2 - title.get_width() // 2
        screen.blit(shadow, (title_x + 2, 102))
        if blink:
            screen.blit(title, (title_x, 100))

        # Scores
        score_text = score_font.render(f"Score: {score}", True, (0, 0, 0))
        high_score_text = score_font.render(f"High Score: {high_score}", True, (20, 40, 200))
        screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, 200))
        screen.blit(high_score_text, (screen.get_width() // 2 - high_score_text.get_width() // 2, 240))

        # Hint
        hint = hint_font.render("Press SPACE to Retry or ESC to Quit", True, (80, 80, 80))
        screen.blit(hint, (screen.get_width() // 2 - hint.get_width() // 2, 300))

        blink_timer += clock.get_time()
        if blink_timer > 500:
            blink = not blink
            blink_timer = 0

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return run_game_func()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

        clock.tick(60)
    return None

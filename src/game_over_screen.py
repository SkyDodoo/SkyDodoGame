# game_over_screen.py
# ---------------------------------
# Game Over screen display logic

# Method: show_game_over
# screen - Pygame screen surface to draw the game over screen on
# font - default font object for drawing text
# score - player's final score
# bg_layers - list of background layers (can be used for animation)
# scroll_offsets - vertical scroll position for each background layer
# scroll_speeds - speed at which each background layer scrolls
# save_high_score_func - function to save a new high score
# load_high_score_func - function to load the current high score
# run_game_func - function to restart the game
# player - reference to the player object (currently unused)
# -------------------------------------------------------------
# Displays the game over screen with title, current score, high score,
# and a blinking "GAME OVER" title.
# Offers the option to retry (SPACE) or quit (ESC).
# High score is updated and saved if the player beats it.
def show_game_over(screen, font, score, bg_layers, scroll_offsets, scroll_speeds, save_high_score_func, load_high_score_func, run_game_func, player):
    import pygame
    clock = pygame.time.Clock()
    running = True

    # Load and update high score if current score is higher
    high_score = load_high_score_func()
    if score > high_score:
        save_high_score_func(score)
        high_score = score

    # Fonts for title, score, and hints
    title_font = pygame.font.SysFont("Comic Sans MS", 64, bold=True)
    score_font = pygame.font.SysFont("Comic Sans MS", 32)
    hint_font = pygame.font.SysFont("Comic Sans MS", 24)

    blink = True # Controls blinking of "GAME OVER"
    blink_timer = 0 # Timer to toggle blinking

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

        # Draw blinking "GAME OVER" title with shadow
        title = title_font.render("GAME OVER", True, (255, 0, 0))
        shadow = title_font.render("GAME OVER", True, (0, 0, 0))
        title_x = screen.get_width() // 2 - title.get_width() // 2
        screen.blit(shadow, (title_x + 2, 102))
        if blink:
            screen.blit(title, (title_x, 100))

        # Draw current and high scores
        score_text = score_font.render(f"Score: {score}", True, (0, 0, 0))
        high_score_text = score_font.render(f"High Score: {high_score}", True, (20, 40, 200))
        screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, 200))
        screen.blit(high_score_text, (screen.get_width() // 2 - high_score_text.get_width() // 2, 240))

        # Show hint to the user
        hint = hint_font.render("Press SPACE to Retry or ESC to Quit", True, (80, 80, 80))
        screen.blit(hint, (screen.get_width() // 2 - hint.get_width() // 2, 300))

        # Update blink timer
        blink_timer += clock.get_time()
        if blink_timer > 500:
            blink = not blink
            blink_timer = 0

        pygame.display.flip()

        # Handle input events
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

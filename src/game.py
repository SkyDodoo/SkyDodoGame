# game_loop.py
# ---------------------------------
# Main game loop and core logic
from src.game_over_screen import show_game_over
from src.score_utils import save_high_score, load_high_score


def run_game():
    import pygame
    from random import randint
    from src.player import Player
    from src.game_platform import generate_platforms, scroll_platforms, recycle_platforms
    from src.start import draw_background
    from src.pause_menu import show_pause_menu
    from src.enemy_logic import spawn_enemies

    pygame.init()
    pygame.mixer.init()
    screen_width, screen_height = 600, 750
    screen = pygame.display.set_mode((screen_width, screen_height))

    bg_layers = [
        pygame.image.load("assets/images/Nature Landscapes Free Pixel Art/nature_1/orig.png").convert_alpha()
    ]
    scroll_offsets = [0 for _ in bg_layers]
    scroll_speeds = [0.2, 0.4, 0.6, 0.8, 1.2]

    clock = pygame.time.Clock()
    pygame.mixer.music.load("assets/sounds/background_music.mp3")
    pygame.mixer.music.play(-1)
    jump_sound = pygame.mixer.Sound('./assets/sounds/jump_sound.wav')
    game_over_sound = pygame.mixer.Sound("assets/sounds/gameover.wav")

    font = pygame.font.SysFont("Arial", 24)
    pause_font = pygame.font.SysFont("Arial", 48)
    notif_font = pygame.font.SysFont("Arial", 24)

    player = Player(300, screen_height - 150)
    platforms = generate_platforms(screen_width, screen_height)
    enemies = spawn_enemies(3, screen_width, screen_height, screen, platforms)

    pause_icon = pygame.image.load("assets/images/pause_btn.svg").convert_alpha()
    info_icon = pygame.image.load("assets/images/info_btn.svg").convert_alpha()
    pause_icon = pygame.transform.scale(pause_icon, (40, 40))
    info_icon = pygame.transform.scale(info_icon, (40, 40))
    pause_rect = pause_icon.get_rect(topleft=(screen_width - 50, 60))
    info_rect = info_icon.get_rect(topleft=(screen_width - 100, 60))

    paused = False
    show_info = False
    start_y = player.y
    max_height = 0
    notif_timer = 0
    notif_message = ""

    running = True
    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif not paused and event.type == pygame.MOUSEBUTTONDOWN:
                if pause_rect.collidepoint(event.pos):
                    paused = True
                elif info_rect.collidepoint(event.pos):
                    show_info = not show_info
            elif not paused and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not player.is_jumping:
                    player.jump()
                    jump_sound.play()

        if paused:
            paused = show_pause_menu(screen, screen_width, screen_height, pause_font, bg_layers, scroll_offsets, scroll_speeds)
            continue

        keys = pygame.key.get_pressed()
        player.move(keys, screen_width)
        player.apply_gravity()
        player.update(dt)

        for p in platforms:
            p.update()

        height_climbed = int(start_y - player.y)
        if height_climbed > max_height:
            max_height = height_climbed

        difficulty_level = max_height // 300

        if player.y < screen_height // 3:
            scroll = screen_height // 3 - player.y
            player.y = screen_height // 3
            scroll_platforms(platforms, scroll)
            recycle_platforms(platforms, screen_width, screen_height)
            for enemy in enemies:
                enemy.rect.y += scroll
                if enemy.rect.y > screen_height:
                    enemy.rect.y = -50
                    enemy.rect.x = randint(50, screen_width - 100)

        player_rect = player.get_rect()
        for p in platforms:
            plat_rect = pygame.Rect(p.x, p.y, p.width, p.height)
            if player.vel_y > 0 and player_rect.colliderect(plat_rect):
                if player_rect.bottom <= plat_rect.bottom + 10:
                    player.y = p.y - player.height
                    player.vel_y = 0
                    player.is_jumping = False

        for enemy in enemies:
            if player.get_rect().colliderect(enemy.rect):
                game_over_sound.play()
                pygame.mixer.music.stop()
                return show_game_over(
                screen, font, max_height,
                bg_layers, scroll_offsets, scroll_speeds,
                save_high_score,
                load_high_score,
                run_game,
                player
                )
        danger_nearby = any(abs(enemy.rect.y - player.y) < 150 for enemy in enemies)
        if danger_nearby:
            notif_message = "⚠ Enemy nearby!"
            notif_timer = pygame.time.get_ticks()

        draw_background(screen)
        for platform in platforms:
            platform.draw(screen)
        for enemy in enemies:
            enemy.update()
            screen.blit(enemy.image, enemy.rect)
        player.draw(screen)

        if show_info:
            pygame.draw.rect(screen, (240, 240, 240), (50, 200, 500, 300))
            info_lines = [
                "🎮 SkyDodo Instructions:",
                "- SPACE to jump",
                "- Avoid red enemies",
                "- Reach the sky!",
                "",
                "Click 'i' to hide this panel."
            ]
            for i, line in enumerate(info_lines):
                screen.blit(font.render(line, True, (0, 0, 0)), (70, 220 + i * 30))

        if notif_message and pygame.time.get_ticks() - notif_timer < 2000:
            notif_bg = pygame.Surface((300, 40), pygame.SRCALPHA)
            notif_bg.fill((0, 0, 0, 180))
            notif_text = notif_font.render(notif_message, True, (255, 200, 200))
            notif_bg_rect = notif_bg.get_rect(center=(screen_width // 2, 40))
            screen.blit(notif_bg, notif_bg_rect)
            screen.blit(notif_text, (notif_bg_rect.centerx - notif_text.get_width() // 2,
                                     notif_bg_rect.centery - notif_text.get_height() // 2))
        elif notif_message:
            notif_message = ""

        screen.blit(font.render(f"Score: {max_height}", True, (0, 0, 0)), (10, 10))
        screen.blit(font.render(f"Lvl: {difficulty_level + 1}", True, (0, 0, 0)), (10, 40))
        screen.blit(pause_icon, pause_rect)
        screen.blit(info_icon, info_rect)

        if player.y > screen_height:
            pygame.mixer.music.stop()
            game_over_sound.play()
            return max_height

        pygame.display.update()
    return None
# game_loop.py
# ---------------------------------
# Main game loop and core logic

import pygame
from random import randint
from src.settings import load_settings, save_settings

from src.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    PLAYER_START_X, PLAYER_START_Y,
    BACKGROUND_IMAGE, PAUSE_ICON_PATH, INFO_ICON_PATH, VOLUME_ICON_PATH, ICON_SIZE,
    PAUSE_BTN_POS, INFO_BTN_POS,
    MUSIC_PATH, JUMP_SOUND_PATH, GAME_OVER_SOUND_PATH,
    SCROLL_TRIGGER_Y, MAX_PLATFORM_DISTANCE,
    INFO_BOX_RECT, INFO_TEXT_COLOR, INFO_BG_COLOR,
    SCORE_POS, LEVEL_POS, SCORE_TEXT_COLOR, INFO_LINES
)
from src.player import Player
from src.game_platform import generate_platforms, scroll_platforms, recycle_platforms
from src.start import draw_background
from src.pause_menu import show_pause_menu
from src.enemy_logic import spawn_enemies
from src.score_utils import save_high_score, load_high_score
from src.game_over_screen import show_game_over

def run_game(scroll_offset=None):
    if scroll_offset is None:
        scroll_offset = 0

    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Background setup
    bg_layers = [pygame.image.load(BACKGROUND_IMAGE).convert_alpha()]
    scroll_offsets = [0 for _ in bg_layers]
    scroll_speeds = [0.2, 0.4, 0.6, 0.8, 1.2]

    # Load audio
    pygame.mixer.music.load(MUSIC_PATH)
    jump_sound = pygame.mixer.Sound(JUMP_SOUND_PATH)
    game_over_sound = pygame.mixer.Sound(GAME_OVER_SOUND_PATH)

    # Load saved volume
    settings = load_settings()
    volume = settings.get("volume", 0.5)

    pygame.mixer.music.set_volume(volume)
    jump_sound.set_volume(volume)
    game_over_sound.set_volume(volume)
    pygame.mixer.music.play(-1)

    # Fonts
    font = pygame.font.SysFont("Arial", 24)
    pause_font = pygame.font.SysFont("Arial", 48)

    # Game objects
    player = Player(PLAYER_START_X, PLAYER_START_Y)
    platforms = generate_platforms(SCREEN_WIDTH, SCREEN_HEIGHT)
    enemies = spawn_enemies(2.5, SCREEN_WIDTH, SCREEN_HEIGHT, screen, platforms)

    # UI icons
    pause_icon = pygame.transform.scale(pygame.image.load(PAUSE_ICON_PATH).convert_alpha(), ICON_SIZE)
    info_icon = pygame.transform.scale(pygame.image.load(INFO_ICON_PATH).convert_alpha(), ICON_SIZE)
    volume_icon = pygame.transform.scale(pygame.image.load(VOLUME_ICON_PATH).convert_alpha(), ICON_SIZE)

    pause_rect = pause_icon.get_rect(topleft=PAUSE_BTN_POS)
    info_rect = info_icon.get_rect(topleft=INFO_BTN_POS)
    volume_icon_pos = (LEVEL_POS[0], LEVEL_POS[1] + 30)
    volume_rect = volume_icon.get_rect(topleft=volume_icon_pos)
    volume_slider_rect = pygame.Rect(volume_rect.left + 10, volume_rect.bottom + 10, 20, 100)

    # UI state
    paused = False
    show_info = False
    slider_visible = False
    running = True

    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif not paused:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pause_rect.collidepoint(event.pos):
                        paused = True
                    elif info_rect.collidepoint(event.pos):
                        show_info = not show_info
                    elif volume_rect.collidepoint(event.pos):
                        slider_visible = not slider_visible
                    elif slider_visible and volume_slider_rect.collidepoint(event.pos):
                        mouse_y = event.pos[1]
                        relative_y = mouse_y - volume_slider_rect.top
                        volume = max(0.0, min(1.0, 1 - (relative_y / volume_slider_rect.height)))
                        pygame.mixer.music.set_volume(volume)
                        jump_sound.set_volume(volume)
                        game_over_sound.set_volume(volume)
                        settings["volume"] = volume
                        save_settings(settings)

                elif event.type == pygame.MOUSEMOTION and slider_visible and event.buttons[0]:
                    if volume_slider_rect.collidepoint(event.pos):
                        mouse_y = event.pos[1]
                        relative_y = mouse_y - volume_slider_rect.top
                        volume = max(0.0, min(1.0, 1 - (relative_y / volume_slider_rect.height)))
                        pygame.mixer.music.set_volume(volume)
                        jump_sound.set_volume(volume)
                        game_over_sound.set_volume(volume)
                        settings["volume"] = volume
                        save_settings(settings)

                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_UP) and not player.is_jumping:
                        player.jump()
                        jump_sound.play()

        if paused:
            paused = show_pause_menu(screen, SCREEN_WIDTH, SCREEN_HEIGHT, pause_font)
            continue

        # Update player and world
        keys = pygame.key.get_pressed()
        player.move(keys, SCREEN_WIDTH)
        player.apply_gravity()
        player.update(dt)

        for p in platforms:
            p.update()

        score = int(scroll_offset)
        difficulty_level = score // MAX_PLATFORM_DISTANCE

        if player.y < SCROLL_TRIGGER_Y:
            scroll = SCROLL_TRIGGER_Y - player.y
            scroll_offset += scroll
            player.y = SCROLL_TRIGGER_Y
            scroll_platforms(platforms, scroll)
            recycle_platforms(platforms, SCREEN_WIDTH, SCREEN_HEIGHT)

            for enemy in enemies:
                enemy.rect.y += scroll
                if enemy.rect.y > SCREEN_HEIGHT:
                    enemy.rect.y = -50
                    enemy.rect.x = randint(50, SCREEN_WIDTH - 100)

        player_rect = player.get_rect()
        for p in platforms:
            plat_rect = pygame.Rect(p.x, p.y, p.width, p.height)
            if player.vel_y > 0 and player_rect.colliderect(plat_rect):
                if player_rect.bottom <= plat_rect.bottom + 10:
                    player.y = p.y - player.height
                    player.vel_y = 0
                    player.is_jumping = False


        # Draw everything
        draw_background(screen)
        for platform in platforms:
            platform.draw(screen)

        for enemy in enemies:
            enemy.update()
            screen.blit(enemy.image, enemy.rect)

        player.draw(screen)

        if show_info:
            pygame.draw.rect(screen, INFO_BG_COLOR, INFO_BOX_RECT)
            for i, line in enumerate(INFO_LINES):
                screen.blit(font.render(line, True, INFO_TEXT_COLOR), (70, 220 + i * 30))

        screen.blit(font.render(f"Score: {score}", True, SCORE_TEXT_COLOR), SCORE_POS)
        screen.blit(font.render(f"Lvl: {difficulty_level + 1}", True, SCORE_TEXT_COLOR), LEVEL_POS)

        screen.blit(pause_icon, pause_rect)
        screen.blit(info_icon, info_rect)
        screen.blit(volume_icon, volume_rect)

        if slider_visible:
            slider_width = 6
            knob_radius = 8
            center_x = volume_slider_rect.centerx

            pygame.draw.rect(screen, (160, 160, 160),
                             (center_x - slider_width // 2, volume_slider_rect.top,
                              slider_width, volume_slider_rect.height), border_radius=3)

            knob_y = volume_slider_rect.top + (1 - volume) * volume_slider_rect.height
            pygame.draw.circle(screen, (80, 80, 255), (center_x, int(knob_y)), knob_radius)

        if player.y > SCREEN_HEIGHT:
            pygame.mixer.music.stop()
            game_over_sound.play()
            return show_game_over(
                screen, font, scroll_offset,
                bg_layers, scroll_offsets, scroll_speeds,
                save_high_score, load_high_score,
                run_game, player
            )


        for enemy in enemies:
            if player.get_rect().colliderect(enemy.rect):
                game_over_sound.play()
                pygame.mixer.music.stop()
                return show_game_over(
                    screen, font, scroll_offset,
                    bg_layers, scroll_offsets, scroll_speeds,
                    save_high_score, load_high_score,
                    run_game, player
                )

        pygame.display.update()

    return None

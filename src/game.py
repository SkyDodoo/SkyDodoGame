# game.py
import pygame
import os
from random import randint
from src.player import Player
from src.game_platform import generate_platforms, scroll_platforms, recycle_platforms
from src.start import draw_background
from src.sprites.enemy_1 import Monster

HIGHSCORE_FILE = "highscore.txt"
ENEMY_SIZE = 50

def load_high_score():
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as f:
            return int(f.read())
    return 0

def save_high_score(score):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))

def spawn_enemies(num, screen_width, screen_height, game, platforms):
    enemies = []
    attempts = 0 #count for attempts (place enemy)
    min_distance = 200 #min distance between the enemies
    min_platform_dist_x = 150
    min_platform_dist_y = 40

    while len(enemies) < num and attempts < 1000: #until enough players or max 100 attempts
        x = randint(50, screen_width - ENEMY_SIZE -50)
        y = randint(100, screen_height -200)

        # creating a test for enemy
        test_rect = pygame.Rect(x,y, ENEMY_SIZE, ENEMY_SIZE)

        collides = False
        for p in platforms:
            plat_rect = pygame.Rect(p.x, p.y, p.width, p.height) #build a rect from the coordinates of the platform

            # no overlap with platform
            if test_rect.colliderect(plat_rect):
                collides = True
                break

            # distance enemy - platform
            dx = max(0, max(p.x -(x+ ENEMY_SIZE), x - (p.x + p.width)))
            dy= max(0, max(p.y - (y + ENEMY_SIZE), y - (p.y + p.height)))
            if dx < min_platform_dist_x and dy < min_platform_dist_y:
                collides = True
                break

        if not collides: #check for distance enemies
            for e in enemies:
                distance = ((e.rect.x - x)**2 + (e.rect.y - y)**2)**0.5 #calculation of the "Luftlinie"
                if distance < min_distance:
                    collides = True
                    break

        if not collides: #create enemy
            enemy = Monster(game=game, x=x, y=y)
            enemies.append(enemy)

        attempts += 1

    return enemies

def draw_animated_background(screen, bg_layers, scroll_offsets, scroll_speeds):
    screen_width = screen.get_width()
    for i, layer in enumerate(bg_layers):
        scroll_offsets[i] = (scroll_offsets[i] + scroll_speeds[i]) % screen_width
        x = -scroll_offsets[i]
        screen.blit(layer, (x, 0))
        screen.blit(layer, (x + screen_width, 0))

def run_game():
    pygame.init()
    pygame.mixer.init()
    screen_width, screen_height = 600, 750
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Load background layers AFTER display is set
    bg_layers = [
        pygame.image.load("assets/images/Nature Landscapes Free Pixel Art/nature_1/1.png").convert_alpha(),
        pygame.image.load("assets/images/Nature Landscapes Free Pixel Art/nature_1/2.png").convert_alpha(),
        pygame.image.load("assets/images/Nature Landscapes Free Pixel Art/nature_1/3.png").convert_alpha(),
        pygame.image.load("assets/images/Nature Landscapes Free Pixel Art/nature_1/5.png").convert_alpha(),
        pygame.image.load("assets/images/Nature Landscapes Free Pixel Art/nature_1/6.png").convert_alpha()
    ]
    scroll_offsets = [0 for _ in bg_layers]
    scroll_speeds = [0.2, 0.4, 0.6, 0.8, 1.2]

    clock = pygame.time.Clock()

    # Load sounds and music
    pygame.mixer.music.load("assets/sounds/background_music.mp3")
    pygame.mixer.music.play(-1)
    jump_sound = pygame.mixer.Sound('./assets/sounds/jump_sound.wav')
    game_over_sound = pygame.mixer.Sound("assets/sounds/gameover.wav")

    # Fonts
    font = pygame.font.SysFont("Arial", 24)
    pause_font = pygame.font.SysFont("Arial", 48)
    notif_font = pygame.font.SysFont("Arial", 24)

    # Game objects
    player = Player(300, screen_height - 150)
    platforms = generate_platforms(screen_width, screen_height)
    enemies = spawn_enemies(3, screen_width, screen_height, screen, platforms)

    # Load icons
    pause_icon = pygame.image.load("assets/images/pause_btn.svg").convert_alpha()
    info_icon = pygame.image.load("assets/images/info_btn.svg").convert_alpha()
    pause_icon = pygame.transform.scale(pause_icon, (40, 40))
    info_icon = pygame.transform.scale(info_icon, (40, 40))
    logo = pygame.image.load("assets/images/logo.webp").convert_alpha()
    logo = pygame.transform.scale(logo, (200, 80))

    # Button positions
    pause_rect = pause_icon.get_rect(topleft=(screen_width - 50, 10))
    info_rect = info_icon.get_rect(topleft=(screen_width - 100, 10))

    # Flags
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
            resume_btn, quit_btn = show_pause_menu(screen, screen_width, screen_height, pause_font, bg_layers, scroll_offsets, scroll_speeds )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if resume_btn.collidepoint(event.pos):
                        paused = False
                        pygame.time.wait(200)
                    elif quit_btn.collidepoint(event.pos):
                        pygame.quit()
                        exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    paused = False
            clock.tick(60)
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
        enemy_speed = 2 + difficulty_level
        platform_speed = 2 + difficulty_level
        gravity_scale = 0.6 + 0.1 * difficulty_level

        if player.y < screen_height // 3:
            scroll = screen_height // 3 - player.y
            player.y = screen_height // 3
            scroll_platforms(platforms, scroll)
            recycle_platforms(platforms, screen_width, screen_height)
            for enemy in enemies:
                enemy.rect.y += scroll
                if enemy.rect.y > screen_height:
                    enemy.rect.y = -ENEMY_SIZE
                    enemy.rect.x = randint(50, screen_width - ENEMY_SIZE - 50)

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
                return show_game_over(screen, font, max_height, bg_layers, scroll_offsets, scroll_speeds)

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
                line_surface = font.render(line, True, (0, 0, 0))
                screen.blit(line_surface, (70, 220 + i * 30))

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

        score_text = font.render(f"Score: {max_height}", True, (0, 0, 0))
        level_text = font.render(f"Lvl: {difficulty_level + 1}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 40))

        screen.blit(pause_icon, pause_rect)
        screen.blit(info_icon, info_rect)

        if player.y > screen_height:
            pygame.mixer.music.stop()
            game_over_sound.play()
            return show_game_over(screen, font, max_height, bg_layers, scroll_offsets, scroll_speeds)

        pygame.display.update()
    return None

def show_game_over(screen, font, score, bg_layers, scroll_offsets, scroll_speeds):
    clock = pygame.time.Clock()
    running = True
    high_score = load_high_score()
    if score > high_score:
        save_high_score(score)
        high_score = score

    title_font = pygame.font.SysFont("Comic Sans MS", 64, bold=True)
    score_font = pygame.font.SysFont("Comic Sans MS", 32)
    hint_font = pygame.font.SysFont("Comic Sans MS", 24)

    blink = True
    blink_timer = 0
    while running:
        # draw_animated_background(screen, bg_layers, scroll_offsets, scroll_speeds)
        # overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        # overlay.fill((0, 0, 0, 100))
        # screen.blit(overlay, (0, 0))

        title = title_font.render("GAME OVER", True, (255, 0, 0))
        shadow = title_font.render("GAME OVER", True, (0, 0, 0))
        title_x = screen.get_width() // 2 - title.get_width() // 2
        screen.blit(shadow, (title_x + 2, 102))
        if blink:
            screen.blit(title, (title_x, 100))
        # screen.blit(logo, (screen.get_width() // 2 - logo.get_width() // 2, 30))

        # Draw Scores
        score_text = score_font.render(f"Score: {score}", True, (0, 0, 0))
        high_score_text = score_font.render(f"High Score: {high_score}", True, (20, 40, 200))
        screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, 200))
        screen.blit(high_score_text, (screen.get_width() // 2 - high_score_text.get_width() // 2, 240))

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
                    return run_game()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

        clock.tick(60)
    return None
    scroll_offsets[i] = (scroll_offsets[i] + scroll_speeds[i]) % screen_height
    y = -scroll_offsets[i]
    screen.blit(layer, (0, y))
    screen.blit(layer, (0, y + screen_height))

def show_pause_menu(screen, screen_width, screen_height, pause_font, bg_layers, scroll_offsets, scroll_speeds):
    clock = pygame.time.Clock()
    running = True

    btn_font = pygame.font.SysFont("Arial", 32)
    resume_btn = pygame.Rect(screen_width // 2 - 100, 300, 200, 50)
    quit_btn = pygame.Rect(screen_width // 2 - 100, 380, 200, 50)

    while running:
        draw_animated_background(screen, bg_layers, scroll_offsets, scroll_speeds)

        # Dim overlay
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        # Title
        title = pause_font.render("Game Paused", True, (255, 255, 255))
        screen.blit(title, (screen_width // 2 - title.get_width() // 2, 150))

        # Buttons
        pygame.draw.rect(screen, (100, 200, 100), resume_btn, border_radius=12)
        pygame.draw.rect(screen, (200, 80, 80), quit_btn, border_radius=12)

        screen.blit(btn_font.render("▶ Resume", True, (255, 255, 255)), (resume_btn.x + 40, resume_btn.y + 10))
        screen.blit(btn_font.render("⏻ Quit", True, (255, 255, 255)), (quit_btn.x + 60, quit_btn.y + 10))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if resume_btn.collidepoint(event.pos):
                    return False
                elif quit_btn.collidepoint(event.pos):
                    pygame.quit()
                    exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

        clock.tick(60)

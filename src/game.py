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

def spawn_enemies(num, screen_width, screen_height, game):
    enemies = []
    for _ in range(num):
        x = randint(50, screen_width - ENEMY_SIZE - 50)
        y = randint(100, screen_height - 200)
        enemy = Monster(game=game, x=x, y=y)
        enemies.append(enemy)
    return enemies

def run_game():
    pygame.init()
    pygame.mixer.init()
    screen_width, screen_height = 600, 750
    screen = pygame.display.set_mode((screen_width, screen_height))
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
    enemies = spawn_enemies(3, screen_width, screen_height)

    # Game state
    paused = False
    enemies = spawn_enemies(3, screen_width, screen_height, screen)

    start_y = player.y
    max_height = 0
    notif_timer = 0
    notif_message = ""

    running = True
    while running:
        dt = clock.tick(60) / 1000

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not player.is_jumping and not paused:
                    player.jump()
                    jump_sound.play()
                elif event.key == pygame.K_p:
                    paused = not paused

        if paused:
            draw_background(screen)
            overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            pause_text = pause_font.render("PAUSED", True, (255, 255, 255))
            screen.blit(pause_text, (screen_width // 2 - pause_text.get_width() // 2, screen_height // 2))
            pygame.display.flip()
            continue

        # Game logic
        keys = pygame.key.get_pressed()
        player.move(keys, screen_width)
        player.apply_gravity()

        # Platform updates
        for p in platforms:
            p.update()

        # Score update
        height_climbed = max(0, start_y - player.y)
        max_height = int(height_climbed)

        # Screen scrolling
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

        # Platform collision
        player_rect = player.get_rect()
        for p in platforms:
            plat_rect = pygame.Rect(p.x, p.y, p.width, p.height)
            if player.vel_y > 0 and player_rect.colliderect(plat_rect):
                if player_rect.bottom <= plat_rect.bottom + 10:
                    player.y = p.y - player.height
                    player.vel_y = 0
                    player.is_jumping = False

        # Enemy collisions
        for enemy in enemies:
            if player.get_rect().colliderect(enemy.rect):
                game_over_sound.play()
                pygame.mixer.music.stop()
                return show_game_over(screen, font, max_height)
            if abs(enemy.y - player.y) < 150:
                notif_message = "⚠ Enemy nearby!"
                notif_timer = pygame.time.get_ticks()

        # Drawing
        draw_background(screen)
        for platform in platforms:
            platform.draw(screen)
        for enemy in enemies:
            enemy.update()
            screen.blit(enemy.image, enemy.rect)
        player.draw(screen)

        # Score display
        score_text = font.render(f"Score: {max_height}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        # Notification display
        if notif_message and pygame.time.get_ticks() - notif_timer < 2000:
            notif_text = notif_font.render(notif_message, True, (255, 100, 100))
            screen.blit(notif_text, (screen_width // 2 - notif_text.get_width() // 2, 40))
        else:
            notif_message = ""

        # Game over check (falling off screen)
        if player.y > screen_height:
            pygame.mixer.music.stop()
            game_over_sound.play()
            return show_game_over(screen, font, max_height)

        pygame.display.update()
    return None


def show_game_over(screen, font, score):
    clock = pygame.time.Clock()
    running = True
    high_score = load_high_score()
    if score > high_score:
        save_high_score(score)
        high_score = score

    # Load background and player character
    bg = pygame.image.load("assets/images/blueback.jpg").convert()
    logo = pygame.image.load("assets/images/logo.webp").convert_alpha()
    logo = pygame.transform.scale(logo, (200, 100))  # adjust as needed
    player_img = pygame.image.load("assets/images/dodo_sprite_sheet.png").convert_alpha()
    player_img = pygame.transform.scale(player_img, (80, 80))  # adjust size as needed

    # Fonts
    title_font = pygame.font.SysFont("Comic Sans MS", 64, bold=True)
    score_font = pygame.font.SysFont("Comic Sans MS", 32)
    hint_font = pygame.font.SysFont("Comic Sans MS", 24)

    blink = True
    blink_timer = 0
    while running:
        screen.blit(bg, (0, 0))

        # Draw "Game Over" Title
        title = title_font.render("GAME OVER", True, (255, 0, 0))
        shadow = title_font.render("GAME OVER", True, (0, 0, 0))
        title_x = screen.get_width() // 2 - title.get_width() // 2
        screen.blit(shadow, (title_x + 2, 102))
        if blink:
            screen.blit(title, (title_x, 100))
        screen.blit(logo, (screen.get_width() // 2 - logo.get_width() // 2, 30))

        # Draw Scores
        score_text = score_font.render(f"Score: {score}", True, (0, 0, 0))
        high_score_text = score_font.render(f"High Score: {high_score}", True, (20, 40, 200))
        screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, 200))
        screen.blit(high_score_text, (screen.get_width() // 2 - high_score_text.get_width() // 2, 240))

        # Retry Instruction
        hint = hint_font.render("Press SPACE to Retry or ESC to Quit", True, (80, 80, 80))
        screen.blit(hint, (screen.get_width() // 2 - hint.get_width() // 2, 300))

        # Draw player character
        screen.blit(player_img, (screen.get_width() // 2 - player_img.get_width() // 2, 380))

        # Blink title
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

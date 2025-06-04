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

    jump_sound = pygame.mixer.Sound('./assets/sounds/jump_sound.wav')
    game_over_sound = pygame.mixer.Sound("assets/sounds/gameover.wav")
    font = pygame.font.SysFont("Arial", 24)

    player = Player(300, screen_height - 150)
    platforms = generate_platforms(screen_width, screen_height)
    enemies = spawn_enemies(3, screen_width, screen_height, screen)

    start_y = player.y
    max_height = 0

    running = True
    while running:
        clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not player.is_jumping:
                    player.jump()
                    jump_sound.play()

        keys = pygame.key.get_pressed()
        player.move(keys, screen_width)
        player.apply_gravity()

        for platform in platforms:
            platform.update()

        # Update score
        height_climbed = max(0, start_y - player.y)
        if height_climbed > max_height:
            max_height = int(height_climbed)

        # Scroll screen
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

        # Platform collisions
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
                return show_game_over(screen, font, max_height)

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

        if player.y > screen_height:
            game_over_sound.play()
            return show_game_over(screen, font, max_height)

        pygame.display.update()

    return None

def show_game_over(screen, font, score):
    clock = pygame.time.Clock()
    high_score = load_high_score()
    if score > high_score:
        save_high_score(score)
        high_score = score

    blink = True
    blink_timer = 0
    running = True

    while running:
        screen.fill((0, 0, 0))

        text = font.render("\U0001FAA6 Game Over", True, (255, 0, 0))
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        hi_score_text = font.render(f"High Score: {high_score}", True, (180, 180, 255))
        retry_text = font.render("Press SPACE to Retry or ESC to Quit", True, (200, 200, 200))

        blink_timer += clock.get_time()
        if blink_timer > 500:
            blink = not blink
            blink_timer = 0

        if blink:
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 200))
        screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, 270))
        screen.blit(hi_score_text, (screen.get_width() // 2 - hi_score_text.get_width() // 2, 310))
        screen.blit(retry_text, (screen.get_width() // 2 - retry_text.get_width() // 2, 350))

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

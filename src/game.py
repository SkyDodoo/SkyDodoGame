# game.py
import pygame
import os
from src.player import Player
from src.game_platform import generate_platforms, scroll_platforms, recycle_platforms
from src.start import draw_background
from random import randint

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

def spawn_enemies(num, screen_width, screen_height):
    enemies = []
    for _ in range(num):
        x = randint(50, screen_width - ENEMY_SIZE - 50)
        y = randint(100, screen_height - 200)
        rect = pygame.Rect(x, y, ENEMY_SIZE, ENEMY_SIZE)
        enemies.append(rect)
    return enemies

def run_game():
    pygame.init()
    pygame.mixer.init()
    screen_width, screen_height = 600, 750
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    jump_sound = pygame.mixer.Sound('./assets/sounds/jump_sound.wav')

    player = Player(300, screen_height - 150)
    platforms = generate_platforms(screen_width, screen_height)
    enemies = spawn_enemies(3, screen_width, screen_height)
    font = pygame.font.SysFont("Arial", 24)
    start_y = player.y
    max_height = 0
    game_over_sound = pygame.mixer.Sound("assets/sounds/gameover.wav")

    running = True
    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not player.is_jumping:
                    player.jump()  # Removed 'stronger=True'
                    jump_sound.play()
        keys = pygame.key.get_pressed()
        player.move(keys, screen_width)
        player.apply_gravity()

        #Moving Platforms
        for p in platforms:
            p.update()


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
            for e in enemies:
                e.y += scroll
                if e.y > screen_height:
                    e.y = -ENEMY_SIZE
                    e.x = randint(50, screen_width - ENEMY_SIZE - 50)

        # Collision with platforms
        player_rect = player.get_rect()
        for p in platforms:
            plat_rect = pygame.Rect(p.x, p.y, p.width, p.height)
            if player.vel_y > 0 and player_rect.colliderect(plat_rect):
                if player_rect.bottom <= plat_rect.bottom + 10:
                    player.y = p.y - player.height
                    player.vel_y = 0
                    player.is_jumping = False

        # Collision with enemies = game over
        for enemy in enemies:
            if player.get_rect().colliderect(enemy):
                game_over_sound.play()
                return show_game_over(screen, font, max_height)

        draw_background(screen)
        for p in platforms:
            p.draw(screen)
        for enemy in enemies:
            pygame.draw.rect(screen, (255, 0, 0), enemy)
        player.draw(screen)

        # Score
        score_text = font.render(f"Score: {max_height}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        # Game over check
        if player.y > screen_height:
            game_over_sound.play()
            return show_game_over(screen, font, max_height)

        pygame.display.update()

def show_game_over(screen, font, score):
    clock = pygame.time.Clock()
    running = True
    high_score = load_high_score()
    if score > high_score:
        save_high_score(score)
        high_score = score

    blink = True
    blink_timer = 0
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

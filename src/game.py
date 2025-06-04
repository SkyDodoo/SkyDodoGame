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
        clock.tick(60) / 1000

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

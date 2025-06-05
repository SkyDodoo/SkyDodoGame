
# enemy_logic.py
# ---------------------------------
# Handles enemy creation with collision constraints

# Method: spawn_enemies
# num - number of enemies to spawn
# screen_width, screen_height - dimensions of the game screen
# game - reference to the game instance (used to create enemy instances)
# platforms - list of platform objects to avoid when spawning enemies
# -------------------------------------------------------------
# Spawns a specified number of enemies at random positions on the screen.
# Ensures that enemies:
# - do not spawn inside or too close to platforms,
# - do not spawn too close to each other (min_distance),
# - are within screen bounds.
# Tries up to 1000 attempts to find valid spawn positions.

def spawn_enemies(num, screen_width, screen_height, game, platforms):
    import pygame
    from random import randint
    from src.sprites.bettle import Bettle

    enemies = []
    attempts = 0
    min_distance = 200
    min_platform_dist_x = 150
    min_platform_dist_y = 40

    while len(enemies) < num and attempts < 1000:
        x = randint(50, screen_width - 50)
        y = randint(100, screen_height - 200)
        test_rect = pygame.Rect(x, y, 50, 50)

        collides = False
        for p in platforms:
            plat_rect = pygame.Rect(p.x, p.y, p.width, p.height)
            if test_rect.colliderect(plat_rect):
                collides = True
                break

            dx = max(0, max(p.x - (x + 50), x - (p.x + p.width)))
            dy = max(0, max(p.y - (y + 50), y - (p.y + p.height)))
            if dx < min_platform_dist_x and dy < min_platform_dist_y:
                collides = True
                break

        if not collides:
            for e in enemies:
                distance = ((e.rect.x - x)**2 + (e.rect.y - y)**2)**0.5
                if distance < min_distance:
                    collides = True
                    break

        if not collides:
            enemies.append(Bettle(game=game, x=x, y=y))

        attempts += 1

    return enemies

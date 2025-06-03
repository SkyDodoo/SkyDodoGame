import pygame
from pygame.locals import *

class Player:
    width = 50
    height = 50
    speed = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (0, 0, 255)
        self.gravity = 0.3
        self.vel_y = 0
        self.is_jumping = False #Player starts at the ground

    # move horizontally
    def move(self, keys, screen_width):
        if keys[K_LEFT]:
            self.x -= self.speed
            if self.x < 0: # limit screen
                self.x = 0
        if keys[K_RIGHT]:
            self.x += self.speed
            if self.x > screen_width - self.width:
                self.x = screen_width - self.width


    def apply_gravity(self):
        self.vel_y += self.gravity
        self.y += self.vel_y

    def jump(self):
        if not self.is_jumping:
            self.vel_y = -6
            self.is_jumping = True


    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))



pygame.init()

screen_width = 600
screen_height = 750
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('SkyDodo')

clock = pygame.time.Clock()

ground_height = 100
ground_y = screen_height - ground_height

player = Player(100, ground_y - Player.height)

running = True
game_over = False


while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    if not game_over:
        keys = pygame.key.get_pressed()
        player.move(keys, screen_width)
        player.apply_gravity()

    if player.y + player.height >= ground_y:
        player.jump()

    if player.y > screen_height:
        game_over = True

    screen.fill((0, 0, 0))
    #pygame.draw.rect(screen,(255, 255, 255,), (0,ground_y, screen_width, ground_height))
    player.draw(screen)
    pygame.display.flip()


pygame.quit()
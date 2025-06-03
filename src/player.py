import pygame

class Player:
    width = 64
    height = 64
    speed = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_y = 0
        self.gravity = 0.4
        self.is_jumping = False

        self.frames = self.load_sprite_frames("../assets/images/dodo_sprite_sheet.png", 128, 128)
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.1
        self.image = self.frames[self.current_frame]

    def load_sprite_frames(self, path, frame_width, frame_height):
        sprite_sheet = pygame.image.load(path).convert_alpha()
        frames = []
        for i in range(6):
            frame = sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (self.width, self.height))
            frames.append(frame)
        return frames

    def move(self, keys, screen_width):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        self.x = max(0, min(self.x, screen_width - self.width))

    def apply_gravity(self):
        self.vel_y += self.gravity
        self.y += self.vel_y

    def jump(self):
        self.vel_y = -10
        self.is_jumping = True

    def update(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

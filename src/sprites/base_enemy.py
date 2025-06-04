import pygame

class BaseEnemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y, sprite_sheet_path, frame_width, frame_height, frame_count, animation_speed=0.15):
        super().__init__()
        self.game = game
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.frames = self.load_frames(frame_width, frame_height, frame_count)
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.animation_speed = animation_speed
        self.animation_timer = 0

    def load_frames(self, width, height, count):
        return [
            self.sprite_sheet.subsurface(pygame.Rect(i * width, 0, width, height))
            for i in range(count)
        ]

    def animate(self):
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.animation_timer = 0

    def update(self):
        self.animate()

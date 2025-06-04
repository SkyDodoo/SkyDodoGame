import pygame
import os

class BaseEnemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y, frame_paths, animation_speed=0.15):
        super().__init__()
        self.game = game
        self.frames = self.load_frames(frame_paths)
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.animation_speed = animation_speed
        self.animation_timer = 0

    def load_frames(self, paths):
        return [pygame.image.load(path).convert_alpha() for path in paths]

    def animate(self):
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.animation_timer = 0

    def update(self):
        self.animate()

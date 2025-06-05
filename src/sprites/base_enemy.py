import pygame
import os

# Constructor: __init__
        # game - reference to the main game object
        # x, y - initial position of the enemy
        # frame_paths - list of file paths for animation frames
        # animation_speed - controls how fast the animation updates
        # -------------------------------------------------------------
        # Initializes the BaseEnemy object with position, animation frames,
        # and animation speed. Sets the starting frame and defines the
        # sprite's rectangle for positioning and collision.

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

    # Method: load_frames
    # paths - list of strings with file paths to animation frames
    # -------------------------------------------------------------
    # Loads each image from the given paths and returns them as a list
    # of surfaces with alpha transparency.
    def load_frames(self, paths):
        return [pygame.image.load(path).convert_alpha() for path in paths]

    # Method: animate
    # -------------------------------------------------------------
    # Increments the animation timer based on animation speed.
    # When the timer exceeds a threshold, advances to the next frame
    # in the animation cycle and resets the timer.
    def animate(self):
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.animation_timer = 0

    # Method: update
    # -------------------------------------------------------------
    # Called every frame to update the enemy.
    # Handles animation logic by calling the animate method.
    def update(self):
        self.animate()

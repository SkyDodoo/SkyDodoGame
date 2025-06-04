# src/player.py
import pygame

class Player:
    width = 64
    height = 64
    speed = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_y = 0
        self.gravity = 0.8
        self.is_jumping = False
        self.direction = "idle"  # 'idle', 'fly', 'jump', 'eat'
        self.facing_right = False

        self.animations = self.load_animation_rows("assets/images/BirdSprite.png", 16, 16)
        self.current_row = 0
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.04
        self.image = self.animations[self.current_row][self.current_frame]

    def load_animation_rows(self, path, frame_width, frame_height):
        sprite_sheet = pygame.image.load(path).convert_alpha()
        sheet_width, sheet_height = sprite_sheet.get_size()
        total_rows = sheet_height // frame_height

        # Define actual number of frames per row
        frames_per_row = {
            0: 2,  # idle
            1: 8,  # fly/jump
            2: 3   # eat (or rotate if repurposed)
        }

        animations = []
        for row in range(total_rows):
            row_frames = []
            max_cols = frames_per_row.get(row, 0)
            for col in range(max_cols):
                # Check if frame is inside image bounds
                if (col + 1) * frame_width <= sheet_width:
                    frame = sprite_sheet.subsurface(
                        pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height)
                    )
                    frame = pygame.transform.scale(frame, (self.width, self.height))
                    row_frames.append(frame)
            animations.append(row_frames)
        return animations

    def move(self, keys, screen_width):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
            self.direction = "fly"
            self.facing_right = True
        elif keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.direction = "fly"
            self.facing_right = False
        else:
            self.direction = "idle"

        self.x = max(0, min(self.x, screen_width - self.width))

    def apply_gravity(self):
        self.vel_y += self.gravity
        self.y += self.vel_y

        # Use jump/fly animation when moving vertically
        if self.vel_y < 0:
            self.direction = "fly"
        elif self.vel_y > 5:
            self.direction = "fly"

    def jump(self):
        self.vel_y = -20
        self.is_jumping = True
        self.direction = "fly"

    def update(self, dt):
        # Set current animation row
        if self.direction == "idle":
            self.current_row = 0
            self.current_frame = 0  # Always show the first idle frame
            self.image = self.animations[self.current_row][self.current_frame]
            return  # Skip animation

        elif self.direction == "fly":
            self.current_row = 1
        elif self.direction == "eat":
            self.current_row = 2

        # Animate for non-idle directions
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            num_frames = len(self.animations[self.current_row])
            self.current_frame = (self.current_frame + 1) % num_frames
            self.image = self.animations[self.current_row][self.current_frame]

    def draw(self, screen):
        image = self.image
        if not self.facing_right:
            image = pygame.transform.flip(self.image, True, False)
        screen.blit(image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

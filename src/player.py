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
        self.direction = "idle"  # 'fly', 'jump', 'rotate'

        # Load animations from multiple rows
        self.animations = self.load_animation_rows("assets/images/BirdSprite.png", 16, 16)
        self.current_row = 0
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.04
        self.image = self.animations[self.current_row][self.current_frame]

    def load_animation_rows(self, path, frame_width, frame_height):
        sprite_sheet = pygame.image.load(path).convert_alpha()
        sheet_width, sheet_height = sprite_sheet.get_size()

        rows = sheet_height // frame_height
        cols = sheet_width // frame_width  # total number of cols, not necessarily used
        max_valid_cols = 6  # manually set how many frames to load per row

        animations = []
        for row in range(rows):
            row_frames = []
            for col in range(max_valid_cols):
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
        elif keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.direction = "fly"
        else:
            self.direction = "idle"
        self.x = max(0, min(self.x, screen_width - self.width))

    def apply_gravity(self):
        self.vel_y += self.gravity
        self.y += self.vel_y
        if self.vel_y < 0:
            self.direction = "jump"
        elif self.vel_y > 5:
            self.direction = "rotate"

    def jump(self):
        self.vel_y = -20
        self.is_jumping = True
        self.direction = "jump"

    def update(self, dt):
        # Select row based on direction
        if self.direction == "idle":
            self.current_row = 0
        elif self.direction == "fly":
            self.current_row = 1
        elif self.direction == "jump" or self.direction == "rotate":
            self.current_row = 2

        # Animate
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_row])
            self.image = self.animations[self.current_row][self.current_frame]

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

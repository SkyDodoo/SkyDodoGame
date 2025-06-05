from src.sprites.base_enemy import BaseEnemy
import os

class Bettle(BaseEnemy):
    def __init__(self, game, x=300, y=400):
        frame_paths = [
            os.path.join("assets", "images", "enemies", f"bettle_smaller{i}.png")
            for i in range(1, 5)
        ]
        super().__init__(
            game=game,
            x=x,
            y=y,
            frame_paths=frame_paths,
            animation_speed=0.2
        )

        self.start_x = x
        self.move_range = 100
        self.speed = 2
        self.direction = 1

    def update(self):
        super().update()

        self.rect.x += self.speed * self.direction

        if self.rect.x > self.start_x + self.move_range:
            self.direction = -1
        elif self.rect.x < self.start_x - self.move_range:
            self.direction = 1


from src.sprites.base_enemy import BaseEnemy
import os

class Monster(BaseEnemy):
    def __init__(self, game, x=300, y=400):
        frame_paths = [
            os.path.join("assets", "images", "enemies", f"bettle{i}.png")
            for i in range(1, 5)
        ]
        super().__init__(
            game=game,
            x=x,
            y=y,
            frame_paths=frame_paths,
            animation_speed=0.2
        )

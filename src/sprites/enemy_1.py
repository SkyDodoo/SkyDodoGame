from base_enemy import BaseEnemy

class Monster(BaseEnemy):
    def __init__(self, game, x=300, y=400):
        super().__init__(
            game=game,
            x=x,
            y=y,
            sprite_sheet_path="",
            frame_width =50,
            frame_height=50,
            frame_count=4,
            animation_speed=0.2)

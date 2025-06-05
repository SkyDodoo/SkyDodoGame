# config.py

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 750

# Player starting position
PLAYER_START_X = 300
PLAYER_START_Y = SCREEN_HEIGHT - 150

# Assets - images
BACKGROUND_IMAGE = "assets/images/Nature Landscapes Free Pixel Art/nature_1/orig.png"
PAUSE_ICON_PATH = "assets/images/pause_btn.svg"
INFO_ICON_PATH = "assets/images/info_btn.svg"
VOLUME_ICON_PATH = "assets/images/volume_btn.svg"
ICON_SIZE = (40, 40)

# UI positions
PAUSE_BTN_POS = (SCREEN_WIDTH - 50, 60)
INFO_BTN_POS = (SCREEN_WIDTH - 100, 60)

# Sounds
MUSIC_PATH = "assets/sounds/background_music.mp3"
JUMP_SOUND_PATH = "assets/sounds/jump_sound.wav"
GAME_OVER_SOUND_PATH = "assets/sounds/gameover.wav"

# Difficulty & mechanics
MAX_PLATFORM_DISTANCE = 300  # Distance per level increase
SCROLL_TRIGGER_Y = SCREEN_HEIGHT // 3

# Info box
INFO_BOX_RECT = (50, 200, 500, 300)
INFO_TEXT_COLOR = (0, 0, 0)
INFO_BG_COLOR = (240, 240, 240)

# Score display
SCORE_POS = (10, 10)
LEVEL_POS = (10, 40)
SCORE_TEXT_COLOR = (0, 0, 0)

# Notification
NOTIF_DURATION = 2000  # in milliseconds
NOTIF_BG_COLOR = (0, 0, 0, 180)
NOTIF_TEXT_COLOR = (255, 200, 200)
NOTIF_POS = (SCREEN_WIDTH // 2, 40)

# Game mechanics
ENEMY_RESPAWN_Y = -50

# Info

INFO_LINES = [
                "🎮 SkyDodo Instructions:",
                "- SPACE or UP ARROW to jump",
                "- Avoid red enemies",
                "- Reach the sky!",
                "",
                "Click 'i' to hide this panel."
            ]
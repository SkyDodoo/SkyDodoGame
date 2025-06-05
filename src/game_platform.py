import pygame
import random

platform_img = pygame.image.load("assets/images/platform.png")
moving_platform_img = pygame.image.load("assets/images/moving_platform_cloud_lighter.png")

#Class for Platforms
class Platform:
    def __init__(self, x, y, width=100, height=25, moving=False, move_range=100, move_speed=2, image=None, is_ground=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.moving = moving
        self.move_range = move_range
        self.move_speed = move_speed
        self.start_x = x
        self.direction = 1 #1 = right, -1 = left
        self.movement_delta = 0
        self.image = image
        self.is_ground = is_ground

        if image:
            self.image = pygame.transform.scale(image, (self.width, self.height))


    # Method: update
    # ---------------------------------------
    # Responsible for moving the platform horizontally (left and right),
    # but only if the platform is marked as moving.
    # It updates the x-position based on speed and direction,
    # reverses direction when reaching movement bounds,
    # and stores the amount of movement in `movement_delta`.

    def update(self):
        if self.moving:
            old_x = self.x
            self.x += self.move_speed * self.direction
            self.movement_delta = self.x - old_x
            if self.x > self.start_x + self.move_range:
                self.direction = -1
            elif self.x < self.start_x:
                self.direction = 1
        else:
            self.movement_delta = 0


    # Method: draw
    # screen - instance of screen
    # -------------------------------------------------------------
    # Draws the platform on the screen.
    # If a custom image is set, it will be drawn at the platform's position.
    # Otherwise, a green rectangle is used as a fallback.
    # Additionally, if the platform is marked as ground and is near the bottom of the screen,
    # it will draw a separate ground image across the full width.

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.width, self.height))

        if self.y >= screen.get_height() - 30 and self.is_ground:
            ground_img = pygame.image.load("assets/images/ground_new.png").convert_alpha()
            ground_img = pygame.transform.scale(ground_img, (screen.get_width(), ground_img.get_height()))
            screen.blit(ground_img, (0, 750 - 80))


# Function: generate_platforms
# screen_width  - width of the game screen in pixels
# screen_height - height of the game screen in pixels
# num           - number of regular platforms to generate (default = 8)
# -------------------------------------------------------------
# Generates the initial list of platforms including:
# - One ground platform at the bottom of the screen
# - A series of regular platforms evenly spaced vertically above
# Returns a list of Platform objects initialized with random x-positions.

def generate_platforms(screen_width, screen_height, num=8):
    platforms = []

    ground = Platform(x=0, y=screen_height - 20, width=screen_width, height=25, moving=False, is_ground=True)
    platforms.append(ground)

    platform_width = 100
    for i in range(num):
        x = random.randint(10, screen_width - platform_width)
        y = screen_height - i * 90

        platforms.append(Platform(x, y, platform_width, 25, image=platform_img))
    return platforms


# Function: scroll_platforms
# platforms     - list of Platform objects currently in the game
# scroll_amount - vertical amount (in pixels) to scroll all platforms downward
# ---------------------------------------------------------------------------
# Shifts all platforms on the screen downward by a given scroll amount.
# This creates the illusion of upward player movement by moving the platforms.

def scroll_platforms(platforms, scroll_amount):
    for p in platforms:
        p.y += scroll_amount


# Function: recycle_platforms
# platforms       - list of current Platform objects in the game
# screen_width    - width of the screen in pixels
# screen_height   - height of the screen in pixels
# -------------------------------------------------------------------------------
# Recycles platforms that move out of view at the bottom of the screen.
# It removes those platforms and generates new ones at the top with random position,
# vertical spacing, movement properties, and appropriate platform image.

def recycle_platforms(platforms, screen_width, screen_height):
    platform_width = 100
    platform_height = 25
    max_attempts = 10
    min_vertical_distance = 50
    max_vertical_distance = 80
    max_horizontal_distance = 120

    for p in platforms[:]:
        if p.y > screen_height:
            platforms.remove(p)

            for i in range(max_attempts):
                new_x = random.randint(0, screen_width - platform_width - 80)
                new_y = random.randint(-100, -10)
                if (not is_too_close_vertically(new_y, platforms, min_vertical_distance) and
                    not is_overlapping(new_x, new_y, platform_width, platform_height, platforms) and
                    is_within_max_horizontal_distance(new_x, platforms, max_horizontal_distance) and
                    is_within_max_vertical_distance(new_y, platforms, max_vertical_distance)
                ):
                    moving = random.random() > 0.8
                    if moving:
                        max_range_left = new_x
                        max_range_right = screen_width - (new_x + platform_width)

                        if max_range_left < 50 or max_range_right < 50:
                            move_range = random.randint(150, 300)
                        else:
                            move_range = int(min(max_range_left, max_range_right) * random.uniform(0.8, 1.0))
                    else:
                        move_range = 0

                    move_speed = random.randint(2, 4) if moving else 0

                    image = moving_platform_img if moving else platform_img
                    platforms.append(Platform(new_x, new_y, platform_width, platform_height, True, move_range, move_speed, image=image))
                    break


# Function: is_overlapping
# new_x          - x position of the new platform
# new_y          - y position of the new platform
# width          - width of the new platform
# height         - height of the new platform
# platforms      - list of existing Platform object
# --------------------------------------------------------------
# Check whether the proposed new platform would overlap with any
# existing platforms based on their rectangular bounds.
# Returns true if overlap is detected, otherwise False.

def is_overlapping(new_x, new_y, width, height, platforms):
    for p in platforms:
        if (new_x < p.x + p.width and
            new_x + width > p.x and
            new_y < p.y + p.height and
            new_y + height > p.y):
            return True
    return False


# Function: is_too_close_vertically
# new_y          - y position of the new platform
# platforms      - list of existing Platform objects
# min_distance   - minimum allowed vertical distance between platforms
#-------------------------------------------------------------------------------
# Checks if the new platforms y-position is too close vertically to
# any existing platform. This helps in ensuring enough space for the
# player to jump or move between platforms.
# Returns True if too close, otherwise False.

def is_too_close_vertically(new_y, platforms, min_distance):
    for p in platforms:
        if abs(new_y - p.y) < min_distance:
            return True
    return False


# Function: is_within_max_vertical_distance
# new_y        - y position of the new platform
# platforms    - list of existing Platform objects
# max_distance - maximum allowed vertical distance between platforms
#---------------------------------------------------------------------------------------
# Check if the new platforms y-position is farther than may_distance
# from any existing platform vertically. This can help control platform
# spacing to avoid placing platforms to far apart.
# Returns True if the distance to any platform exceeds max_distance,
# otherwise returns False.

def is_within_max_vertical_distance(new_y, platforms, max_distance):
    for p in platforms:
        if abs(new_y - p.y) > max_distance:
            return True
    return False


# Function: is_within_max_horizontal_distance
# new_x         - x position of the new platform
# platforms     - list of existing Platform objects
# max_distance  - maximum allowed horizontal distance between platforms
# ---------------------------------------------------------------------
# Checks if the horizontal center of the new platform is within max_distance
# of the horizontal center of any existing platform.
# Returns True if there is at least one platform close enough horizontally,
# otherwise returns False.

def is_within_max_horizontal_distance(new_x, platforms, max_distance):
    for p in platforms:
        p_center_x = p.x +  p.width / 2
        new_center_x = new_x + 100 / 2
        if abs(new_center_x - p_center_x) < max_distance:
            return True
    return False

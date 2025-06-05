# background.py
# ---------------------------------
# Parallax background drawing functionality for vertical scrolling

# Method: draw_animated_background
# screen - instance of the screen to draw on
# bg_layers - list of background image layers (surfaces)
# scroll_offsets - list of current scroll positions for each layer
# scroll_speeds - list of scroll speeds corresponding to each layer
# -------------------------------------------------------------
# Draws a vertically scrolling animated background.
# Each layer scrolls at its own speed to create a parallax effect.
# The images are wrapped around so that the scrolling appears continuous.
# For each layer, two copies are drawn to ensure seamless looping.

def draw_animated_background(screen, bg_layers, scroll_offsets, scroll_speeds):
    screen_height = screen.get_height()
    for i, layer in enumerate(bg_layers):
        scroll_offsets[i] = (scroll_offsets[i] + scroll_speeds[i]) % screen_height
        y = -scroll_offsets[i]
        screen.blit(layer, (0, y))
        screen.blit(layer, (0, y + screen_height))

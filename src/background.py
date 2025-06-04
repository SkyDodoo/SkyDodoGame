# background.py
# ---------------------------------
# Parallax background drawing functionality for vertical scrolling

def draw_animated_background(screen, bg_layers, scroll_offsets, scroll_speeds):
    screen_height = screen.get_height()
    for i, layer in enumerate(bg_layers):
        scroll_offsets[i] = (scroll_offsets[i] + scroll_speeds[i]) % screen_height
        y = -scroll_offsets[i]
        screen.blit(layer, (0, y))
        screen.blit(layer, (0, y + screen_height))

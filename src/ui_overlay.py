import pygame

# Method: draw_overlay
# screen - instance of the screen to draw on
# overlay_type - string, either "pause" or "info", determines the content
# font - Pygame font object used for rendering the title
# logo - optional surface to be drawn at the top center (e.g. game logo)
# icon - optional surface to be drawn in the top-left corner (e.g. info or pause icon)
# -------------------------------------------------------------
# Draws a semi-transparent overlay on the screen.
# Displays either a "PAUSED" or "INFO" overlay based on overlay_type.
# Optionally renders a logo and an icon.
# If overlay_type is "info", additional instructions and tips are displayed.
def draw_overlay(screen, overlay_type, font, logo=None, icon=None):
    width, height = screen.get_size()

    # Dim background
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    # Optional logo (top center)
    if logo:
        screen.blit(logo, (width // 2 - logo.get_width() // 2, 30))

    # Icon (top-left)
    if icon:
        screen.blit(icon, (20, 20))

    # Title
    title_text = "PAUSED" if overlay_type == "pause" else "INFO"
    title_surface = font.render(title_text, True, (255, 255, 255))
    screen.blit(title_surface, (width // 2 - title_surface.get_width() // 2, 120))

    # Info lines
    if overlay_type == "info":
        info_font = pygame.font.SysFont("Arial", 24)
        lines = [
            "🕹️  Controls:",
            "- SPACE: Jump",
            "- P: Pause",
            "- I: Toggle Info Screen",
            "- ESC: Quit Game",
            "",
            "💡 Tip: Land on green platforms.",
            "Avoid red enemies!",
        ]
        for i, line in enumerate(lines):
            line_surface = info_font.render(line, True, (255, 255, 255))
            screen.blit(line_surface, (60, 200 + i * 30))

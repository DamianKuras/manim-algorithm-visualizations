from manim import *


class BaseVisualization(Scene):

    # Constants for font and colors
    FONT_PATH = "./fonts/Excalifont-Regular.woff2"
    FONT_NAME = "Excalifont"
    BG_COLOR = "#374151"
    TEXT_COLOR = WHITE
    HIGHLIGHT_COLOR = YELLOW
    MATCH_COLOR = GREEN
    MISMATCH_COLOR = RED
    ACCENT_COLOR = BLUE

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        register_font(self.FONT_PATH)  # Register font in the constructor

    def setup_scene(self, title_text, title_font_size=48):
        """
        Sets up the scene with a title and a background color.
        """
        self.camera.background_color = self.BG_COLOR
        title = Text(
            title_text,
            font=self.FONT_NAME,
            font_size=title_font_size,
            color=self.TEXT_COLOR,
        ).to_edge(UP, buff=0.5)
        self.add(title)

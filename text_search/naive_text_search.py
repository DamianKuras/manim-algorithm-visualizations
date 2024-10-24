from manim import *

# Constants for font and colors
FONT_PATH = "./fonts/Excalifont-Regular.woff2"
FONT_NAME = "Excalifont"
BG_COLOR = "#374151"
TEXT_COLOR = WHITE
HIGHLIGHT_COLOR = YELLOW
MATCH_COLOR = GREEN
MISMATCH_COLOR = RED
WINDOW_COLOR = BLUE


class NaiveSearch(Scene):
    """
    A Manim animation that visualizes the Naive Search Algorithm.
    """

    def setup_scene(self, title_text, title_font_size=48):
        """
        Sets up the scene with a title and a background color.
        """
        register_font(FONT_PATH)
        self.camera.background_color = BG_COLOR
        title = Text(
            title_text, font=FONT_NAME, font_size=title_font_size, color=TEXT_COLOR
        ).to_edge(UP, buff=0.5)
        self.add(title)

    def display_labeled_text(self, label, content, position, font_size=36, buff=0.5):
        """
        Utility to create and display labeled text
        """
        label_mobject = (
            Text(label, font=FONT_NAME, font_size=font_size, color=TEXT_COLOR)
            .to_edge(LEFT, buff=buff)
            .shift(position)
        )
        content_mobject = VGroup(
            *[
                Text(char, font=FONT_NAME, font_size=font_size + 12, color=TEXT_COLOR)
                for char in content
            ]
        )
        content_mobject.arrange(RIGHT, buff=0.3).next_to(label_mobject, RIGHT, buff=0.5)
        self.add(label_mobject, content_mobject)
        return content_mobject

    def animate_match_or_mismatch(
        self, text_mobject, pattern_mobject, index_text, index_pattern, match=True
    ):
        """
        Animates the comparison of a character between text and pattern.
        """
        color = MATCH_COLOR if match else MISMATCH_COLOR
        self.play(
            text_mobject[index_text].animate.set_color(color),
            pattern_mobject[index_pattern].animate.set_color(color),
            run_time=0.3,
        )

    def reset_colors(self, text_mobject, pattern_mobject, start_idx, pattern_len):
        """Resets the color of text and pattern characters to white."""
        for j in range(pattern_len):
            text_mobject[start_idx + j].set_color(WHITE)
            pattern_mobject[j].set_color(WHITE)

    def construct(self):
        self.setup_scene("Naive Search Algorithm")

        text = "ABABABC"
        pattern = "ABC"
        pattern_len = len(pattern)
        text_mobject = self.display_labeled_text("Text:", text, UP * 1)
        pattern_mobject = self.display_labeled_text("Pattern:", pattern, DOWN * 2)

        # Perform the Naive Search
        for i in range(len(text) - pattern_len + 1):
            # Highlight the current window of comparison in the text
            window_highlight = SurroundingRectangle(
                text_mobject[i : i + pattern_len],
                color=BLUE,
                buff=0.2,
                stroke_width=2.5,
            )
            self.play(Create(window_highlight))

            # Compare each letter of the pattern with the current window in the text
            matched = True
            for j in range(pattern_len):
                if text[i + j] != pattern[j]:
                    self.animate_match_or_mismatch(
                        text_mobject, pattern_mobject, i + j, j, match=False
                    )
                    self.wait(0.5)
                    matched = False
                    break

                self.animate_match_or_mismatch(
                    text_mobject, pattern_mobject, i + j, j, match=True
                )

            self.wait(0.5)

            if matched:
                # Display match found if the entire pattern matches
                match_text = (
                    Text("Match Found!", font=FONT_NAME, color=TEXT_COLOR)
                    .scale(0.75)
                    .next_to(text_mobject, RIGHT * 2)
                )
                self.play(Write(match_text))
                self.wait(1)
                self.play(FadeOut(match_text))

            # Reset colors for the next window
            self.reset_colors(text_mobject, pattern_mobject, i, pattern_len)

            self.play(FadeOut(window_highlight))

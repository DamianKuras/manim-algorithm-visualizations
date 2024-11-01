from manim import *

from utils.base_visualization import BaseVisualization
from utils.visual_array import VisualArray


class KMPAlgorithm(BaseVisualization):

    def construct(self):
        # Set background color
        self.setup_scene("KMP Search Algorithm")

        # Text and Pattern Titles
        text_title = (
            Text("Text:", font=self.FONT_NAME, font_size=30, color=self.TEXT_COLOR)
            .to_edge(LEFT, buff=0.75)
            .shift(UP * 1)
        )

        pattern_title = (
            Text("Pattern:", font=self.FONT_NAME, font_size=30, color=self.TEXT_COLOR)
            .to_edge(LEFT, buff=0.75)
            .shift(DOWN * 0)
        )
        lps_title = (
            Text("LPS Table:", font=self.FONT_NAME, font_size=30, color=self.TEXT_COLOR)
            .to_edge(LEFT, buff=0.75)
            .shift(DOWN * 1)
        )

        # Example text and pattern
        text = "ABADABACDABABCABAB"
        pattern = "ABABCABAB"
        lps = [0, 0, 1, 2, 0, 1, 2, 3, 4]

        # Create and display the text, pattern, and LPS table
        text_mobject = VisualArray(
            list(text),
            font_name=self.FONT_NAME,
            font_size=24,
            element_color=self.TEXT_COLOR,
            border_color=self.ACCENT_COLOR,
            cell_width=0.6,
            cell_height=0.6,
        ).next_to(text_title, RIGHT, buff=1)
        pattern_mobject = VisualArray(
            list(pattern),
            font_name=self.FONT_NAME,
            font_size=24,
            element_color=self.TEXT_COLOR,
            border_color=self.ACCENT_COLOR,
            cell_width=0.6,
            cell_height=0.6,
        ).next_to(pattern_title, RIGHT, buff=1)
        lps_mobject = VisualArray(
            lps,
            font_name=self.FONT_NAME,
            font_size=24,
            element_color=self.TEXT_COLOR,
            border_color=self.ACCENT_COLOR,
            cell_width=0.6,
            cell_height=0.6,
        ).next_to(lps_title, RIGHT, buff=0.5)

        # Display the text, pattern, and LPS table
        self.add(
            text_title,
            text_mobject,
            pattern_title,
            pattern_mobject,
            lps_title,
            lps_mobject,
        )

        # Perform KMP search
        i, j = 0, 0

        while i < len(text):
            # Highlight current character in the text and pattern

            # Play the highlight animations
            self.play(
                text_mobject.get_highlight_element_animation(
                    i, color=self.HIGHLIGHT_COLOR
                ),
                pattern_mobject.get_highlight_element_animation(
                    j, color=self.HIGHLIGHT_COLOR
                ),
            )

            if text[i] == pattern[j]:
                i += 1
                j += 1
                # Highlight the matching letters
                self.play(
                    text_mobject.get_highlight_element_animation(
                        i - 1, self.MATCH_COLOR
                    ),
                    pattern_mobject.get_highlight_element_animation(
                        j - 1, self.MATCH_COLOR
                    ),
                )
                if j == len(pattern):
                    match_text = Text(
                        "Match Found!", font=self.FONT_NAME, font_size=30
                    ).next_to(text_mobject, DOWN)
                    self.play(Write(match_text))
                    self.wait(1)
                    self.play(FadeOut(match_text))
                    j = lps[j - 1]  # Backtrack using LPS

            else:
                # Mismatch
                if j != 0:
                    self.play(
                        text_mobject.get_highlight_element_animation(
                            i, self.MISMATCH_COLOR
                        ),
                        pattern_mobject.get_highlight_element_animation(
                            j, self.MISMATCH_COLOR
                        ),
                    )
                    # Wait for 0.5 seconds to show the mismatch
                    self.wait(0.5)
                    # Highlight corresponding LPS value for backtracking
                    lps_highlight = lps_mobject.get_highlight_element_animation(
                        j - 1, color=self.ACCENT_COLOR
                    )
                    self.play(lps_highlight)

                    # Backtrack j using the LPS table
                    new_j = lps[j - 1]

                    self.play(
                        pattern_mobject.get_highlight_element_animation(
                            k, self.TEXT_COLOR
                        )
                        for k in range(new_j, j + 1)
                    )
                    j = new_j
                    # Fadeout lps highlight after backtracking
                    lps_mobject.reset_colors()

                    self.play(
                        pattern_mobject.get_highlight_element_animation(
                            j, self.HIGHLIGHT_COLOR
                        )
                    )

                else:
                    self.play(
                        text_mobject.get_highlight_element_animation(
                            i, self.MISMATCH_COLOR
                        ),
                        pattern_mobject.get_highlight_element_animation(
                            j, self.MISMATCH_COLOR
                        ),
                    )
                    # Move to the next character in the text
                    i += 1

        self.wait(2)

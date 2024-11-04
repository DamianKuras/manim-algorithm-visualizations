from manim import *

from utils.base_visualization import BaseVisualization
from utils.visual_array import VisualArray


class KMPAlgorithm(BaseVisualization):
    """
    A Manim animation that visualizes the KMP text search algorithm.
    """

    def create_labeled_array(self, title, elements, buffer=0.0, shift_val=ORIGIN):
        """
        Creates a labeled array with a title and elements for visualization.
        """
        label_text = (
            Text(title, font=self.FONT_NAME, font_size=30, color=self.TEXT_COLOR)
            .to_edge(LEFT, buff=0.75)
            .shift(shift_val)
        )

        array = VisualArray(
            elements,
            font_name=self.FONT_NAME,
            font_size=24,
            element_color=self.TEXT_COLOR,
            border_color=self.ACCENT_COLOR,
            cell_width=0.5,
            cell_height=0.5,
        ).next_to(label_text, RIGHT, buff=buffer)
        return label_text, array

    def highlight_current_characters(self, i, j, text_mobject, pattern_mobject, color):
        """
        Highlights the current characters in the text and pattern during comparison
        """
        self.play(
            text_mobject.get_change_element_color_animation(i, color=color),
            pattern_mobject.get_change_element_color_animation(j, color=color),
        )

    def show_match_found(self, pattern_mobject):
        """
        Displays a message indicating a successful pattern match.
        """
        match_text = Text("Match Found!", font=self.FONT_NAME, font_size=30).next_to(
            pattern_mobject, RIGHT, buff=1
        )
        self.play(Write(match_text))
        self.wait(1)
        self.play(FadeOut(match_text))

    def backtrack(self, i, j, lps, lps_mobject, text_mobject, pattern_mobject):
        """
        Performs backtracking in the KMP algorithm using the LPS (Longest Prefix Suffix) table.
        """
        # Highlight corresponding LPS value for backtracking
        self.play(
            lps_mobject.get_change_element_color_animation(
                j - 1, color=self.HIGHLIGHT_COLOR
            )
        )
        new_j = lps[j - 1]
        # Unhighlight previously matched text characters that dont match after backtracking
        self.play(
            text_mobject.get_change_element_color_animation(k, color=self.TEXT_COLOR)
            for k in range(i - j, i - j + (j - new_j))
        )
        self.play(
            pattern_mobject.get_change_element_color_animation(k, self.TEXT_COLOR)
            for k in range(new_j, j + 1)
        )
        lps_mobject.reset_colors()

        return new_j

    def perform_kmp_search(
        self, text, pattern, lps, text_mobject, pattern_mobject, lps_mobject
    ):
        """
        Executes the KMP search algorithm on the given text and pattern.
        """
        i, j = 0, 0
        while i < len(text):
            self.highlight_current_characters(
                i, j, text_mobject, pattern_mobject, self.HIGHLIGHT_COLOR
            )
            if text[i] == pattern[j]:
                self.highlight_current_characters(
                    i, j, text_mobject, pattern_mobject, self.MATCH_COLOR
                )
                i += 1
                j += 1
                if j == len(pattern):
                    self.show_match_found(pattern_mobject)
                    break
            else:
                self.highlight_current_characters(
                    i, j, text_mobject, pattern_mobject, self.MISMATCH_COLOR
                )
                # j = self.handle_mismatch(i, j, lps)
                if j != 0:
                    j = self.backtrack(
                        i, j, lps, lps_mobject, text_mobject, pattern_mobject
                    )
                else:
                    # if no more backtracking can be made start matching from next character in text
                    text_mobject.reset_colors()
                    i += 1

    def construct(self):
        # Set background color
        self.setup_scene("KMP Search Algorithm")

        # Example text and pattern
        text = "ABADABACDABABCABAB"
        pattern = "ABABCABAB"
        lps = [0, 0, 1, 2, 0, 1, 2, 3, 4]

        text_title, text_mobject = self.create_labeled_array(
            "Text:", list(text), 1.5, UP
        )
        pattern_title, pattern_mobject = self.create_labeled_array(
            "Pattern:", list(pattern), 1
        )
        lps_title, lps_mobject = self.create_labeled_array("LPS Table:", lps, 0.5, DOWN)
        # Display the text, pattern, and LPS table
        self.add(
            text_title,
            text_mobject,
            pattern_title,
            pattern_mobject,
            lps_title,
            lps_mobject,
        )

        self.perform_kmp_search(
            text, pattern, lps, text_mobject, pattern_mobject, lps_mobject
        )

        self.wait(2)

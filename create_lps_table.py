from manim import *

from utils.base_visualization import BaseVisualization
from utils.visual_array import VisualArray


class CreateLPSTable(BaseVisualization):
    """
    A Manim animation that visualizes creation of the LPS table.
    """

    def create_labeled_array(
        self, elements, label_text, position, shift_val=ORIGIN, buff=0
    ):
        """
        Creates a labeled array with a title and elements for visualization.
        """
        array = VisualArray(
            elements,
            font_name=self.FONT_NAME,
            font_size=48,
            element_color=self.TEXT_COLOR,
            border_color=self.ACCENT_COLOR,
        )
        label = Text(
            label_text, font=self.FONT_NAME, font_size=36, color=self.TEXT_COLOR
        )
        array.to_edge(position, buff=buff).shift(shift_val)
        label.next_to(array, LEFT, buff=0.5)
        self.add(label, array)
        return array, label

    def highlight_prefix_suffix(self, array, prefix_len, current_idx):
        """
        Highlights the prefix and suffix in the pattern array as part of the LPS computation.
        """
        for k in range(prefix_len):
            self.play(
                array.get_change_element_color_animation(k, color=self.MATCH_COLOR),
                run_time=0.1,
            )
        for k in range(current_idx - prefix_len + 1, current_idx + 1):
            self.play(
                array.get_change_element_color_animation(k, color=self.ACCENT_COLOR),
                run_time=0.1,
            )

    def construct(self):
        self.setup_scene("Creation of the LPS Table")

        pattern = "ABABCABAB"
        pattern_array, pattern_label = self.create_labeled_array(
            pattern, "Pattern:", position=UP, buff=2.5, shift_val=RIGHT
        )
        lps = [0] * len(pattern)
        lps_array, lps_label = self.create_labeled_array(
            lps, "LPS Table:", position=DOWN, buff=2.5, shift_val=RIGHT
        )

        i, j = 1, 0  # Start from the second character in the pattern

        while i < len(pattern):
            pattern_array.reset_colors()
            lps_array.reset_colors()

            self.play(
                pattern_array.get_change_element_color_animation(
                    i, color=self.HIGHLIGHT_COLOR
                )
            )
            self.wait(0.3)

            if pattern[i] == pattern[j]:
                j += 1
                self.highlight_prefix_suffix(pattern_array, j, i)

                # Update LPS table
                self.play(
                    lps_array.get_update_element_animation(
                        i, j, color=self.ACCENT_COLOR
                    )
                )
                i += 1
            else:
                if j != 0:
                    j = lps[j - 1]
                else:
                    self.play(
                        lps_array.get_update_element_animation(
                            i, 0, color=self.MISMATCH_COLOR
                        )
                    )
                    i += 1

        self.wait(2)  # Pause to display the completed LPS table

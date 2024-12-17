from manim import *
from utils.base_visualization import BaseVisualization
from utils.visual_array import VisualArray
from utils.text_helpers import wrap_text


class BoyerMooreAlgorithm(BaseVisualization):
    """
    A Manim animation that visualizes the Boyer-Moore text search algorithm.
    """

    CELL_WIDTH = 0.5
    CELL_HEIGHT = 0.5
    TITLE_FONT_SIZE = 30
    INFO_FONT_SIZE = 22
    VISUAL_ARRAY_FONT_SIZE = 24

    def __init__(self):
        super().__init__()
        self.graying_out_executed = False
        self.text = "AAAZBBBAAAABABCA"
        self.pattern = "ABCA"
        self.pattern_len = len(self.pattern)
        self.text_len = len(self.text)
        self.bad_char_shift = self.create_bad_character_table(self.pattern)
        self.good_suffix_shift = self.create_good_suffix_table(self.pattern)
        self.previously_matched = set()
        self.previously_mismatched = set()
        self.pattern_pos = 0
        self.text_pos = 0

    def create_labeled_array(self, title, elements, buffer=0.0, shift_val=ORIGIN):
        """
        Creates a labeled array with a title and elements for visualization.
        """
        label_text = (
            Text(
                title,
                font=self.FONT_NAME,
                font_size=self.TITLE_FONT_SIZE,
                color=self.TEXT_COLOR,
            )
            .to_edge(LEFT)
            .shift(shift_val)
        )

        array = VisualArray(
            elements,
            font_name=self.FONT_NAME,
            font_size=self.VISUAL_ARRAY_FONT_SIZE,
            element_color=self.TEXT_COLOR,
            border_color=self.ACCENT_COLOR,
            cell_width=self.CELL_WIDTH,
            cell_height=self.CELL_HEIGHT,
        ).next_to(label_text, RIGHT, buff=buffer)
        return label_text, array

    def change_char_colors(self, text_idx, pattern_idx, color):
        """
        Changes the color of characters in the text and pattern.
        """
        self.play(
            self.text_mobject.get_change_element_color_animation(text_idx, color=color),
            self.pattern_mobject.get_change_element_color_animation(
                pattern_idx, color=color
            ),
        )

    def show_match_found(self):
        """
        Displays a message indicating a successful pattern match below text mobject.
        """
        self.play(FadeOut(self.matching_window))
        match_text = self.create_info_message(
            "Match Found!",
        )
        self.play(FadeIn(match_text))
        self.wait(1)
        self.play(FadeOut(match_text))

    def create_info_message(self, message, direction=DOWN, buff=2.5):
        """
        Create a message below the target mobject.
        """
        text = Text(
            message,
            font=self.FONT_NAME,
            font_size=self.INFO_FONT_SIZE,
            color=self.TEXT_COLOR,
        ).next_to(self.text_mobject, direction, buff)
        return text

    def show_bad_char_shift(
        self,
        shift_value,
        character,
    ):
        """
        Visualize the application of the Bad Character Rule during the Boyer-Moore string search algorithm.
        """
        if 0 < shift_value < self.pattern_len:
            shift_text = self.create_info_message(
                f"Bad Character Rule: Shift by {shift_value}\n"
                f'Shift pattern up to rightmost occurrence of character "{character}"',
            )
        elif shift_value < 0:
            shift_text = self.create_info_message(
                f"Bad Character Rule: Shift by {shift_value}\n"
                + wrap_text(
                    'If the rightmost occurrence of char in pattern is to the right of the mismatched character(i.e. within that part of pattern that we have already passed we would have to move pattern backwards to align the two known occurrence of char. We would not want to do this. In this case we say that shift distance is "worthless" and slide pattern forward by 1.',
                    75,
                ),
            )
        else:
            shift_text = self.create_info_message(
                f"Bad Character Rule: Shift by {shift_value}\n"
                "No character in pattern matches current character in text.\n"
                "Move pattern past current character in text.",
            )

        shifted_projection = self.pattern_mobject.copy()
        shifted_projection.reset_colors()
        self.play(Write(shift_text))
        self.wait(1)
        self.play(
            FadeIn(shifted_projection),
            shifted_projection.animate.shift(
                RIGHT * shift_value * self.CELL_WIDTH
            ).shift(DOWN),
            duration=2,
        )
        self.wait(1)
        self.play(FadeOut(shift_text), FadeOut(shifted_projection))

    def show_good_suffix_shift(self, shift_value, matched_characters):
        """
        Visualize the application of the Good Suffix Rule during the Boyer-Moore string search algorithm.
        """
        shift_text = self.create_info_message(
            f"Good Suffix Rule: Shift pattern by {shift_value}.\n"
            "Align the matched suffix with its leftmost occurrence.\n",
        )

        suffix_start = self.pattern_len - matched_characters
        suffix_end = suffix_start + matched_characters

        prefix_start = suffix_start - shift_value
        prefix_end = suffix_end - shift_value

        suffix_rect = SurroundingRectangle(
            VGroup(self.pattern_mobject.element_cells[suffix_start:suffix_end]),
            color=self.MATCH_COLOR,
            buff=-0.1,
        )
        prefix_rect = SurroundingRectangle(
            VGroup(self.pattern_mobject.element_cells[prefix_start:prefix_end]),
            color=self.MATCH_COLOR,
            buff=-0.1,
        )

        shifted_projection = self.pattern_mobject.copy()
        shifted_projection.reset_colors()
        shifted_projection.shift(RIGHT * shift_value * self.CELL_WIDTH).shift(DOWN)

        self.play(
            Write(shift_text),
            Create(shifted_projection),
            Create(suffix_rect),
            Create(prefix_rect),
        )
        self.wait(1)

        self.play(
            FadeOut(shift_text),
            FadeOut(shifted_projection),
            FadeOut(suffix_rect),
            FadeOut(prefix_rect),
        )

    def create_matching_window(self, text_pos, pattern_pos):
        rect = SurroundingRectangle(
            VGroup(
                self.text_mobject.element_cells[text_pos],
                self.pattern_mobject.element_cells[pattern_pos],
            ),
            color=ORANGE,
        )
        return rect

    def gray_out_skipped_characters(
        self,
        start,
        end,
    ):
        """
        Grays out the characters in the text that were skipped and never matched.
        """
        if start >= end:
            return
        for i in range(start, end):
            if i in self.previously_matched or i in self.previously_mismatched:
                continue
            self.play(
                self.text_mobject.get_change_element_color_animation(i, color=GRAY),
                run_time=0.2,
            )
        # show info message the first time graying out gets executed
        if not self.graying_out_executed:
            explanation_text = self.create_info_message(
                "Grayed characters in text are skipped during matching process",
            )

            self.play(FadeIn(explanation_text))
            self.wait(2)
            self.play(FadeOut(explanation_text))
            self.graying_out_executed = True

    def create_bad_character_table(self, pattern):
        """
        Creates a bad character shift table as a dictionary
        """
        bad_char_shift = {}
        for index, c in enumerate(pattern):
            bad_char_shift[c] = index

        return bad_char_shift

    def create_good_suffix_table(self, pattern):
        """
        Creates the good suffix shift table.
        """
        m = len(pattern)
        goodSuffixShift = [0] * (m + 1)
        borderPos = [0] * (m + 1)
        i = m
        j = m + 1
        borderPos[i] = j

        while i > 0:
            while j <= m and pattern[i - 1] != pattern[j - 1]:
                if goodSuffixShift[j] == 0:
                    goodSuffixShift[j] = j - i
                j = borderPos[j]
            i = i - 1
            j = j - 1
            borderPos[i] = j

        for k in range(m + 1):
            if goodSuffixShift[k] == 0:
                goodSuffixShift[k] = j
            if k == j:
                j = borderPos[j]

        return goodSuffixShift

    def handle_matched_characters(self, text_idx, pattern_idx):
        self.change_char_colors(text_idx, pattern_idx, self.MATCH_COLOR)
        self.previously_matched.add(text_idx)
        if pattern_idx - 1 >= 0:
            self.play(self.matching_window.animate.shift(LEFT * 0.5))
        else:
            self.play(FadeOut(self.matching_window))

    def handle_mismatch(
        self,
        text_idx,
        pattern_idx,
    ):
        self.change_char_colors(text_idx, pattern_idx, self.MISMATCH_COLOR)
        self.previously_mismatched.add(text_idx)

    def unhighlight_matched_and_mismatched(self, range_start, range_end):
        to_unhighlight = []
        for i in range(range_start, range_end):
            if i in self.previously_matched or i in self.previously_mismatched:
                to_unhighlight.append(i)
        if len(to_unhighlight) > 0:
            self.play(
                self.text_mobject.get_change_element_color_animation(k, self.TEXT_COLOR)
                for k in to_unhighlight
            )
        self.pattern_mobject.reset_colors()

    def handle_shift(self, shift_value, matched_characters):
        shift_text = self.create_info_message(f"Total shift value: {shift_value}")
        self.play(
            FadeIn(shift_text),
            self.pattern_mobject.animate.shift(RIGHT * shift_value * 0.5),
            self.matching_window.animate.shift(
                RIGHT * (shift_value + matched_characters) * 0.5
            ),
        )
        self.wait(1)
        self.play(FadeOut(shift_text))

    def perform_boyer_moore_search(
        self,
    ):
        """
        Executes the Boyer-Moore search algorithm on the given text and pattern.
        """
        i = 0

        self.play(Create(self.matching_window))
        while i <= self.text_len - self.pattern_len:
            j = self.pattern_len - 1  # Start matching pattern from the end

            matched_characters = 0

            while j >= 0 and self.pattern[j] == self.text[i + j]:  # Matching
                self.handle_matched_characters(i + j, j)
                j -= 1
                matched_characters += 1

            if j < 0:  # Fully matched
                self.show_match_found()
                return
            else:  # Mismatch

                bad_char_shift_value = j - self.bad_char_shift.get(self.text[i + j], -1)
                good_suffix_shift_value = self.good_suffix_shift[j + 1]
                self.handle_mismatch(i + j, j)
                self.show_bad_char_shift(bad_char_shift_value, self.text[i + j])

                if matched_characters > 0:
                    self.show_good_suffix_shift(
                        good_suffix_shift_value,
                        matched_characters,
                    )

                shift_value = max(1, max(bad_char_shift_value, good_suffix_shift_value))
                self.gray_out_skipped_characters(i, min(i + j, i + shift_value))
                self.unhighlight_matched_and_mismatched(i, i + self.pattern_len)
                self.handle_shift(shift_value, matched_characters)

                i += shift_value
                matched_characters = 0

    def construct(self):
        self.setup_scene("Boyer-Moore Search Algorithm")

        text_title, self.text_mobject = self.create_labeled_array(
            "Text:", list(self.text), 1.5, UP * 2
        )
        pattern_title, self.pattern_mobject = self.create_labeled_array(
            "Pattern:", list(self.pattern), 1, UP * 1
        )

        shift_title = Text(
            "Shift: ",
            font=self.FONT_NAME,
            font_size=self.TITLE_FONT_SIZE,
            color=self.TEXT_COLOR,
        ).to_edge(LEFT)

        self.add(
            text_title,
            self.text_mobject,
            pattern_title,
            self.pattern_mobject,
            shift_title,
        )
        self.matching_window = self.create_matching_window(
            0 + self.pattern_len - 1,
            self.pattern_len - 1,
        )
        self.perform_boyer_moore_search()

        self.wait(2)

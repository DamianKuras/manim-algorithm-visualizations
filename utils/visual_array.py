from manim import *


class VisualArray(VGroup):
    """
    A Manim-based array that allows updating and highlighting elements.
    """

    def __init__(
        self,
        elements,
        font_name,
        font_size,
        element_color,
        border_color,
        cell_width=1.0,
        cell_height=1.0,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.element_cells = VGroup()

        for e in elements:
            # Create text for the element
            text = Text(
                str(e), font=font_name, font_size=font_size, color=element_color
            )

            # Create a cell (rectangle) around the text with fixed width and height
            cell = Rectangle(width=cell_width, height=cell_height, color=border_color)
            text.move_to(cell.get_center())

            # Group the text and cell together as a single element
            element_cell = VGroup(cell, text)
            self.element_cells.add(element_cell)

        # Arrange the cells to form a continuous array
        self.element_cells.arrange(RIGHT, buff=0)
        self.add(self.element_cells)

        self.default_color = element_color

    def get_update_element_animation(self, index, value, color):
        """
        Returns an animation that updates the element at the specified index with a new value and color.
        """
        new_text = Text(
            str(value),
            font=self.element_cells[index][1].font,
            font_size=self.element_cells[index][1].font_size,
            color=color,
        )
        new_text.move_to(self.element_cells[index][0].get_center())
        return ReplacementTransform(self.element_cells[index][1], new_text)

    def get_change_element_color_animation(self, index, color):
        """
        Returns an animation to change color of an element at the specified index.
        """
        return self.element_cells[index][1].animate.set_color(color)

    def reset_colors(self):
        """
        Resets the color of all elements in the array to their default color.
        """
        for elem_cell in self.element_cells:
            elem_cell[1].set_color(self.default_color)

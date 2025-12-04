"""
GuessRow widget for Mastermind GUI.

Displays a single guess row with color slots and bulls/cows feedback.
"""

import tkinter as tk
from typing import List
from ..utils import get_color_hex


class GuessRow(tk.Frame):
    """
    A widget that displays a guess with color slots and feedback.

    Shows the guessed colors and the bulls/cows feedback for that guess.
    """

    def __init__(self, parent: tk.Widget, code_length: int):
        """
        Initialize the GuessRow widget.

        Args:
            parent: Parent widget
            code_length: Number of color slots in the code
        """
        super().__init__(parent, relief=tk.RIDGE, borderwidth=2, bg="#F0F0F0")

        self.code_length = code_length
        self.color_labels = []
        self.feedback_label = None

        self._create_widgets()

    def _create_widgets(self):
        """Create the color slots and feedback area."""
        # Create frame for color slots
        colors_frame = tk.Frame(self, bg="#F0F0F0")
        colors_frame.pack(side=tk.LEFT, padx=10, pady=5)

        # Create color slot labels
        for i in range(self.code_length):
            label = tk.Label(
                colors_frame,
                width=4,
                height=2,
                relief=tk.SUNKEN,
                borderwidth=2,
                bg="#CCCCCC",
                text="",
            )
            label.pack(side=tk.LEFT, padx=2)
            self.color_labels.append(label)

        # Create feedback area
        self.feedback_label = tk.Label(
            self,
            width=25,
            height=2,
            relief=tk.SUNKEN,
            borderwidth=2,
            bg="white",
            text="",
            font=("Arial", 10),
        )
        self.feedback_label.pack(side=tk.LEFT, padx=10, pady=5)

    def set_guess(self, colors: List[str]):
        """
        Display the guessed colors.

        Args:
            colors: List of color names to display
        """
        for i, color in enumerate(colors):
            if i < len(self.color_labels):
                self.color_labels[i].config(bg=get_color_hex(color))

    def set_feedback(self, bulls: int, cows: int):
        """
        Display the bulls and cows feedback.

        Args:
            bulls: Number of bulls (correct color and position)
            cows: Number of cows (correct color, wrong position)
        """
        feedback_parts = []

        if bulls > 0:
            feedback_parts.append(f"Bulls: {bulls} ●")

        if cows > 0:
            feedback_parts.append(f"Cows: {cows} ○")

        if bulls == 0 and cows == 0:
            feedback_text = "No matches"
        else:
            feedback_text = " | ".join(feedback_parts)

        self.feedback_label.config(
            text=feedback_text,
            fg="#2C3E50",
            font=("Arial", 10, "bold"),
        )

    def clear(self):
        """Clear the row (reset to empty state)."""
        for label in self.color_labels:
            label.config(bg="#CCCCCC")
        self.feedback_label.config(text="")

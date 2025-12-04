"""
Game board screen for Mastermind GUI.

Main gameplay interface where players make guesses and see feedback.
"""

import tkinter as tk
from tkinter import messagebox
from typing import TYPE_CHECKING, List, Optional

from ..widgets.colorpicker import ColorPicker
from ..widgets.row import GuessRow
from ..utils import (
    get_available_colors,
    get_color_hex,
    colors_to_symbols,
    get_alphabet_for_colors,
)
from ...engine import Rules
from ...game import Game

if TYPE_CHECKING:
    from ..app import MastermindApp


class GameBoardScreen(tk.Frame):
    """
    Main game board screen for gameplay.
    """

    def __init__(
        self,
        parent: tk.Widget,
        app: "MastermindApp",
        config: dict,
        secret: Optional[str] = None,
    ):
        """
        Initialize the game board screen.

        Args:
            parent: Parent widget
            app: Main application controller
            config: Game configuration dictionary
            secret: Optional secret code (for PvP mode)
        """
        super().__init__(parent, bg="#2C3E50")
        self.app = app
        self.config = config

        self.available_colors = get_available_colors(config["num_colors"])
        self.current_guess: List[str] = []
        self.guess_rows: List[GuessRow] = []

        # Create game instance
        alphabet = get_alphabet_for_colors(config["num_colors"])
        rules = Rules(
            length=config["length"],
            alphabet=alphabet,
            allow_duplicates=config["allow_duplicates"],
        )

        self.game = Game(
            rules=rules,
            mode=config["mode"],
            max_attempts=config["max_attempts"],
            secret=secret,
        )

        # Determine player name
        if config["mode"] == "pvp":
            self.player_name = config["player2_name"]
        else:
            self.player_name = config["player1_name"]

        self._create_widgets()

    def _create_widgets(self):
        """Create the UI widgets."""
        # Header
        header_frame = tk.Frame(self, bg="#34495E")
        header_frame.pack(fill=tk.X, pady=10)

        # Player name and attempt counter
        info_label = tk.Label(
            header_frame,
            text=(
                f"Player: {self.player_name}  |  "
                f"Attempt: {self.game.attempts_used + 1}/{self.game.max_attempts}"
            ),
            font=("Arial", 16, "bold"),
            bg="#34495E",
            fg="white",
        )
        info_label.pack(pady=10)
        self.info_label = info_label

        # Help text explaining feedback
        help_text = tk.Label(
            header_frame,
            text=(
                "● Bulls = Correct color in correct position  |  "
                "○ Cows = Correct color in wrong position"
            ),
            font=("Arial", 10),
            bg="#34495E",
            fg="#ECF0F1",
        )
        help_text.pack(pady=(0, 10))

        # Main content frame
        content_frame = tk.Frame(self, bg="#2C3E50")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20)

        # Past guesses area
        guesses_label = tk.Label(
            content_frame,
            text="Past Guesses:",
            font=("Arial", 14, "bold"),
            bg="#2C3E50",
            fg="white",
        )
        guesses_label.pack(anchor=tk.W, pady=(10, 5))

        # Scrollable frame for guess history
        history_frame = tk.Frame(
            content_frame,
            bg="white",
            relief=tk.SUNKEN,
            borderwidth=2,
        )
        history_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Canvas and scrollbar for scrolling
        canvas = tk.Canvas(history_frame, bg="white", height=200)
        scrollbar = tk.Scrollbar(
            history_frame,
            orient="vertical",
            command=canvas.yview,
        )
        self.scrollable_frame = tk.Frame(canvas, bg="white")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.history_canvas = canvas

        # Current guess area
        current_label = tk.Label(
            content_frame,
            text="Current Guess:",
            font=("Arial", 14, "bold"),
            bg="#2C3E50",
            fg="white",
        )
        current_label.pack(anchor=tk.W, pady=(15, 5))

        # Current guess display
        guess_display_frame = tk.Frame(
            content_frame,
            bg="white",
            relief=tk.RAISED,
            borderwidth=2,
        )
        guess_display_frame.pack(fill=tk.X, pady=5)

        self.guess_labels = []
        for i in range(self.config["length"]):
            label = tk.Label(
                guess_display_frame,
                width=6,
                height=3,
                relief=tk.SUNKEN,
                borderwidth=2,
                bg="#CCCCCC",
                text=str(i + 1),
                font=("Arial", 12, "bold"),
            )
            label.pack(side=tk.LEFT, padx=5, pady=10)
            self.guess_labels.append(label)

        # Color picker
        picker_label = tk.Label(
            content_frame,
            text="Select Colors:",
            font=("Arial", 14, "bold"),
            bg="#2C3E50",
            fg="white",
        )
        picker_label.pack(anchor=tk.W, pady=(15, 5))

        picker_frame = tk.Frame(
            content_frame,
            bg="white",
            relief=tk.RAISED,
            borderwidth=2,
        )
        picker_frame.pack(fill=tk.X, pady=5)

        self.color_picker = ColorPicker(
            picker_frame,
            self.available_colors,
            self._on_color_selected,
        )
        self.color_picker.pack(pady=10)

        # Buttons
        buttons_frame = tk.Frame(content_frame, bg="#2C3E50")
        buttons_frame.pack(pady=15)

        # Clear button
        clear_button = tk.Button(
            buttons_frame,
            text="Clear",
            font=("Arial", 12, "bold"),
            bg="#E74C3C",
            fg="white",
            command=self._on_clear,
            width=12,
            height=2,
        )
        clear_button.pack(side=tk.LEFT, padx=10)

        # Submit button
        self.submit_button = tk.Button(
            buttons_frame,
            text="Submit Guess",
            font=("Arial", 12, "bold"),
            bg="#27AE60",
            fg="white",
            command=self._on_submit,
            width=15,
            height=2,
            state=tk.DISABLED,
        )
        self.submit_button.pack(side=tk.LEFT, padx=10)

    def _on_color_selected(self, color: str):
        """Handle color selection."""
        if len(self.current_guess) < self.config["length"]:
            self.current_guess.append(color)
            self._update_guess_display()

    def _update_guess_display(self):
        """Update the current guess display."""
        for i, label in enumerate(self.guess_labels):
            if i < len(self.current_guess):
                label.config(bg=get_color_hex(self.current_guess[i]), text="")
            else:
                label.config(bg="#CCCCCC", text=str(i + 1))

        # Enable submit if guess is complete
        if len(self.current_guess) == self.config["length"]:
            self.submit_button.config(state=tk.NORMAL)
        else:
            self.submit_button.config(state=tk.DISABLED)

    def _on_clear(self):
        """Clear the current guess."""
        self.current_guess = []
        self._update_guess_display()

    def _on_submit(self):
        """Submit the current guess."""
        # Convert colors to symbols
        guess_symbols = colors_to_symbols(self.current_guess)

        try:
            # Make guess
            result = self.game.make_guess(self.player_name, guess_symbols)

            # Add guess to history
            self._add_guess_to_history(
                self.current_guess,
                result["bulls"],
                result["cows"],
            )

            # Clear current guess
            self.current_guess = []
            self._update_guess_display()

            # Update attempt counter
            self.info_label.config(
                text=(
                    f"Player: {self.player_name}  |  "
                    f"Attempt: {self.game.attempts_used + 1}/{self.game.max_attempts}"
                )
            )

            # Check if game is over
            if result["is_finished"]:
                self._game_over()

        except ValueError as exc:
            messagebox.showerror("Error", str(exc))

    def _add_guess_to_history(self, colors: List[str], bulls: int, cows: int):
        """Add a guess to the history display."""
        row = GuessRow(self.scrollable_frame, self.config["length"])
        row.pack(fill=tk.X, padx=5, pady=2)
        row.set_guess(colors)
        row.set_feedback(bulls, cows)
        self.guess_rows.append(row)

        # Scroll to bottom
        self.history_canvas.update_idletasks()
        self.history_canvas.yview_moveto(1.0)

    def _game_over(self):
        """Handle game over."""
        # Disable controls
        self.color_picker.set_enabled(False)
        self.submit_button.config(state=tk.DISABLED)

        # Navigate to game over screen
        self.app.show_gameover_screen(self.game, self.player_name)

"""
Start screen for Mastermind GUI.

Allows players to configure game settings and start a new game.
"""

import tkinter as tk
from tkinter import messagebox
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..app import MastermindApp


class StartScreen(tk.Frame):
    """
    Start screen for game configuration.

    Allows selection of game mode, rules, and player names.
    """

    def __init__(self, parent: tk.Widget, app: "MastermindApp"):
        """
        Initialize the start screen.

        Args:
            parent: Parent widget
            app: Main application controller
        """
        super().__init__(parent, bg="#2C3E50")
        self.app = app

        self._create_widgets()

    def _create_widgets(self):
        """Create the UI widgets."""
        # Title
        title_label = tk.Label(
            self,
            text="🎮 Mastermind Game",
            font=("Arial", 32, "bold"),
            bg="#2C3E50",
            fg="white",
        )
        title_label.pack(pady=30)

        # Main config frame
        config_frame = tk.Frame(self, bg="white", relief=tk.RAISED, borderwidth=3)
        config_frame.pack(padx=50, pady=20, fill=tk.BOTH, expand=True)

        # Game Mode
        mode_frame = tk.LabelFrame(
            config_frame,
            text="Game Mode",
            font=("Arial", 12, "bold"),
            bg="white",
        )
        mode_frame.pack(padx=20, pady=10, fill=tk.X)

        self.mode_var = tk.StringVar(value="pvc")
        tk.Radiobutton(
            mode_frame,
            text="Player vs Computer",
            variable=self.mode_var,
            value="pvc",
            font=("Arial", 11),
            bg="white",
        ).pack(anchor=tk.W, padx=10, pady=5)

        tk.Radiobutton(
            mode_frame,
            text="Player vs Player",
            variable=self.mode_var,
            value="pvp",
            font=("Arial", 11),
            bg="white",
            command=self._on_mode_change,
        ).pack(anchor=tk.W, padx=10, pady=5)

        # Game Settings
        settings_frame = tk.LabelFrame(
            config_frame,
            text="Game Settings",
            font=("Arial", 12, "bold"),
            bg="white",
        )
        settings_frame.pack(padx=20, pady=10, fill=tk.X)

        # Code Length
        length_frame = tk.Frame(settings_frame, bg="white")
        length_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(
            length_frame,
            text="Code Length:",
            font=("Arial", 11),
            bg="white",
        ).pack(side=tk.LEFT)
        self.length_var = tk.IntVar(value=4)
        length_spinbox = tk.Spinbox(
            length_frame,
            from_=3,
            to=6,
            textvariable=self.length_var,
            width=10,
            font=("Arial", 11),
        )
        length_spinbox.pack(side=tk.RIGHT, padx=10)

        # Number of Colors
        colors_frame = tk.Frame(settings_frame, bg="white")
        colors_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(
            colors_frame,
            text="Colors Available:",
            font=("Arial", 11),
            bg="white",
        ).pack(side=tk.LEFT)
        self.colors_var = tk.IntVar(value=6)
        colors_spinbox = tk.Spinbox(
            colors_frame,
            from_=4,
            to=6,
            textvariable=self.colors_var,
            width=10,
            font=("Arial", 11),
        )
        colors_spinbox.pack(side=tk.RIGHT, padx=10)

        # Max Attempts
        attempts_frame = tk.Frame(settings_frame, bg="white")
        attempts_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(
            attempts_frame,
            text="Max Attempts:",
            font=("Arial", 11),
            bg="white",
        ).pack(side=tk.LEFT)
        self.attempts_var = tk.IntVar(value=10)
        attempts_spinbox = tk.Spinbox(
            attempts_frame,
            from_=5,
            to=15,
            textvariable=self.attempts_var,
            width=10,
            font=("Arial", 11),
        )
        attempts_spinbox.pack(side=tk.RIGHT, padx=10)

        # Allow Duplicates
        self.duplicates_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            settings_frame,
            text="Allow Duplicate Colors",
            variable=self.duplicates_var,
            font=("Arial", 11),
            bg="white",
        ).pack(anchor=tk.W, padx=10, pady=5)

        # Player Names
        players_frame = tk.LabelFrame(
            config_frame,
            text="Player Names",
            font=("Arial", 12, "bold"),
            bg="white",
        )
        players_frame.pack(padx=20, pady=10, fill=tk.X)

        # Player 1
        player1_frame = tk.Frame(players_frame, bg="white")
        player1_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(
            player1_frame,
            text="Player Name:",
            font=("Arial", 11),
            bg="white",
        ).pack(side=tk.LEFT)
        self.player1_var = tk.StringVar(value="Player")
        tk.Entry(
            player1_frame,
            textvariable=self.player1_var,
            font=("Arial", 11),
            width=20,
        ).pack(side=tk.RIGHT, padx=10)

        # Player 2 (for PvP)
        self.player2_frame = tk.Frame(players_frame, bg="white")
        tk.Label(
            self.player2_frame,
            text="Player 2 Name:",
            font=("Arial", 11),
            bg="white",
        ).pack(side=tk.LEFT)
        self.player2_var = tk.StringVar(value="Player2")
        tk.Entry(
            self.player2_frame,
            textvariable=self.player2_var,
            font=("Arial", 11),
            width=20,
        ).pack(side=tk.RIGHT, padx=10)

        # Start Button
        start_button = tk.Button(
            config_frame,
            text="Start Game",
            font=("Arial", 14, "bold"),
            bg="#27AE60",
            fg="white",
            activebackground="#229954",
            activeforeground="white",
            command=self._on_start_game,
            width=20,
            height=2,
        )
        start_button.pack(pady=20)

    def _on_mode_change(self):
        """Handle mode change to show/hide player 2 name."""
        if self.mode_var.get() == "pvp":
            self.player2_frame.pack(fill=tk.X, padx=10, pady=5)
        else:
            self.player2_frame.pack_forget()

    def _on_start_game(self):
        """Handle start game button click."""
        # Validate inputs
        player1_name = self.player1_var.get().strip()
        if not player1_name:
            messagebox.showerror("Error", "Please enter a player name!")
            return

        mode = self.mode_var.get()

        if mode == "pvp":
            player2_name = self.player2_var.get().strip()
            if not player2_name:
                messagebox.showerror("Error", "Please enter Player 2 name!")
                return
        else:
            player2_name = None

        # Build configuration
        config = {
            "mode": mode,
            "length": self.length_var.get(),
            "num_colors": self.colors_var.get(),
            "max_attempts": self.attempts_var.get(),
            "allow_duplicates": self.duplicates_var.get(),
            "player1_name": player1_name,
            "player2_name": player2_name,
        }

        # Navigate to appropriate screen
        if mode == "pvp":
            self.app.show_secret_selection_screen(config)
        else:
            self.app.show_gameboard_screen(config)

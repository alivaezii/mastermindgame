"""
Game over screen for Mastermind GUI.

Displays game results and provides options for next actions.
"""

import tkinter as tk
from tkinter import messagebox
from typing import TYPE_CHECKING
from datetime import datetime
from ..utils import symbols_to_colors, get_color_hex
from ...scoreboard import calculate_score, ScoreEntry, save_score

if TYPE_CHECKING:
    from ..app import MastermindApp
    from ...game import Game


class GameOverScreen(tk.Frame):
    """
    Screen displayed when the game ends.
    
    Shows results, score, and action buttons.
    """
    
    def __init__(self, parent: tk.Widget, app: 'MastermindApp', game: 'Game', player_name: str):
        """
        Initialize the game over screen.
        
        Args:
            parent: Parent widget
            app: Main application controller
            game: Completed game instance
            player_name: Name of the player
        """
        super().__init__(parent, bg="#2C3E50")
        self.app = app
        self.game = game
        self.player_name = player_name
        self.score_saved = False
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the UI widgets."""
        # Result message
        if self.game.won:
            message = "🎉 Congratulations! You Won! 🎉"
            message_color = "#27AE60"
        else:
            message = "😢 Game Over - You Lost"
            message_color = "#E74C3C"
        
        result_label = tk.Label(
            self,
            text=message,
            font=("Arial", 32, "bold"),
            bg="#2C3E50",
            fg=message_color
        )
        result_label.pack(pady=40)
        
        # Info frame
        info_frame = tk.Frame(self, bg="white", relief=tk.RAISED, borderwidth=3)
        info_frame.pack(padx=50, pady=20)
        
        # Secret code display
        secret_label = tk.Label(
            info_frame,
            text="Secret Code:",
            font=("Arial", 16, "bold"),
            bg="white"
        )
        secret_label.pack(pady=(20, 10))
        
        # Display secret as colors
        secret_colors = symbols_to_colors(self.game.secret)
        secret_frame = tk.Frame(info_frame, bg="white")
        secret_frame.pack(pady=10)
        
        for color in secret_colors:
            label = tk.Label(
                secret_frame,
                width=6,
                height=3,
                relief=tk.RAISED,
                borderwidth=3,
                bg=get_color_hex(color)
            )
            label.pack(side=tk.LEFT, padx=5)
        
        # Stats
        stats_frame = tk.Frame(info_frame, bg="white")
        stats_frame.pack(pady=20)
        
        attempts_label = tk.Label(
            stats_frame,
            text=f"Attempts Used: {self.game.attempts_used}/{self.game.max_attempts}",
            font=("Arial", 14),
            bg="white"
        )
        attempts_label.pack(pady=5)
        
        # Calculate and display score
        score = calculate_score(
            won=self.game.won,
            attempts_used=self.game.attempts_used,
            max_attempts=self.game.max_attempts,
            mode=self.game.mode
        )
        
        score_label = tk.Label(
            stats_frame,
            text=f"Your Score: {score}",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#3498DB"
        )
        score_label.pack(pady=10)
        
        self.score = score
        
        # Buttons frame
        buttons_frame = tk.Frame(self, bg="#2C3E50")
        buttons_frame.pack(pady=30)
        
        # Save Score button
        self.save_button = tk.Button(
            buttons_frame,
            text="Save Score",
            font=("Arial", 12, "bold"),
            bg="#3498DB",
            fg="white",
            command=self._on_save_score,
            width=15,
            height=2
        )
        self.save_button.grid(row=0, column=0, padx=10, pady=5)
        
        # View High Scores button
        highscores_button = tk.Button(
            buttons_frame,
            text="View High Scores",
            font=("Arial", 12, "bold"),
            bg="#9B59B6",
            fg="white",
            command=self._on_view_highscores,
            width=15,
            height=2
        )
        highscores_button.grid(row=0, column=1, padx=10, pady=5)
        
        # Play Again button
        play_again_button = tk.Button(
            buttons_frame,
            text="Play Again",
            font=("Arial", 12, "bold"),
            bg="#27AE60",
            fg="white",
            command=self._on_play_again,
            width=15,
            height=2
        )
        play_again_button.grid(row=1, column=0, padx=10, pady=5)
        
        # Quit button
        quit_button = tk.Button(
            buttons_frame,
            text="Quit",
            font=("Arial", 12, "bold"),
            bg="#E74C3C",
            fg="white",
            command=self._on_quit,
            width=15,
            height=2
        )
        quit_button.grid(row=1, column=1, padx=10, pady=5)
    
    def _on_save_score(self):
        """Save the score to the scoreboard."""
        if self.score_saved:
            messagebox.showinfo("Info", "Score already saved!")
            return
        
        try:
            entry = ScoreEntry(
                player_name=self.player_name,
                mode=self.game.mode,
                won=self.game.won,
                attempts_used=self.game.attempts_used,
                max_attempts=self.game.max_attempts,
                score=self.score,
                timestamp=datetime.now().isoformat()
            )
            
            save_score(entry)
            self.score_saved = True
            self.save_button.config(state=tk.DISABLED, text="Score Saved ✓")
            messagebox.showinfo("Success", "Score saved successfully!")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save score: {e}")
    
    def _on_view_highscores(self):
        """Navigate to high scores screen."""
        self.app.show_highscores_screen()
    
    def _on_play_again(self):
        """Start a new game."""
        self.app.show_start_screen()
    
    def _on_quit(self):
        """Quit the application."""
        self.app.quit()

"""
High scores screen for Mastermind GUI.

Displays the leaderboard with top scores.
"""

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING
from ...scoreboard import top_scores

if TYPE_CHECKING:
    from ..app import MastermindApp


class HighScoresScreen(tk.Frame):
    """
    Screen displaying the high scores leaderboard.
    """
    
    def __init__(self, parent: tk.Widget, app: 'MastermindApp'):
        """
        Initialize the high scores screen.
        
        Args:
            parent: Parent widget
            app: Main application controller
        """
        super().__init__(parent, bg="#2C3E50")
        self.app = app
        
        self._create_widgets()
        self._load_scores()
    
    def _create_widgets(self):
        """Create the UI widgets."""
        # Title
        title_label = tk.Label(
            self,
            text="🏆 High Scores 🏆",
            font=("Arial", 32, "bold"),
            bg="#2C3E50",
            fg="#F1C40F"
        )
        title_label.pack(pady=30)
        
        # Scores frame
        scores_frame = tk.Frame(self, bg="white", relief=tk.RAISED, borderwidth=3)
        scores_frame.pack(padx=50, pady=20, fill=tk.BOTH, expand=True)
        
        # Create treeview for scores table
        columns = ("Rank", "Player", "Score", "Mode", "Result", "Attempts")
        self.tree = ttk.Treeview(scores_frame, columns=columns, show="headings", height=15)
        
        # Define column headings
        self.tree.heading("Rank", text="Rank")
        self.tree.heading("Player", text="Player Name")
        self.tree.heading("Score", text="Score")
        self.tree.heading("Mode", text="Mode")
        self.tree.heading("Result", text="Result")
        self.tree.heading("Attempts", text="Attempts")
        
        # Define column widths
        self.tree.column("Rank", width=60, anchor=tk.CENTER)
        self.tree.column("Player", width=150, anchor=tk.W)
        self.tree.column("Score", width=80, anchor=tk.CENTER)
        self.tree.column("Mode", width=80, anchor=tk.CENTER)
        self.tree.column("Result", width=80, anchor=tk.CENTER)
        self.tree.column("Attempts", width=100, anchor=tk.CENTER)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(scores_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        # Back button
        back_button = tk.Button(
            self,
            text="Back",
            font=("Arial", 14, "bold"),
            bg="#3498DB",
            fg="white",
            command=self._on_back,
            width=15,
            height=2
        )
        back_button.pack(pady=20)
    
    def _load_scores(self):
        """Load and display the top scores."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load top 10 scores
        scores = top_scores(limit=10)
        
        if not scores:
            # Show message if no scores
            self.tree.insert("", tk.END, values=("", "No scores yet!", "", "", "", ""))
        else:
            # Add scores to table
            for rank, entry in enumerate(scores, 1):
                result = "Won ✓" if entry.won else "Lost ✗"
                mode_display = entry.mode.upper()
                attempts_display = f"{entry.attempts_used}/{entry.max_attempts}"
                
                self.tree.insert(
                    "",
                    tk.END,
                    values=(rank, entry.player_name, entry.score, mode_display, result, attempts_display)
                )
    
    def _on_back(self):
        """Return to the previous screen."""
        self.app.show_start_screen()

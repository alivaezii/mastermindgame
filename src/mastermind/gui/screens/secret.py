"""
Secret selection screen for Mastermind GUI (PvP mode).

Allows Player 1 to set a secret code for Player 2 to guess.
"""

import tkinter as tk
from tkinter import messagebox
from typing import TYPE_CHECKING, List
from ..widgets.colorpicker import ColorPicker
from ..utils import get_available_colors, get_color_hex, colors_to_symbols, get_alphabet_for_colors
from ...engine import Rules, validate_guess

if TYPE_CHECKING:
    from ..app import MastermindApp


class SecretSelectionScreen(tk.Frame):
    """
    Screen for Player 1 to select a secret code in PvP mode.
    """
    
    def __init__(self, parent: tk.Widget, app: 'MastermindApp', config: dict):
        """
        Initialize the secret selection screen.
        
        Args:
            parent: Parent widget
            app: Main application controller
            config: Game configuration dictionary
        """
        super().__init__(parent, bg="#34495E")
        self.app = app
        self.config = config
        
        self.available_colors = get_available_colors(config["num_colors"])
        self.selected_colors: List[str] = []
        self.color_labels = []
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the UI widgets."""
        # Title
        title_label = tk.Label(
            self,
            text=f"{self.config['player1_name']}: Set Your Secret Code",
            font=("Arial", 24, "bold"),
            bg="#34495E",
            fg="white"
        )
        title_label.pack(pady=30)
        
        # Instructions
        instructions = tk.Label(
            self,
            text="Select colors to create your secret code.\nPlayer 2 will try to guess it!",
            font=("Arial", 12),
            bg="#34495E",
            fg="white"
        )
        instructions.pack(pady=10)
        
        # Secret display frame
        secret_frame = tk.LabelFrame(
            self,
            text="Your Secret Code",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="black"
        )
        secret_frame.pack(pady=20)
        
        # Color slots for secret
        slots_frame = tk.Frame(secret_frame, bg="white")
        slots_frame.pack(padx=20, pady=15)
        
        for i in range(self.config["length"]):
            label = tk.Label(
                slots_frame,
                width=6,
                height=3,
                relief=tk.SUNKEN,
                borderwidth=3,
                bg="#CCCCCC",
                text=str(i+1),
                font=("Arial", 12, "bold")
            )
            label.pack(side=tk.LEFT, padx=5)
            self.color_labels.append(label)
        
        # Color picker
        picker_frame = tk.LabelFrame(
            self,
            text="Select Colors",
            font=("Arial", 14, "bold"),
            bg="white"
        )
        picker_frame.pack(pady=20)
        
        self.color_picker = ColorPicker(
            picker_frame,
            self.available_colors,
            self._on_color_selected
        )
        self.color_picker.pack(padx=20, pady=15)
        
        # Buttons frame
        buttons_frame = tk.Frame(self, bg="#34495E")
        buttons_frame.pack(pady=20)
        
        # Clear button
        clear_button = tk.Button(
            buttons_frame,
            text="Clear",
            font=("Arial", 12, "bold"),
            bg="#E74C3C",
            fg="white",
            command=self._on_clear,
            width=12,
            height=2
        )
        clear_button.pack(side=tk.LEFT, padx=10)
        
        # Confirm button
        self.confirm_button = tk.Button(
            buttons_frame,
            text="Confirm Secret",
            font=("Arial", 12, "bold"),
            bg="#27AE60",
            fg="white",
            command=self._on_confirm,
            width=15,
            height=2,
            state=tk.DISABLED
        )
        self.confirm_button.pack(side=tk.LEFT, padx=10)
    
    def _on_color_selected(self, color: str):
        """
        Handle color selection.
        
        Args:
            color: Selected color name
        """
        if len(self.selected_colors) < self.config["length"]:
            self.selected_colors.append(color)
            self._update_display()
    
    def _update_display(self):
        """Update the secret code display."""
        for i, label in enumerate(self.color_labels):
            if i < len(self.selected_colors):
                label.config(bg=get_color_hex(self.selected_colors[i]), text="")
            else:
                label.config(bg="#CCCCCC", text=str(i+1))
        
        # Enable confirm button if secret is complete
        if len(self.selected_colors) == self.config["length"]:
            self.confirm_button.config(state=tk.NORMAL)
        else:
            self.confirm_button.config(state=tk.DISABLED)
    
    def _on_clear(self):
        """Clear the selected secret."""
        self.selected_colors = []
        self._update_display()
    
    def _on_confirm(self):
        """Confirm the secret and proceed to game."""
        # Validate the secret
        secret_symbols = colors_to_symbols(self.selected_colors)
        alphabet = get_alphabet_for_colors(self.config["num_colors"])
        rules = Rules(
            length=self.config["length"],
            alphabet=alphabet,
            allow_duplicates=self.config["allow_duplicates"]
        )
        
        try:
            validate_guess(secret_symbols, rules)
            # Navigate to game board with secret
            self.app.show_gameboard_screen(self.config, secret_symbols)
        except ValueError as e:
            messagebox.showerror("Invalid Secret", str(e))

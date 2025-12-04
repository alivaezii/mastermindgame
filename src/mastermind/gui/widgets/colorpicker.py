"""
ColorPicker widget for Mastermind GUI.

Provides a reusable color selection interface with clickable color buttons.
"""

import tkinter as tk
from typing import Callable, List, Optional
from ..utils import get_color_hex


class ColorPicker(tk.Frame):
    """
    A widget that displays a grid of color buttons for selection.
    
    When a color is clicked, calls the provided callback function.
    """
    
    def __init__(
        self,
        parent: tk.Widget,
        colors: List[str],
        on_select: Callable[[str], None],
        columns: int = 6
    ):
        """
        Initialize the ColorPicker widget.
        
        Args:
            parent: Parent widget
            colors: List of color names to display
            on_select: Callback function called with color name when clicked
            columns: Number of columns in the grid (default: 6)
        """
        super().__init__(parent)
        
        self.colors = colors
        self.on_select = on_select
        self.columns = columns
        self.buttons = {}
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the color button grid."""
        for i, color in enumerate(self.colors):
            row = i // self.columns
            col = i % self.columns
            
            # Create button with color background
            btn = tk.Button(
                self,
                bg=get_color_hex(color),
                width=4,
                height=2,
                relief=tk.RAISED,
                borderwidth=3,
                command=lambda c=color: self._on_color_click(c)
            )
            btn.grid(row=row, column=col, padx=5, pady=5)
            
            self.buttons[color] = btn
    
    def _on_color_click(self, color: str):
        """
        Handle color button click.
        
        Args:
            color: Name of the clicked color
        """
        self.on_select(color)
    
    def set_enabled(self, enabled: bool):
        """
        Enable or disable all color buttons.
        
        Args:
            enabled: True to enable, False to disable
        """
        state = tk.NORMAL if enabled else tk.DISABLED
        for btn in self.buttons.values():
            btn.config(state=state)

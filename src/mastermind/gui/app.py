"""
Main application controller for Mastermind GUI.

Manages screen navigation and application state.
"""

import tkinter as tk
from typing import Optional, Dict, Any


class MastermindApp:
    """
    Main application controller for the Mastermind GUI.
    
    Manages the Tk root window, screen navigation, and game state.
    """
    
    def __init__(self):
        """Initialize the application."""
        self.root = tk.Tk()
        self.root.title("🎮 Mastermind Game")
        self.root.geometry("800x750")
        self.root.resizable(False, False)
        
        # Application state
        self.current_screen = None
        self.game_config: Optional[Dict[str, Any]] = None
        self.game_instance = None
        
        # Show start screen
        self.show_start_screen()
    
    def show_start_screen(self):
        """Navigate to the start screen."""
        from .screens.start import StartScreen
        self._show_screen(StartScreen(self.root, self))
    
    def show_secret_selection_screen(self, config: Dict[str, Any]):
        """
        Navigate to the secret selection screen (PvP mode).
        
        Args:
            config: Game configuration dictionary
        """
        from .screens.secret import SecretSelectionScreen
        self.game_config = config
        self._show_screen(SecretSelectionScreen(self.root, self, config))
    
    def show_gameboard_screen(self, config: Dict[str, Any], secret: Optional[str] = None):
        """
        Navigate to the game board screen.
        
        Args:
            config: Game configuration dictionary
            secret: Optional secret code (for PvP mode)
        """
        from .screens.gameboard import GameBoardScreen
        self.game_config = config
        self._show_screen(GameBoardScreen(self.root, self, config, secret))
    
    def show_gameover_screen(self, game, player_name: str):
        """
        Navigate to the game over screen.
        
        Args:
            game: The completed Game instance
            player_name: Name of the player
        """
        from .screens.gameover import GameOverScreen
        self.game_instance = game
        self._show_screen(GameOverScreen(self.root, self, game, player_name))
    
    def show_highscores_screen(self):
        """Navigate to the high scores screen."""
        from .screens.highscores import HighScoresScreen
        self._show_screen(HighScoresScreen(self.root, self))
    
    def _show_screen(self, screen: tk.Frame):
        """
        Display a screen, destroying the current one.
        
        Args:
            screen: The screen widget to display
        """
        # Destroy current screen if it exists
        if self.current_screen is not None:
            self.current_screen.destroy()
        
        # Display new screen
        self.current_screen = screen
        self.current_screen.pack(fill=tk.BOTH, expand=True)
    
    def run(self):
        """Start the application main loop."""
        self.root.mainloop()
    
    def quit(self):
        """Quit the application."""
        self.root.quit()


def main():
    """Entry point for the GUI application."""
    app = MastermindApp()
    app.run()


if __name__ == "__main__":
    main()

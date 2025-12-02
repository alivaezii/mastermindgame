"""
Game state management for Mastermind.

This module provides the Game class that encapsulates game state and logic,
supporting both Player vs Computer (pvc) and Player vs Player (pvp) modes.
"""

import random
from typing import Literal, Optional

from .engine import Rules, validate_guess, score


def generate_secret(rules: Rules) -> str:
    """Create a secret code according to the current Rules."""
    if rules.allow_duplicates:
        return "".join(random.choice(rules.alphabet) for _ in range(rules.length))
    # Without duplicates we must sample unique symbols
    if rules.length > len(rules.alphabet):
        raise ValueError("length cannot exceed the number of unique symbols in the alphabet.")
    return "".join(random.sample(rules.alphabet, rules.length))


class Game:
    """
    Encapsulates the state and logic of a Mastermind game.
    
    Supports two modes:
    - "pvc" (Player vs Computer): Computer generates the secret
    - "pvp" (Player vs Player): One player provides the secret
    
    Attributes:
        rules: The game rules (length, alphabet, duplicates)
        mode: Game mode ("pvc" or "pvp")
        max_attempts: Maximum number of allowed guesses
        attempts_used: Number of guesses made so far
        is_finished: Whether the game has ended
        won: True if won, False if lost, None if game is ongoing
    """
    
    def __init__(
        self,
        rules: Rules,
        mode: Literal["pvc", "pvp"],
        max_attempts: int,
        secret: Optional[str] = None
    ):
        """
        Initialize a new game.
        
        Args:
            rules: Game rules configuration
            mode: "pvc" for Player vs Computer, "pvp" for Player vs Player
            max_attempts: Maximum number of guesses allowed
            secret: Optional secret code. If None in pvc mode, will be generated.
                   Required for pvp mode.
        
        Raises:
            ValueError: If secret is None in pvp mode, or if secret is invalid
        """
        self.rules = rules
        self.mode = mode
        self.max_attempts = max_attempts
        self.attempts_used = 0
        self.is_finished = False
        self.won: Optional[bool] = None
        
        # Handle secret initialization
        if mode == "pvc" and secret is None:
            self._secret = generate_secret(rules)
        elif secret is not None:
            # Validate the provided secret
            validate_guess(secret, rules)
            self._secret = secret
        else:
            raise ValueError("Secret must be provided for pvp mode")
    
    def make_guess(self, player_name: Optional[str], guess: str) -> dict:
        """
        Process a guess and update game state.
        
        Args:
            player_name: Name of the player making the guess (optional)
            guess: The guessed code
        
        Returns:
            Dictionary containing:
                - bulls: Number of correct symbols in correct positions
                - cows: Number of correct symbols in wrong positions
                - attempts_used: Total attempts made so far
                - remaining_attempts: Attempts remaining
                - is_finished: Whether the game has ended
                - won: True if won, False if lost, None if ongoing
                - secret: The secret code (only included if game is lost)
        
        Raises:
            ValueError: If guess is invalid or game is already finished
        """
        if self.is_finished:
            raise ValueError("Game is already finished")
        
        # Validate the guess
        validate_guess(guess, self.rules)
        
        # Increment attempts
        self.attempts_used += 1
        
        # Calculate bulls and cows
        bulls, cows = score(self._secret, guess)
        
        # Check win condition
        if bulls == self.rules.length:
            self.is_finished = True
            self.won = True
        # Check lose condition
        elif self.attempts_used >= self.max_attempts:
            self.is_finished = True
            self.won = False
        
        # Build result dictionary
        result = {
            "bulls": bulls,
            "cows": cows,
            "attempts_used": self.attempts_used,
            "remaining_attempts": self.remaining_attempts(),
            "is_finished": self.is_finished,
            "won": self.won
        }
        
        # Include secret only if game is lost
        if self.is_finished and not self.won:
            result["secret"] = self._secret
        
        return result
    
    def is_over(self) -> bool:
        """Check if the game has ended."""
        return self.is_finished
    
    def remaining_attempts(self) -> int:
        """Get the number of remaining attempts."""
        return max(0, self.max_attempts - self.attempts_used)
    
    @property
    def secret(self) -> str:
        """
        Get the secret code.
        
        Note: This property is primarily for testing purposes.
        In normal gameplay, the secret should not be exposed until the game ends.
        """
        return self._secret

"""Mastermind package initializer."""
from .engine import Rules, validate_guess, score
from .game import Game
from .scoreboard import ScoreEntry, calculate_score, save_score, load_scores, top_scores

__all__ = [
    "Rules",
    "validate_guess",
    "score",
    "Game",
    "ScoreEntry",
    "calculate_score",
    "save_score",
    "load_scores",
    "top_scores",
]
__version__ = "0.2.0"  # Updated for Sprint 2
c
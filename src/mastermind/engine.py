"""
Core game logic for Mastermind.

- Rules: holds game configuration (code length, alphabet, duplicates).
- validate_guess: ensures a guess matches the current Rules.
- score: computes (bulls, cows) for a secret/guess pair.

All functions are pure and side-effect free to keep testing simple.
"""

from dataclasses import dataclass
from typing import Tuple
from collections import Counter


@dataclass(frozen=True)
class Rules:
    """Immutable container for game rules."""
    length: int = 4
    alphabet: str = "012345"
    allow_duplicates: bool = True


def validate_guess(guess: str, rules: Rules) -> None:
    """
    Validate a guess against the given rules.

    Raises:
        ValueError: if length is wrong, characters are invalid,
                    or duplicates are not allowed but present.
    """
    if len(guess) != rules.length:
        raise ValueError(f"Guess must be {rules.length} characters long.")
    if any(ch not in rules.alphabet for ch in guess):
        raise ValueError("Guess contains characters not in the alphabet.")
    if not rules.allow_duplicates and len(set(guess)) < len(guess):
        raise ValueError("Duplicates are not allowed for this game.")


def score(secret: str, guess: str) -> Tuple[int, int]:
    """
    Compute (bulls, cows):
      - bulls: same symbol in the same position
      - cows : same symbol but different position

    Note: This function assumes secret and guess have the same length.
    """
    bulls = sum(s == g for s, g in zip(secret, guess))
    cows = sum((Counter(secret) & Counter(guess)).values()) - bulls
    return bulls, cows

"""
Game state management for Mastermind.

This module provides the Game class that encapsulates game state and logic,
supporting both Player vs Computer (pvc) and Player vs Player (pvp) modes.
"""

import random
from typing import Any, Literal, Optional

from .engine import Rules, validate_guess, score


def generate_secret(rules: Rules) -> str:
    """Create a secret code according to the current Rules."""
    if rules.allow_duplicates:
        return "".join(random.choice(rules.alphabet) for _ in range(rules.length))

    if rules.length > len(rules.alphabet):
        raise ValueError("length cannot exceed the number of unique symbols in the alphabet.")

    return "".join(random.sample(rules.alphabet, rules.length))


class Game:
    def __init__(
        self,
        rules: Rules,
        mode: Literal["pvc", "pvp"],
        max_attempts: int,
        secret: Optional[str] = None,
    ):
        self.rules: Rules = rules
        self.mode: Literal["pvc", "pvp"] = mode
        self.max_attempts: int = int(max_attempts)
        self.attempts_used: int = 0
        self.is_finished: bool = False
        self.won: Optional[bool] = None

        if mode == "pvc" and secret is None:
            self._secret: str = generate_secret(rules)
        elif secret is not None:
            validate_guess(secret, rules)
            self._secret = secret
        else:
            raise ValueError("Secret must be provided for pvp mode")

    def make_guess(self, player_name: Optional[str], guess: str) -> dict[str, Any]:
        _ = player_name

        if self.is_finished:
            raise ValueError("Game is already finished")

        validate_guess(guess, self.rules)

        self.attempts_used += 1

        bulls, cows = score(self._secret, guess)

        if bulls == self.rules.length:
            self.is_finished = True
            self.won = True
        elif self.attempts_used >= self.max_attempts:
            self.is_finished = True
            self.won = False

        result: dict[str, Any] = {
            "bulls": bulls,
            "cows": cows,
            "attempts_used": self.attempts_used,
            "remaining_attempts": self.remaining_attempts(),
            "is_finished": self.is_finished,
            "won": self.won,
        }

        if self.is_finished and self.won is False:
            result["secret"] = self._secret

        return result

    def is_over(self) -> bool:
        return self.is_finished

    def remaining_attempts(self) -> int:
        return max(0, self.max_attempts - self.attempts_used)

    @property
    def secret(self) -> str:
        return self._secret

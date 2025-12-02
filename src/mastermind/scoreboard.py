"""
Scoring and scoreboard system for Mastermind.

Provides score calculation, persistence to JSON, and retrieval of top scores.
"""

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Union


@dataclass(frozen=True)
class ScoreEntry:
    """
    Immutable record of a game score.

    Attributes:
        player_name: Name of the player
        mode: Game mode ("pvc" or "pvp")
        won: Whether the player won
        attempts_used: Number of attempts used
        max_attempts: Maximum attempts allowed
        score: Calculated score
        timestamp: ISO 8601 timestamp string
    """
    player_name: str
    mode: str
    won: bool
    attempts_used: int
    max_attempts: int
    score: int
    timestamp: str


def calculate_score(won: bool, attempts_used: int, max_attempts: int, mode: str) -> int:
    """
    Calculate the score for a completed game.

    Scoring rules:
    - If won: base_score (100) + bonus per remaining attempt (10 each)
    - If lost: 0

    Args:
        won: Whether the player won the game
        attempts_used: Number of attempts used
        max_attempts: Maximum attempts allowed
        mode: Game mode (reserved for future use)

    Returns:
        The calculated score (integer)

    Example:
        >>> calculate_score(won=True, attempts_used=3, max_attempts=10, mode="pvc")
        170  # 100 + (10 * 7)
        >>> calculate_score(won=False, attempts_used=10, max_attempts=10, mode="pvc")
        0
    """
    if won:
        base_score = 100
        bonus_per_remaining = 10
        remaining = max(0, max_attempts - attempts_used)
        return base_score + bonus_per_remaining * remaining
    return 0


def load_scores(path: Union[Path, str] = "scores.json") -> list[ScoreEntry]:
    """
    Load scores from a JSON file.

    Args:
        path: Path to the scores file (default: "scores.json")

    Returns:
        List of ScoreEntry objects. Returns empty list if file doesn't exist.
    """
    path = Path(path)

    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        # Convert dictionaries to ScoreEntry objects
        return [ScoreEntry(**entry) for entry in data]
    except (json.JSONDecodeError, TypeError, KeyError):
        # If file is corrupted or invalid, return empty list
        return []


def save_score(entry: ScoreEntry, path: Union[Path, str] = "scores.json") -> None:
    """
    Save a score entry to the JSON file.

    Loads existing scores, appends the new entry, and writes back.

    Args:
        entry: The ScoreEntry to save
        path: Path to the scores file (default: "scores.json")
    """
    path = Path(path)

    # Load existing scores
    scores = load_scores(path)

    # Append new entry
    scores.append(entry)

    # Convert to dictionaries for JSON serialization
    data = [asdict(entry) for entry in scores]

    # Write to file
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def top_scores(limit: int = 10, path: Union[Path, str] = "scores.json") -> list[ScoreEntry]:
    """
    Retrieve the top N scores.

    Scores are sorted by score (descending), then by timestamp (ascending) for ties.

    Args:
        limit: Maximum number of scores to return (default: 10)
        path: Path to the scores file (default: "scores.json")

    Returns:
        List of top ScoreEntry objects, sorted by score descending
    """
    scores = load_scores(path)

    # Sort by score descending, then by timestamp ascending (earlier is better for ties)
    sorted_scores = sorted(
        scores,
        key=lambda x: (-x.score, x.timestamp),
    )

    return sorted_scores[:limit]

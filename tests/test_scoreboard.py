"""
Unit tests for the scoreboard module.

Tests cover score calculation, persistence, and retrieval.
Uses tmp_path fixture for isolated file operations.
"""
import json
from datetime import datetime
from pathlib import Path

import pytest

from mastermind.scoreboard import (
    ScoreEntry,
    calculate_score,
    load_scores,
    save_score,
    top_scores
)


def test_calculate_score_won_full_attempts():
    """Test score calculation when winning with all attempts remaining."""
    score = calculate_score(won=True, attempts_used=0, max_attempts=10, mode="pvc")
    assert score == 200  # 100 + (10 * 10)


def test_calculate_score_won_some_attempts():
    """Test score calculation when winning with some attempts used."""
    score = calculate_score(won=True, attempts_used=3, max_attempts=10, mode="pvc")
    assert score == 170  # 100 + (10 * 7)


def test_calculate_score_won_last_attempt():
    """Test score calculation when winning on the last attempt."""
    score = calculate_score(won=True, attempts_used=10, max_attempts=10, mode="pvc")
    assert score == 100  # 100 + (10 * 0)


def test_calculate_score_lost():
    """Test score calculation when losing."""
    score = calculate_score(won=False, attempts_used=10, max_attempts=10, mode="pvc")
    assert score == 0


def test_calculate_score_different_modes():
    """Test that mode parameter doesn't affect score (reserved for future)."""
    score_pvc = calculate_score(won=True, attempts_used=5, max_attempts=10, mode="pvc")
    score_pvp = calculate_score(won=True, attempts_used=5, max_attempts=10, mode="pvp")
    assert score_pvc == score_pvp == 150


def test_score_entry_creation():
    """Test creating a ScoreEntry."""
    entry = ScoreEntry(
        player_name="Alice",
        mode="pvc",
        won=True,
        attempts_used=3,
        max_attempts=10,
        score=170,
        timestamp="2025-11-29T18:00:00"
    )
    assert entry.player_name == "Alice"
    assert entry.score == 170
    assert entry.won is True


def test_score_entry_immutable():
    """Test that ScoreEntry is immutable."""
    entry = ScoreEntry(
        player_name="Alice",
        mode="pvc",
        won=True,
        attempts_used=3,
        max_attempts=10,
        score=170,
        timestamp="2025-11-29T18:00:00"
    )
    with pytest.raises(AttributeError):
        entry.score = 200


def test_load_scores_nonexistent_file(tmp_path):
    """Test loading scores when file doesn't exist."""
    scores_file = tmp_path / "scores.json"
    scores = load_scores(scores_file)
    assert scores == []


def test_save_and_load_single_score(tmp_path):
    """Test saving and loading a single score."""
    scores_file = tmp_path / "scores.json"
    
    entry = ScoreEntry(
        player_name="Alice",
        mode="pvc",
        won=True,
        attempts_used=3,
        max_attempts=10,
        score=170,
        timestamp="2025-11-29T18:00:00"
    )
    
    save_score(entry, scores_file)
    
    # Verify file was created
    assert scores_file.exists()
    
    # Load and verify
    loaded = load_scores(scores_file)
    assert len(loaded) == 1
    assert loaded[0].player_name == "Alice"
    assert loaded[0].score == 170


def test_save_multiple_scores(tmp_path):
    """Test saving multiple scores."""
    scores_file = tmp_path / "scores.json"
    
    entry1 = ScoreEntry(
        player_name="Alice",
        mode="pvc",
        won=True,
        attempts_used=3,
        max_attempts=10,
        score=170,
        timestamp="2025-11-29T18:00:00"
    )
    
    entry2 = ScoreEntry(
        player_name="Bob",
        mode="pvp",
        won=False,
        attempts_used=10,
        max_attempts=10,
        score=0,
        timestamp="2025-11-29T18:05:00"
    )
    
    save_score(entry1, scores_file)
    save_score(entry2, scores_file)
    
    loaded = load_scores(scores_file)
    assert len(loaded) == 2
    assert loaded[0].player_name == "Alice"
    assert loaded[1].player_name == "Bob"


def test_top_scores_ordering(tmp_path):
    """Test that top_scores returns scores in correct order."""
    scores_file = tmp_path / "scores.json"
    
    # Create entries with different scores
    entries = [
        ScoreEntry("Alice", "pvc", True, 3, 10, 170, "2025-11-29T18:00:00"),
        ScoreEntry("Bob", "pvc", True, 1, 10, 190, "2025-11-29T18:01:00"),
        ScoreEntry("Charlie", "pvc", False, 10, 10, 0, "2025-11-29T18:02:00"),
        ScoreEntry("Diana", "pvc", True, 5, 10, 150, "2025-11-29T18:03:00"),
    ]
    
    for entry in entries:
        save_score(entry, scores_file)
    
    top = top_scores(limit=10, path=scores_file)
    
    # Should be ordered by score descending
    assert len(top) == 4
    assert top[0].player_name == "Bob"  # 190
    assert top[1].player_name == "Alice"  # 170
    assert top[2].player_name == "Diana"  # 150
    assert top[3].player_name == "Charlie"  # 0


def test_top_scores_limit(tmp_path):
    """Test that top_scores respects the limit parameter."""
    scores_file = tmp_path / "scores.json"
    
    # Create 5 entries
    for i in range(5):
        entry = ScoreEntry(
            player_name=f"Player{i}",
            mode="pvc",
            won=True,
            attempts_used=i,
            max_attempts=10,
            score=100 + (10 * (10 - i)),
            timestamp=f"2025-11-29T18:0{i}:00"
        )
        save_score(entry, scores_file)
    
    # Request only top 3
    top = top_scores(limit=3, path=scores_file)
    assert len(top) == 3


def test_top_scores_tie_breaking(tmp_path):
    """Test that ties are broken by timestamp (earlier is better)."""
    scores_file = tmp_path / "scores.json"
    
    # Create entries with same score but different timestamps
    entry1 = ScoreEntry("Alice", "pvc", True, 3, 10, 170, "2025-11-29T18:00:00")
    entry2 = ScoreEntry("Bob", "pvc", True, 3, 10, 170, "2025-11-29T17:00:00")  # Earlier
    
    save_score(entry1, scores_file)
    save_score(entry2, scores_file)
    
    top = top_scores(limit=10, path=scores_file)
    
    # Bob should be first (same score but earlier timestamp)
    assert top[0].player_name == "Bob"
    assert top[1].player_name == "Alice"


def test_load_scores_corrupted_file(tmp_path):
    """Test that loading a corrupted file returns empty list."""
    scores_file = tmp_path / "scores.json"
    
    # Write invalid JSON
    scores_file.write_text("not valid json", encoding="utf-8")
    
    scores = load_scores(scores_file)
    assert scores == []


def test_load_scores_invalid_structure(tmp_path):
    """Test that loading a file with invalid structure returns empty list."""
    scores_file = tmp_path / "scores.json"
    
    # Write valid JSON but invalid structure
    scores_file.write_text('{"invalid": "structure"}', encoding="utf-8")
    
    scores = load_scores(scores_file)
    assert scores == []


def test_save_score_creates_directory(tmp_path):
    """Test that save_score creates parent directories if needed."""
    scores_file = tmp_path / "subdir" / "scores.json"
    
    entry = ScoreEntry("Alice", "pvc", True, 3, 10, 170, "2025-11-29T18:00:00")
    save_score(entry, scores_file)
    
    assert scores_file.exists()
    assert scores_file.parent.exists()


def test_json_format(tmp_path):
    """Test that the JSON file is properly formatted."""
    scores_file = tmp_path / "scores.json"
    
    entry = ScoreEntry("Alice", "pvc", True, 3, 10, 170, "2025-11-29T18:00:00")
    save_score(entry, scores_file)
    
    # Read the raw JSON
    with scores_file.open("r", encoding="utf-8") as f:
        data = json.load(f)
    
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["player_name"] == "Alice"
    assert data[0]["score"] == 170

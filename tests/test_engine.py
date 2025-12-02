"""
Unit tests for the core engine.

We keep tests small, deterministic, and focused on one behavior at a time.
"""
import pytest
from mastermind import Rules, validate_guess, score


def test_score_exact_match():
    assert score("1234", "1234") == (4, 0)


def test_score_partial_match():
    # "1234" vs "1243" -> positions 1 and 2 match (bulls=2), the other two are swapped (cows=2)
    assert score("1234", "1243") == (2, 2)


def test_score_no_overlap():
    assert score("1234", "5555") == (0, 0)


def test_validate_length_error():
    rules = Rules(length=4)
    with pytest.raises(ValueError):
        validate_guess("12345", rules)


def test_validate_invalid_character():
    rules = Rules(length=4, alphabet="0123")
    with pytest.raises(ValueError):
        validate_guess("1293", rules)  # '9' is not allowed


def test_validate_duplicates_not_allowed():
    rules = Rules(length=4, allow_duplicates=False)
    with pytest.raises(ValueError):
        validate_guess("1123", rules)  # duplicates not allowed

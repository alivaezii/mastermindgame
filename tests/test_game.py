"""
Unit tests for the Game class.

Tests cover both game modes (pvc, pvp), win/lose conditions,
max attempts enforcement, and state management.
"""
import pytest
from mastermind import Rules
from mastermind.game import Game, generate_secret


def test_generate_secret_with_duplicates():
    """Test secret generation with duplicates allowed."""
    rules = Rules(length=4, alphabet="0123", allow_duplicates=True)
    secret = generate_secret(rules)
    assert len(secret) == 4
    assert all(ch in rules.alphabet for ch in secret)


def test_generate_secret_no_duplicates():
    """Test secret generation without duplicates."""
    rules = Rules(length=3, alphabet="0123", allow_duplicates=False)
    secret = generate_secret(rules)
    assert len(secret) == 3
    assert len(set(secret)) == 3
    assert all(ch in rules.alphabet for ch in secret)


def test_generate_secret_no_duplicates_error():
    """Test that generating secret fails when length exceeds alphabet size."""
    rules = Rules(length=5, alphabet="012", allow_duplicates=False)
    with pytest.raises(ValueError):
        generate_secret(rules)


def test_game_pvc_mode_generates_secret():
    """Test that pvc mode generates a secret when none is provided."""
    rules = Rules(length=4, alphabet="012345")
    game = Game(rules=rules, mode="pvc", max_attempts=10)
    assert len(game.secret) == 4
    assert all(ch in rules.alphabet for ch in game.secret)


def test_game_pvp_mode_requires_secret():
    """Test that pvp mode requires a secret to be provided."""
    rules = Rules(length=4, alphabet="012345")
    with pytest.raises(ValueError, match="Secret must be provided for pvp mode"):
        Game(rules=rules, mode="pvp", max_attempts=10)


def test_game_pvp_mode_with_secret():
    """Test that pvp mode accepts a valid secret."""
    rules = Rules(length=4, alphabet="012345")
    game = Game(rules=rules, mode="pvp", max_attempts=10, secret="0123")
    assert game.secret == "0123"


def test_game_initial_state():
    """Test that game initializes with correct state."""
    rules = Rules(length=4, alphabet="012345")
    game = Game(rules=rules, mode="pvp", max_attempts=10, secret="0123")
    assert game.attempts_used == 0
    assert game.is_finished is False
    assert game.won is None
    assert game.remaining_attempts() == 10
    assert game.is_over() is False


def test_game_winning_guess():
    """Test winning the game with a correct guess."""
    rules = Rules(length=4, alphabet="012345")
    game = Game(rules=rules, mode="pvp", max_attempts=10, secret="0123")
    
    result = game.make_guess("Player1", "0123")
    
    assert result["bulls"] == 4
    assert result["cows"] == 0
    assert result["attempts_used"] == 1
    assert result["remaining_attempts"] == 9
    assert result["is_finished"] is True
    assert result["won"] is True
    assert "secret" not in result  # Secret not revealed when won
    assert game.is_over() is True


def test_game_losing_by_max_attempts():
    """Test losing the game by reaching max attempts."""
    rules = Rules(length=4, alphabet="012345")
    game = Game(rules=rules, mode="pvp", max_attempts=3, secret="0123")
    
    # Make 3 wrong guesses
    result1 = game.make_guess("Player1", "1111")
    assert result1["is_finished"] is False
    assert result1["won"] is None
    
    result2 = game.make_guess("Player1", "2222")
    assert result2["is_finished"] is False
    assert result2["won"] is None
    
    result3 = game.make_guess("Player1", "3333")
    assert result3["is_finished"] is True
    assert result3["won"] is False
    assert result3["secret"] == "0123"  # Secret revealed when lost
    assert game.is_over() is True


def test_game_winning_on_last_attempt():
    """Test winning on the last allowed attempt."""
    rules = Rules(length=4, alphabet="012345")
    game = Game(rules=rules, mode="pvp", max_attempts=2, secret="0123")
    
    # First guess wrong
    result1 = game.make_guess("Player1", "1111")
    assert result1["is_finished"] is False
    
    # Second guess correct
    result2 = game.make_guess("Player1", "0123")
    assert result2["is_finished"] is True
    assert result2["won"] is True
    assert result2["attempts_used"] == 2


def test_game_partial_match():
    """Test game with partial matches (bulls and cows)."""
    rules = Rules(length=4, alphabet="012345")
    game = Game(rules=rules, mode="pvp", max_attempts=10, secret="0123")
    
    result = game.make_guess("Player1", "0321")
    assert result["bulls"] == 2  # 0 and 3 in correct positions
    assert result["cows"] == 2  # 1 and 2 in wrong positions
    assert result["is_finished"] is False


def test_game_cannot_guess_after_finished():
    """Test that guessing after game ends raises an error."""
    rules = Rules(length=4, alphabet="012345")
    game = Game(rules=rules, mode="pvp", max_attempts=10, secret="0123")
    
    # Win the game
    game.make_guess("Player1", "0123")
    
    # Try to guess again
    with pytest.raises(ValueError, match="Game is already finished"):
        game.make_guess("Player1", "4444")


def test_game_invalid_guess_raises_error():
    """Test that invalid guesses raise appropriate errors."""
    rules = Rules(length=4, alphabet="012345")
    game = Game(rules=rules, mode="pvp", max_attempts=10, secret="0123")
    
    # Wrong length
    with pytest.raises(ValueError):
        game.make_guess("Player1", "012")
    
    # Invalid character
    with pytest.raises(ValueError):
        game.make_guess("Player1", "012X")


def test_game_remaining_attempts_decrements():
    """Test that remaining attempts decrements correctly."""
    rules = Rules(length=4, alphabet="012345")
    game = Game(rules=rules, mode="pvp", max_attempts=5, secret="0123")
    
    assert game.remaining_attempts() == 5
    
    game.make_guess("Player1", "1111")
    assert game.remaining_attempts() == 4
    
    game.make_guess("Player1", "2222")
    assert game.remaining_attempts() == 3


def test_game_pvc_mode_full_game():
    """Test a full game in pvc mode."""
    rules = Rules(length=4, alphabet="012345")
    game = Game(rules=rules, mode="pvc", max_attempts=10)
    
    # We don't know the secret, but we can guess it
    secret = game.secret
    
    # Make a wrong guess
    result1 = game.make_guess("Player1", "0000")
    assert result1["is_finished"] is False
    
    # Make the correct guess
    result2 = game.make_guess("Player1", secret)
    assert result2["is_finished"] is True
    assert result2["won"] is True


def test_game_with_no_duplicates_rule():
    """Test game with no duplicates allowed."""
    rules = Rules(length=4, alphabet="012345", allow_duplicates=False)
    game = Game(rules=rules, mode="pvp", max_attempts=10, secret="0123")
    
    # Valid guess without duplicates
    result = game.make_guess("Player1", "4521")
    assert result["attempts_used"] == 1
    
    # Invalid guess with duplicates
    with pytest.raises(ValueError):
        game.make_guess("Player1", "1123")


def test_game_invalid_secret_raises_error():
    """Test that providing an invalid secret raises an error."""
    rules = Rules(length=4, alphabet="012345")
    
    # Secret with invalid character
    with pytest.raises(ValueError):
        Game(rules=rules, mode="pvp", max_attempts=10, secret="012X")
    
    # Secret with wrong length
    with pytest.raises(ValueError):
        Game(rules=rules, mode="pvp", max_attempts=10, secret="012")

# tests/test_cli.py
import sys
import pytest


sys.modules.pop("mastermind", None)
sys.modules.pop("mastermind.cli", None)

import mastermind.cli as cli_mod  # noqa: E402


def test_cli_help_exits_with_zero():
  
    old_argv = sys.argv.copy()
    try:
        sys.argv = ["mastermind", "--help"]
        with pytest.raises(SystemExit) as e:
            cli_mod.main()
        assert e.value.code == 0
    finally:
        sys.argv = old_argv


def test_cli_play_help_exits_with_zero():
   
    old_argv = sys.argv.copy()
    try:
        sys.argv = ["mastermind", "play", "--help"]
        with pytest.raises(SystemExit) as e:
            cli_mod.main()
        assert e.value.code == 0
    finally:
        sys.argv = old_argv


def test_play_pvc_quick_win(capsys, monkeypatch, tmp_path):
    """Test PvC mode with a quick win."""
    # Patch the Game class to use a known secret
    from mastermind.game import Game
    original_init = Game.__init__
    
    def mock_init(self, rules, mode, max_attempts, secret=None):
        # Force a known secret
        original_init(self, rules, mode, max_attempts, secret="0123")
    
    monkeypatch.setattr(Game, "__init__", mock_init)
    
    # Mock user inputs: name, then winning guess
    inputs = iter(["TestPlayer", "0123"])
    monkeypatch.setattr("builtins.input", lambda *a, **k: next(inputs))
    
    # Use tmp_path for scores
    monkeypatch.setattr("mastermind.cli.save_score", lambda entry, path="scores.json": None)
    monkeypatch.setattr("mastermind.cli.top_scores", lambda limit=10, path="scores.json": [])
    
    cli_mod.play(length=4, alphabet="012345", allow_duplicates=True, mode="pvc", max_attempts=10)
    
    out = capsys.readouterr().out
    assert "Mastermind - PVC Mode" in out
    assert "4 bulls" in out
    assert "Congratulations" in out
    assert "won in 1 attempts" in out


def test_play_pvc_with_max_attempts_loss(capsys, monkeypatch, tmp_path):
    """Test PvC mode losing by reaching max attempts."""
    from mastermind.game import Game
    original_init = Game.__init__
    
    def mock_init(self, rules, mode, max_attempts, secret=None):
        original_init(self, rules, mode, max_attempts, secret="0123")
    
    monkeypatch.setattr(Game, "__init__", mock_init)
    
    # Mock inputs: name, then 3 wrong guesses
    inputs = iter(["TestPlayer", "1111", "2222", "3333"])
    monkeypatch.setattr("builtins.input", lambda *a, **k: next(inputs))
    
    # Mock scoreboard functions
    monkeypatch.setattr("mastermind.cli.save_score", lambda entry, path="scores.json": None)
    monkeypatch.setattr("mastermind.cli.top_scores", lambda limit=10, path="scores.json": [])
    
    cli_mod.play(length=4, alphabet="012345", allow_duplicates=True, mode="pvc", max_attempts=3)
    
    out = capsys.readouterr().out
    assert "Game Over" in out
    assert "The secret was: 0123" in out
    assert "Your score: 0" in out


def test_play_pvp_mode(capsys, monkeypatch, tmp_path):
    """Test PvP mode where Player 1 sets secret and Player 2 guesses."""
    # Mock inputs: player1 name, player2 name, secret, then winning guess
    inputs = iter(["Alice", "Bob", "0123"])
    monkeypatch.setattr("builtins.input", lambda *a, **k: next(inputs))
    
    # Mock getpass for secret input
    monkeypatch.setattr("mastermind.cli.getpass", lambda *a, **k: "0123")
    
    # Mock scoreboard functions
    monkeypatch.setattr("mastermind.cli.save_score", lambda entry, path="scores.json": None)
    monkeypatch.setattr("mastermind.cli.top_scores", lambda limit=10, path="scores.json": [])
    
    cli_mod.play(length=4, alphabet="012345", allow_duplicates=True, mode="pvp", max_attempts=10)
    
    out = capsys.readouterr().out
    assert "Mastermind - PVP Mode" in out
    assert "Alice" in out
    assert "Bob" in out
    assert "Congratulations Bob" in out


def test_play_invalid_then_valid_guess(capsys, monkeypatch):
    """Test handling of invalid guesses followed by valid guess."""
    from mastermind.game import Game
    original_init = Game.__init__
    
    def mock_init(self, rules, mode, max_attempts, secret=None):
        original_init(self, rules, mode, max_attempts, secret="0123")
    
    monkeypatch.setattr(Game, "__init__", mock_init)
    
    # Mock inputs: name, invalid guess (too short), invalid guess (bad char), valid winning guess
    inputs = iter(["TestPlayer", "12", "0x23", "0123"])
    monkeypatch.setattr("builtins.input", lambda *a, **k: next(inputs))
    
    # Mock scoreboard functions
    monkeypatch.setattr("mastermind.cli.save_score", lambda entry, path="scores.json": None)
    monkeypatch.setattr("mastermind.cli.top_scores", lambda limit=10, path="scores.json": [])
    
    cli_mod.play(length=4, alphabet="012345", allow_duplicates=True, mode="pvc", max_attempts=10)
    
    out = capsys.readouterr().out
    assert "Invalid guess" in out
    assert "Congratulations" in out


def test_main_default_runs_pvc(monkeypatch, capsys):
    """Test that main() runs PvC mode by default."""
    old_argv = sys.argv.copy()
    try:
        sys.argv = ["mastermind"]
        
        from mastermind.game import Game
        original_init = Game.__init__
        
        def mock_init(self, rules, mode, max_attempts, secret=None):
            original_init(self, rules, mode, max_attempts, secret="0123")
        
        monkeypatch.setattr(Game, "__init__", mock_init)
        monkeypatch.setattr("builtins.input", lambda *a, **k: "TestPlayer" if "name" in a[0].lower() else "0123")
        monkeypatch.setattr("mastermind.cli.save_score", lambda entry, path="scores.json": None)
        monkeypatch.setattr("mastermind.cli.top_scores", lambda limit=10, path="scores.json": [])
        
        cli_mod.main()
        out = capsys.readouterr().out
        assert "Mastermind - PVC Mode" in out
        assert "Congratulations" in out
    finally:
        sys.argv = old_argv


def test_main_with_mode_argument(monkeypatch, capsys):
    """Test that --mode argument works."""
    old_argv = sys.argv.copy()
    try:
        sys.argv = ["mastermind", "--mode", "pvp", "--max-attempts", "5"]
        
        # Mock inputs for PvP
        inputs = iter(["Alice", "Bob", "0123"])
        monkeypatch.setattr("builtins.input", lambda *a, **k: next(inputs))
        monkeypatch.setattr("mastermind.cli.getpass", lambda *a, **k: "0123")
        monkeypatch.setattr("mastermind.cli.save_score", lambda entry, path="scores.json": None)
        monkeypatch.setattr("mastermind.cli.top_scores", lambda limit=10, path="scores.json": [])
        
        cli_mod.main()
        out = capsys.readouterr().out
        assert "Mastermind - PVP Mode" in out
        assert "Max attempts: 5" in out
    finally:
        sys.argv = old_argv


def test_play_shows_attempt_counter(capsys, monkeypatch):
    """Test that attempt counter is displayed."""
    from mastermind.game import Game
    original_init = Game.__init__
    
    def mock_init(self, rules, mode, max_attempts, secret=None):
        original_init(self, rules, mode, max_attempts, secret="0123")
    
    monkeypatch.setattr(Game, "__init__", mock_init)
    
    # Make 2 wrong guesses then win
    inputs = iter(["TestPlayer", "1111", "2222", "0123"])
    monkeypatch.setattr("builtins.input", lambda *a, **k: next(inputs))
    monkeypatch.setattr("mastermind.cli.save_score", lambda entry, path="scores.json": None)
    monkeypatch.setattr("mastermind.cli.top_scores", lambda limit=10, path="scores.json": [])
    
    cli_mod.play(length=4, alphabet="012345", allow_duplicates=True, mode="pvc", max_attempts=10)
    
    out = capsys.readouterr().out
    # Check that we see results for multiple attempts and final win message
    assert "Result:" in out
    assert "bulls" in out
    assert "Congratulations" in out
    assert "won in 3 attempts" in out



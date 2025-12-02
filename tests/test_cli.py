# tests/test_cli.py
import sys
import pytest


sys.modules.pop("mastermind", None)
sys.modules.pop("mastermind.cli", None)

import mastermind.cli as cli_mod  # noqa: E402
from mastermind.engine import Rules  


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


def test_play_quick_win_with_patched_secret(capsys, monkeypatch):
    
    monkeypatch.setattr(cli_mod, "generate_secret", lambda rules: "0123")
 
    inputs = iter(["0123"])
    monkeypatch.setattr("builtins.input", lambda *a, **k: next(inputs))

    cli_mod.play(length=4, alphabet="012345", allow_duplicates=True, seed=None)

    out = capsys.readouterr().out
    assert "Mastermind started:" in out
    assert "Result: bulls=4, cows=0" in out
    assert "You won" in out


def test_play_invalid_then_valid(capsys, monkeypatch):
  
    monkeypatch.setattr(cli_mod, "generate_secret", lambda rules: "0123")
    inputs = iter(["12", "0x23", "0123"])
    monkeypatch.setattr("builtins.input", lambda *a, **k: next(inputs))

    cli_mod.play(length=4, alphabet="012345", allow_duplicates=True, seed=None)

    out = capsys.readouterr().out
    assert "Invalid guess" in out
    assert "Result: bulls=" in out
    assert "You won" in out


def test_main_default_path_runs_play_and_finishes(monkeypatch, capsys):
  
    old_argv = sys.argv.copy()
    try:
        sys.argv = ["mastermind"] 
        monkeypatch.setattr(cli_mod, "generate_secret", lambda rules: "0123")
        monkeypatch.setattr("builtins.input", lambda *a, **k: "0123")
        cli_mod.main()  
        out = capsys.readouterr().out
        assert "Mastermind started:" in out and "You won" in out
    finally:
        sys.argv = old_argv


def test_generate_secret_with_duplicates(monkeypatch):
    
    rules = Rules(length=5, alphabet="0123", allow_duplicates=True)

 
    class DummyRNG:
        def choice(self, seq):  # noqa: D401
            return seq[0]
    dummy = DummyRNG()

    monkeypatch.setattr("random.choice", dummy.choice)
    secret = cli_mod.generate_secret(rules)
    assert len(secret) == 5
    assert set(secret).issubset(set(rules.alphabet))


def test_generate_secret_no_duplicates_valid(monkeypatch):

    rules = Rules(length=3, alphabet="0123", allow_duplicates=False)

    
    monkeypatch.setattr("random.sample", lambda seq, k: list(seq[:k]))
    secret = cli_mod.generate_secret(rules)
    assert len(secret) == 3
    assert len(set(secret)) == 3
    assert set(secret).issubset(set(rules.alphabet))


def test_generate_secret_no_duplicates_error():

    rules = Rules(length=3, alphabet="01", allow_duplicates=False)
    with pytest.raises(ValueError):
        _ = cli_mod.generate_secret(rules)

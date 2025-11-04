"""
Simple Command Line Interface (CLI) for playing Mastermind.

We intentionally use only the Python standard library (argparse + random)
to avoid extra dependencies in Sprint 1.
"""

import argparse
import random
from typing import Optional

from .engine import Rules, validate_guess, score


def generate_secret(rules: Rules) -> str:
    """Create a secret code according to the current Rules."""
    if rules.allow_duplicates:
        return "".join(random.choice(rules.alphabet) for _ in range(rules.length))
    # Without duplicates we must sample unique symbols
    if rules.length > len(rules.alphabet):
        raise ValueError("length cannot exceed the number of unique symbols in the alphabet.")
    return "".join(random.sample(rules.alphabet, rules.length))


def play(length: int, alphabet: str, allow_duplicates: bool, seed: Optional[int] = None) -> None:
    """
    Run an interactive game loop in the terminal.

    Args:
        length: length of the secret code.
        alphabet: allowed symbols (string).
        allow_duplicates: whether repeated symbols are permitted.
        seed: optional random seed for reproducibility (useful in tests/demos).
    """
    if seed is not None:
        random.seed(seed)

    rules = Rules(length=length, alphabet=alphabet, allow_duplicates=allow_duplicates)
    secret = generate_secret(rules)

    print(f"Mastermind started: length={length}, alphabet={alphabet}, allow_duplicates={allow_duplicates}")
    attempts = 0

    while True:
        guess = input("Your guess: ").strip()
        try:
            validate_guess(guess, rules)
        except ValueError as e:
            print(f"Invalid guess: {e}")
            continue

        attempts += 1
        bulls, cows = score(secret, guess)
        print(f"Result: bulls={bulls}, cows={cows}")

        if bulls == length:
            print(f"🎉 You won in {attempts} attempts!")
            break


def main() -> None:
    """
    Entry point registered via console_scripts in pyproject.toml:
      $ mastermind play --length 4 --alphabet 012345 --no-duplicates
    """
    parser = argparse.ArgumentParser(prog="mastermind", description="Play Mastermind in your terminal.")
    parser.add_argument("--length", type=int, default=4, help="Code length (default: 4)")
    parser.add_argument("--alphabet", type=str, default="012345", help="Allowed symbols, e.g., '012345' or 'ABCDEF'")
    parser.add_argument("--allow-duplicates", action="store_true", default=True, help="Allow repeated symbols (default)")
    parser.add_argument("--no-duplicates", dest="allow_duplicates", action="store_false", help="Disallow duplicates")
    parser.add_argument("--seed", type=int, default=None, help="Optional RNG seed for reproducible sessions")

    # subcommand pattern (kept for future extensibility)
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("play", help="Start the interactive game")

    args = parser.parse_args()

    # default to 'play' if no subcommand is given
    if args.command is None or args.command == "play":
        play(args.length, args.alphabet, args.allow_duplicates, args.seed)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

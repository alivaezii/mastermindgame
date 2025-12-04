"""
Command Line Interface (CLI) for playing Mastermind.

Supports two game modes:
- Player vs Computer (pvc): Computer generates the secret
- Player vs Player (pvp): One player sets the secret, another guesses

Uses only the Python standard library.
"""

import argparse
import random
from getpass import getpass
from typing import Optional

from .engine import Rules
from .game import Game
from .scoreboard import ScoreEntry, calculate_score, save_score, top_scores


def play(
    length: int,
    alphabet: str,
    allow_duplicates: bool,
    mode: str = "pvc",
    max_attempts: int = 10,
    seed: Optional[int] = None
) -> None:
    """
    Run an interactive game loop in the terminal.
    """
    if seed is not None:
        random.seed(seed)

    rules = Rules(length=length, alphabet=alphabet, allow_duplicates=allow_duplicates)

    print(f"Mastermind - {mode.upper()} Mode")
    print(f"Rules: length={length}, alphabet={alphabet}, allow_duplicates={allow_duplicates}")
    print(f"Max attempts: {max_attempts}\n")

    # Handle different game modes
    if mode == "pvc":
        player_name = input("Enter your name: ").strip() or "Player"
        game = Game(rules=rules, mode="pvc", max_attempts=max_attempts)
        guesser_name = player_name
        print(f"\nWelcome {player_name}! The computer has generated a secret code.")
        print("Try to guess it!\n")

    elif mode == "pvp":
        player1_name = input("Player 1 name (code setter): ").strip() or "Player1"
        player2_name = input("Player 2 name (code breaker): ").strip() or "Player2"

        print(f"\n{player1_name}, please enter the secret code.")
        print("(It will not be displayed on screen)")

        while True:
            secret = getpass(
                f"Secret code ({length} characters from '{alphabet}'): "
            ).strip()
            try:
                from .engine import validate_guess
                validate_guess(secret, rules)
                break
            except ValueError as e:
                print(f"Invalid secret: {e}")
                print("Please try again.\n")

        game = Game(rules=rules, mode="pvp", max_attempts=max_attempts, secret=secret)
        guesser_name = player2_name
        print(f"\n{player2_name}, try to guess {player1_name}'s secret code!\n")

    else:
        raise ValueError(f"Unknown mode: {mode}")

    # Main game loop
    while not game.is_over():
        attempt_num = game.attempts_used + 1

        guess = input(
            f"Attempt {attempt_num}/{max_attempts} - Your guess: "
        ).strip()

        try:
            result = game.make_guess(guesser_name, guess)
        except ValueError as e:
            print(f"Invalid guess: {e}\n")
            continue

        bulls = result["bulls"]
        cows = result["cows"]
        print(f"Result: {bulls} bulls, {cows} cows")

        if result["is_finished"]:
            if result["won"]:
                print(
                    f"\nCongratulations {guesser_name}! "
                    f"You won in {result['attempts_used']} attempts!"
                )
            else:
                print(f"\nGame Over! You've used all {max_attempts} attempts.")
                print(f"The secret was: {result['secret']}")
            print()
            break
        else:
            print(f"Remaining attempts: {result['remaining_attempts']}\n")

    # Calculate and save score
    score_value = calculate_score(
        won=game.won,
        attempts_used=game.attempts_used,
        max_attempts=max_attempts,
        mode=mode
    )

    print(f"Your score: {score_value}")

    entry = ScoreEntry(
        player_name=guesser_name,
        mode=mode,
        won=game.won,
        attempts_used=game.attempts_used,
        max_attempts=max_attempts,
        score=score_value,
        timestamp=""
    )

    save_score(entry)
    print("Score saved!\n")

    # Display top scores
    print("Top 5 Scores:")
    print("-" * 60)
    top = top_scores(limit=5)
    if top:
        for i, e in enumerate(top, 1):
            won_flag = "YES" if e.won else "NO"
            print(
                f"{i}. {e.player_name:15} | {won_flag} | Score: {e.score:3} | "
                f"{e.mode.upper()} | {e.attempts_used}/{e.max_attempts} attempts"
            )
    else:
        print("No scores yet. You're the first!")
    print("-" * 60)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="mastermind",
        description="Play Mastermind in your terminal."
    )
    parser.add_argument("--length", type=int, default=4)
    parser.add_argument("--alphabet", type=str, default="012345")
    parser.add_argument("--allow-duplicates", action="store_true", default=True)
    parser.add_argument("--no-duplicates", dest="allow_duplicates", action="store_false")
    parser.add_argument("--mode", type=str, choices=["pvc", "pvp"], default="pvc")
    parser.add_argument("--max-attempts", type=int, default=10)
    parser.add_argument("--seed", type=int, default=None)

    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("play", help="Start the interactive game")

    args = parser.parse_args()

    if args.command is None or args.command == "play":
        play(
            args.length,
            args.alphabet,
            args.allow_duplicates,
            args.mode,
            args.max_attempts,
            args.seed
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

cat <<EOF > CONTRIBUTING.md
# Hey! Thanks for helping with Mastermind!

We're super excited that you want to jump in and contribute! Just a heads-up: we like to keep our code clean and tidy so the project stays easy to manage for everyone.

## Getting Started

1.  **Grab a copy**: Fork this repo and clone it to your local machine.
2.  **Get set up**: Create a virtual environment and install the tools you'll need:
    \`\`\`bash
    pip install -e .[dev]
    \`\`\`
3.  **Keep it clean**:
      - **Type Hints**: Please don't forget them! We use type hints for everything.
      - **Formatting**: Let the robots handle the style. Just run \`black\` and \`isort\` before you commit.
      - **Linting**: Make sure \`flake8\` is happy and doesn't throw any errors.
4.  **Test, test, test**:
      - Adding a cool new feature? Make sure to write a test for it!
      - We aim high here—try to keep code coverage at **90%** or better.
      - Give \`pytest\` a quick run before you push your changes.

## Ready to Merge?

  - Send your Pull Request over to the \`develop\` branch.
  - Wait for those green checkmarks from GitHub Actions (the CI pipeline).
  - Let us know what you did! Write a clear description in your PR so we know what's up.

Happy coding! 🚀
EOF

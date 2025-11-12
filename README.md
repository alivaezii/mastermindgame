# 🎮 Mastermind Game (Python)

A simple command-line implementation of the classic **Mastermind** logic game, built to demonstrate clean software design, testing, and CI/CD automation principles using Python.

---

## 🚀 Quick Start

### 1. Create and activate environment
```bash
conda env create -f environment.yml
conda activate mastermind
```

### 2. Run the game
```bash
python -m mastermind
```

### 3. Run tests
```bash
pytest
```

---

## 🧪 Testing & Code Quality

This project follows a lightweight yet strict **Testing and Quality Policy**:

| Area | Tool | Purpose |
|------|------|----------|
| **Testing** | `pytest` + `pytest-cov` | Unit & CLI tests, min. 85% coverage |
| **Formatting** | `black` + `isort` | Code formatting & import sorting |
| **Linting** | `flake8` | Static code analysis |
| **Pre-commit** | `pre-commit` | Auto-runs all checks before pushing |
| **CI/CD** | GitHub Actions | Multi-version tests (Python 3.10 & 3.11) |

📄 For full details: [Quality & CI/CD Policy](./docs/Quality_Testing_CICD_Policy.md)

---

## 📂 Project Structure
```
mastermindgame/
│
├── src/mastermind/
│   ├── __init__.py
│   ├── engine.py
│   ├── cli.py
│
├── tests/
│   ├── test_engine.py
│   └── test_cli.py
│
├── environment.yml
├── pyproject.toml
└── .github/workflows/ci.yml
```

---

## ⚙️ Continuous Integration (CI)

All commits and pull requests trigger an automated workflow that performs:

1. Environment setup via **Conda**
2. Auto-formatting using **isort** and **black**
3. Linting with **flake8**
4. Running **pytest** for all unit and CLI tests
5. Enforcing **coverage ≥ 85%**

If all stages pass, the build turns ✅ green in GitHub Actions.

---

## 🤝 Contributing

1. Fork this repository  
2. Create a new branch: `feature/my-feature`  
3. Run local quality checks before committing:
   ```bash
   isort . && black . && flake8 . && pytest
   ```
4. Submit a Pull Request — all CI jobs must pass before merge.

---

## 🧱 Built With
- Python 3.10 / 3.11
- Conda environment management
- pytest + coverage
- black / isort / flake8 / pre-commit
- GitHub Actions for CI/CD automation

---

## 📝 License
MIT License © 2025  
Developed by **Hochschule Campus Wien**

---

### 💡 Related Documentation
- [Quality Assurance & CI/CD Policy](./Quality_Testing_CICD_Policy.md)
- [Python ↔ Java Toolchain Comparison](./Python_vs_Java_Tooling.md)

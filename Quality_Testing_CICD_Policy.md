# Quality Assurance, Testing Strategy & CI/CD Automation Policy

## 🎯 Objectives
- **Reliability:** Ensure consistent behavior across supported Python versions (3.10 and 3.11).
- **Maintainability:** Keep the codebase clean, readable, and standardized.
- **Automation:** Fully automate testing, linting, and formatting through CI/CD workflows.
- **Transparency:** Provide traceable quality gates (linting, formatting, and coverage) for every commit and pull request.

## 🧪 Testing Strategy

### Test Levels
- **Unit Tests:** Validate core logic in the `engine` module and scoring functions. All functions must be *pure* (side-effect-free) and deterministic.
- **CLI Tests (Non-Interactive):** Validate CLI behavior for commands such as `--help`, successful exit codes, and argument validation.
- **(Optional) Integration Smoke Tests:** Run minimal end-to-end scenarios to ensure CLI ↔ engine interaction works correctly.

### Test Design Guidelines
- Each test should focus on **one clear behavior** (Given-When-Then structure).
- Avoid randomness or I/O dependencies (use `random.seed(42)` if randomness is needed).
- Use meaningful test names following the pattern `test_<behavior>_<expected>()`.
- Ensure deterministic outcomes for reproducibility in CI.

### Code Coverage
- **Minimum required coverage:** 85% (target: 90%).
- **Local execution:**
  ```bash
  pytest --cov=mastermind --cov-report=term-missing
  ```
- Coverage reports list missing lines to guide improvement.

## 🧹 Code Quality & Linting Standards

### Format & Style Tools
| Tool | Purpose | Config |
|------|----------|--------|
| **Black** | Auto-formatter for uniform code style | `line-length = 130` |
| **isort** | Auto-sorts imports (aligned with Black) | `profile = black` |
| **Flake8** | Static linting and rule enforcement | `max-line-length = 130` |

### Flake8 Rules
- Ignore rules: `E203, W503, W291, W293, E303`
- Per-file ignores:
  ```
  tests/*: E501, E402
  ```
- This ensures flexibility for test files while keeping production code strict.

### Local Quality Check
```bash
isort .
black .
flake8 .
pytest
```

## 🧩 Pre-commit Hooks
All developers must install and use `pre-commit` to ensure code quality before pushing:
```bash
pre-commit install
pre-commit run --all-files
```
CI will also enforce the same checks for consistency across environments.

## ⚙️ CI/CD Automation (GitHub Actions)

### Overview
- Runs automatically on every **push** or **pull request** to `main` or `develop`.
- Supports manual execution via `workflow_dispatch`.
- Executes under **Ubuntu** using **Miniconda** for environment management.
- Uses a **matrix build** for Python versions `3.10` and `3.11`.

### Pipeline Stages
1. **Checkout:** Fetch the latest repository state.
2. **Environment Setup:** Create conda environment from `environment.yml`.
3. **Install Package:**
   ```bash
   pip install -e .
   ```
4. **Auto-format (Quality Automation):**
   ```bash
   isort .
   black .
   ```
5. **Lint Check:**
   ```bash
   flake8 .
   ```
6. **Run Tests with Coverage:**
   ```bash
   pytest
   ```

### CI Configuration Key Points
- `fail-fast: false` → ensures both Python versions complete even if one fails.
- Conda channels: `conda-forge, defaults` with `channel-priority: strict`.
- Optional optimization: `use-mamba: true` for faster dependency resolution.
- Coverage and linting act as **quality gates** before merging.

## ✅ Definition of Done (DoD)
A feature or pull request is considered *done* when:
1. All **CI jobs are green** (Black, isort, Flake8, Pytest).
2. Code coverage ≥ **85%**.
3. No new Flake8 violations introduced.
4. Commit messages follow semantic naming (e.g., `feat:`, `fix:`, `test:`, `refactor:`).
5. PR includes a clear description of changes and relevant tests.

## 🧱 Branching & Merge Policy
- **Feature branches:** `feature/<short-name>`
- **Protected branches:** `main`, `develop` (require PR + passing CI).
- **Merging:**
  - Use **Squash & Merge** for concise, meaningful history.
  - CI must pass before merge approval.

## 🧠 Local Development Workflow
```bash
conda env create -f environment.yml -n mastermind
conda activate mastermind

# Before commit or push:
isort . && black . && flake8 .
pytest
```

## 🧾 Summary
- **Test Pyramid:** Focused on Unit & CLI Non-Interactive testing.
- **Quality Gate:** Auto-format + lint + minimum coverage enforcement.
- **Reliability:** Deterministic tests and multi-Python validation.
- **Automation:** Full CI/CD pipeline with pre-commit alignment.
- **Developer Experience:** Clear local workflow and consistent rules between dev and CI.

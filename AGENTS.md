# AGENTS.md - My Swiss Army Knife

A monorepo for personal tools and documentation, primarily Python-based and managed with `uv`.

## 🛠 Tech Stack
- **Language:** Python 3.12+
- **Dependency Manager:** [uv](https://github.com/astral-sh/uv)
- **CLIs:** Click
- **Documentation:** Markdown

## 📁 Directory Structure
- `apps/`: Standalone Python applications.
  - `datetime-calculator/`: CLI for date arithmetic (`dt-calc`).
  - `google-sheets-merger/`: CLI to merge Google Sheets (`gs-merge`).
- `scripts/`: Shell automation (currently empty).
- `docs/`: General documentation and notes.

## 🚀 Common Commands

### Root Commands
- **Sync all environments:** `uv sync`

### Datetime Calculator (`apps/datetime-calculator`)
- **Run tool:** `uv run dt-calc --help`
- **Run tests:** `uv run pytest` (from the app directory)
- **Run specific test:** `uv run pytest tests/test_main.py`

### Google Sheets Merger (`apps/google-sheets-merger`)
- **Run tool:** `uv run gs-merge --help`
- **Dependencies:** Requires `credentials.json` in the app directory for Google API access.
- **Cache:** Local data cached in `.cache/`.

## 🏛 Architecture & Patterns
- **CLI first:** Tools are designed as command-line utilities using `click`.
- **Flat structure:** Logic is typically contained within a single main file or a simple module structure within each app.
- **Monorepo:** Use `uv` to manage environments. Apps are independent but live in the same repo.

## 📝 Conventions
- **Tooling:** Always use `uv run` to execute scripts and tests.
- **Testing:** New apps should include a `tests/` directory with `pytest`.
- **Docs:** Each app must have its own `README.md` and `docs/` if necessary.

## ⚠️ Constraints & Gotchas
- **Python Version:** Strictly 3.12+ as specified in `pyproject.toml`.
- **Google API:** `google-sheets-merger` requires manual OAuth setup (see its README).
- **Environment:** Do not use `pip` or `poetry`; stick to `uv`.

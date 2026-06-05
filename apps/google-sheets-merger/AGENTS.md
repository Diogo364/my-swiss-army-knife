# AGENTS.md - Google Sheets Merger

CLI tool to merge multiple Google Sheets into a single destination.

## 🚀 Commands
- **Run CLI:** `uv run gs-merge --help`
- **Manual Run:** `uv run python main.py`

## 📁 Structure
- `main.py`: Core logic and CLI entry point.
- `.cache/`: Local CSV caches of processed sheets.

## ⚠️ Requirements
- **Auth:** Requires `credentials.json` in this directory (Google Cloud OAuth2 Desktop credentials).
- **Tokens:** `token.json` is generated after first successful auth.

## 📝 Details
- Uses `pandas` for data merging and `gspread` for Google Sheets interaction.
- Managed by `uv`.

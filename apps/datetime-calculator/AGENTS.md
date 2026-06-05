# AGENTS.md - Datetime Calculator

CLI tool for robust date arithmetic, specifically handling business days and month/year clamping.

## 🛠 Tech Stack
- **CLI Framework:** [Click](https://click.palletsprojects.com/)
- **Date Logic:** Standard `datetime` + `dateutil.relativedelta` (for complex month/year math).
- **Testing:** `pytest` + `pytest-mock`.

## 🚀 Common Commands
- **Run Tool:** `uv run dt-calc "2024-01-01" "+ 15 wd"`
- **Run Tests:** `uv run pytest`
- **Run with Verbose Output:** `uv run dt-calc "+ 1 week" -v`

## 📁 Key Files
- `datetime_calculator.py`: Contains the logic for parsing operations and calculating results.
  - `parse_operation(str)`: Regex-based parser for `[+-] [amount] [unit]`.
  - `calculate(date, op, amount, unit)`: Core arithmetic engine.
- `tests/test_main.py`: Comprehensive tests covering edge cases like leap years and month-end clamping.

## 🏛 Architecture & Patterns
- **Working Days (`wd`):** Calculated via a loop that skips `weekday() >= 5` (Saturday/Sunday).
- **Month/Year Clamping:** Uses `dateutil.relativedelta` which automatically handles logic like "Jan 31st + 1 month = Feb 28th/29th".
- **Flexible CLI Input:** `main()` handles optional date arguments. If the first argument matches `[+-]`, it assumes the date is `today()`.

## 🧪 Testing Guidelines
- **Mocking `today()`:** Use `pytest-mock` to patch `datetime_calculator.date` (see `test_cli_default_today` in `test_main.py`).
- **Operation Strings:** Always test with quoted strings in the CLI (e.g., `"+ 5 days"`) to ensure the shell doesn't split the operator.

## ⚠️ Constraints
- **Python Version:** 3.12+
- **Unit Support:** `days`, `wd`/`working-days`, `weeks`, `months`, `years`.

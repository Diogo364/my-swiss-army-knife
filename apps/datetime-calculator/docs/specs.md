# Project: Datetime Calculator CLI

A command-line tool for performing quick calendar arithmetic, specifically tailored for business and project planning needs.

# Real Problem
Users often need to calculate deadlines or milestones based on different types of intervals (calendar days vs. working days) which are tedious to calculate manually.
Example scenarios:
- "What is the date 15 working days from today?"
- "What was the date 3 months before a specific launch?"

# High-level Requirements

## 1. Input Specifications
- **Base Date:** 
  - Format: `YYYY-MM-DD` (ISO 8601).
  - Default: Today's date if not provided.
- **Operation:**
  - Syntax: `[operator] [amount] [unit]` (e.g., `+ 15 days`, `- 2 months`).
  - **Operators:** `+` (add), `-` (subtract).
  - **Units:** 
    - `days` (calendar days)
    - `wd` or `working-days` (Monday to Friday)
    - `weeks` (calendar weeks)
    - `months` (calendar months)
    - `years` (calendar years)

## 2. Business Rules
- **Working Days:** Saturday and Sunday are excluded. Public holidays are NOT excluded in the initial version to keep it simple.
- **Month Arithmetic:** Adding 1 month to Jan 31st results in Feb 28th (or 29th), not March 3rd (clamping to end of month).
- **Timezone:** All operations are performed in the local system timezone.

## 3. CLI Interface
The script should be invoked via `dt-calc`.
- **Command structure:** `dt-calc [DATE] [OPERATION]`
- **Examples:**
  - `dt-calc 2023-10-27 "+ 15 wd"`
  - `dt-calc -- "+ 10 days"` (using today as default)

## 4. Output
- **Format:** `YYYY-MM-DD` (Standard)
- **Optional:** A verbose mode that includes the day of the week (e.g., `2023-11-15 (Wednesday)`).

# Techstack
- **Language:** Python 3.12+
- **Environment Management:** [uv](https://github.com/astral-sh/uv)
- **CLI Framework:** [Click](https://click.palletsprojects.com/)
- **Core Library:** `datetime` (standard library) or `python-dateutil` for complex month logic.

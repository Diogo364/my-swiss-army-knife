# Datetime Calculator CLI

A robust command-line interface for performing date arithmetic, built with Python, Click, and `python-dateutil`.

## Features

- **Standard Arithmetic**: Add or subtract days, weeks, months, and years.
- **Working Days**: Calculate dates excluding weekends (Saturday and Sunday).
- **Month Clamping**: Automatically handles month-end logic (e.g., adding 1 month to January 31st results in February 28th or 29th).
- **Flexible Input**: Supports specific start dates (ISO 8601) or defaults to today.
- **Verbose Output**: Optionally include the day of the week in the result.

## Installation

This project uses [`uv`](https://github.com/astral-sh/uv) for dependency management and packaging.

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd apps/datetime-calculator
    ```

2.  **Install dependencies and the CLI tool**:
    ```bash
    uv sync
    ```

This will create a virtual environment and install the `dt-calc` script as an entry point.

## Usage

The general syntax is:
```bash
dt-calc [DATE] [OPERATION] [FLAGS]
```

-   **`DATE`**: Optional. Start date in `YYYY-MM-DD` format. Defaults to today's date if omitted.
-   **`OPERATION`**: Required. A string in the format `"[operator] [amount] [unit]"`.
    -   **Operator**: `+` or `-`.
    -   **Amount**: A positive integer.
    -   **Unit**: `days`, `wd` (working days), `weeks`, `months`, or `years` (singular forms also supported).
-   **`FLAGS`**:
    -   `--verbose` or `-v`: Appends the name of the weekday to the output.

### Examples

**1. Basic addition (relative to today):**
```bash
dt-calc "+ 10 days"
# Output: 2024-06-12 (assuming today is 2024-06-02)
```

**2. Adding working days to a specific date:**
```bash
dt-calc 2024-01-01 "+ 15 wd"
# Output: 2024-01-22
```

**3. Month clamping logic:**
```bash
dt-calc 2024-01-31 "+ 1 month"
# Output: 2024-02-29 (2024 is a leap year)
```

**4. Verbose output:**
```bash
dt-calc 2024-12-25 "+ 1 week" --verbose
# Output: 2025-01-01 (Wednesday)
```

**5. Multi-part operation (using shell quotes):**
```bash
dt-calc "- 2 years" -v
# Output: 2022-06-02 (Thursday)
```

## Development

### Running Tests
Tests are located in the `tests/` directory and use `pytest` with `pytest-mock`.

```bash
uv run pytest
```

### Project Structure
- `datetime_calculator.py`: Main logic and CLI definition.
- `pyproject.toml`: Project metadata and dependencies.
- `tests/test_main.py`: Comprehensive test suite.

## License
MIT

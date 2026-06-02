# My Swiss Army Knife

A monorepo for personal tools, projects, and documentation, built primarily with **Python**, **Shell scripts**, and **Markdown**.

## 🚀 Overview

This repository is a centralized hub for my digital utility belt. It leverages **uv** for fast, reliable Python package management and environment handling.

## 🧰 Tech Stack

- **Python**: Core logic and complex utilities (managed by [uv](https://github.com/astral-sh/uv)).
- **Shell Scripts**: System automation and quick CLI shortcuts.
- **Markdown**: Documentation, notes, and personal knowledge management.

## 📁 Project Structure

```text
.
├── apps/               # Tools and applications
├── scripts/            # Shell scripts (Bash/Zsh)
├── docs/               # Documentation and Markdown notes
└── README.md           # This file
```

## 🛠️ Tools

### 📅 Datetime Calculator (`dt-calc`)
A robust CLI for date arithmetic (adding/subtracting days, working days, weeks, months, and years).
- **Location**: `apps/datetime-calculator`
- **Features**: Weekday support, month clamping, and verbose output.

### 📊 Google Sheets Merger (`gs-merge`)
A CLI tool to merge multiple Google Sheets into a single spreadsheet based on shared worksheet names.
- **Location**: `apps/google-sheets-merger`
- **Features**: OAuth2 auth, schema alignment (Union), and source tracking.

## ⚙️ Installation

You can install the tools directly from this remote repository using `pipx` or `pip`.

### 1. Installation via pipx (Recommended)
This is the preferred method for CLI tools as it installs them in isolated environments and makes them available globally.

```bash
# Install Datetime Calculator
pipx install "git+https://github.com/Diogo364/my-swiss-army-knife.git#subdirectory=apps/datetime-calculator"

# Install Google Sheets Merger
pipx install "git+https://github.com/Diogo364/my-swiss-army-knife.git#subdirectory=apps/google-sheets-merger"
```

### 2. Direct Installation via pip
Alternatively, you can install the sub-packages directly into your current environment:

```bash
pip install "git+https://github.com/Diogo364/my-swiss-army-knife.git#subdirectory=apps/datetime-calculator"
```

## 🛠️ Development

### Prerequisites

- [uv](https://github.com/astral-sh/uv) installed on your system.
- A POSIX-compliant shell (Bash, Zsh, etc.).

### Usage with uv

To set up the Python environment and sync all dependencies:

```bash
uv sync
```

To run a specific tool during development:

```bash
uv run dt-calc --help
# OR
uv run python apps/google-sheets-merger/main.py --help
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

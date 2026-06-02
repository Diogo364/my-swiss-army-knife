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

## 🛠️ Getting Started

### Prerequisites

- [uv](https://github.com/astral-sh/uv) installed on your system.
- A POSIX-compliant shell (Bash, Zsh, etc.).

### Usage with uv

To set up the Python environment:

```bash
uv sync
```

To run a specific tool:

```bash
uv run apps/path/to/tool.py
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

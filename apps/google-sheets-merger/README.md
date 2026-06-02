# Google Sheets Merger CLI

A Python CLI tool to merge multiple Google Sheets into a single destination spreadsheet based on shared worksheet names.

## Features

- **OAuth2 Authentication:** Uses standard browser-based login.
- **Worksheet Grouping:** Merges tabs with the same name across all input files.
- **Schema Alignment:** Performs a Union (outer join) to preserve all columns from all sources.
- **Source Tracking:** Adds a `source_spreadsheet_name` column to every row.
- **Local Caching:** Caches raw data locally in `.cache/` for stability and inspection.
- **Overwrite Logic:** Replaces the destination spreadsheet if it already exists.

## Prerequisites

1.  **Python & UV:** Ensure you have [uv](https://github.com/astral-sh/uv) installed.
2.  **Google Cloud Project:**
    - Go to the [Google Cloud Console](https://console.cloud.google.com/).
    - Create a new project.
    - Enable **Google Sheets API** and **Google Drive API**.
    - Configure the **OAuth consent screen** (Internal/External).
    - Create **OAuth 2.0 Client IDs** (Desktop App).
    - Download the JSON file and rename it to `credentials.json`.
    - Place `credentials.json` in the same directory as `main.py`.

## Installation

```bash
uv sync
```

## Usage

```bash
uv run python main.py "URL1" "URL2" --output-name "Merged Spreadsheet Name"
```

### Arguments

- `URLS`: One or more Google Sheet URLs (positional).
- `--output-name`: (Required) The name of the resulting spreadsheet in your Google Drive.
- `--cache-dir`: (Optional) The directory to store local caches. Defaults to `.cache`.

## How it Works

1.  **Auth:** Authenticates via browser and saves tokens to `token.json`.
2.  **Read:** Downloads data from each worksheet in every provided URL.
3.  **Process:**
    - Maps worksheet names (e.g., "Sales", "Inventory").
    - Injects the source file name into the data.
    - Saves a CSV copy in `.cache/`.
4.  **Merge:** Uses `pandas` to align columns across files for each worksheet name.
5.  **Write:** 
    - Finds any existing file with `--output-name` and deletes it.
    - Creates a new spreadsheet and populates it with the merged worksheets.

# Project
A CLI script to merge data from multiple Google Sheets into a single destination spreadsheet.

# High-level Requirements
- **Access:** Access multiple Google Spreadsheets via their full URLs provided as CLI arguments.
- **Authentication:** Use **OAuth2 User Flow** for API access (opens browser for authentication).
- **Processing:**
  - Iterate through all tabs (worksheets) in each provided spreadsheet.
  - Cache raw data locally during the process to ensure stability.
- **Merge Logic:**
  - Group worksheets by their **title**. (e.g., all tabs named "Sales" across all files will be merged into one "Sales" tab in the output).
  - **Source Identification:** Add a `source_spreadsheet_name` column to every row containing the name of the source spreadsheet.
  - **Schema Mismatch:** Perform a **Union (outer join)** of all columns. If a column exists in one source but not another, it should be included, with missing values handled appropriately.
- **Output:**
  - Save all merged tables into a single Google Spreadsheet in Google Drive.
  - **Output Behavior:** If a spreadsheet with the target name already exists, it must be **overwritten**.
  - Each unique worksheet name from the sources becomes a tab in the destination file.

# Input
- `urls`: Multiple Google Sheet URLs provided as positional command-line arguments.
- `--output-name`: The name of the resulting spreadsheet in Google Drive.

# Output
- A single merged Google Spreadsheet in the user's Google Drive.

# Techstack
- **Language:** Python
- **Environment Management:** UV
- **CLI Framework:** Click
- **Google API:** `gspread` (for sheet operations)
- **Data Handling:** `pandas` (for efficient merging and schema alignment)

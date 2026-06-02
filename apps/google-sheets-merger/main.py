import os
import os.path
import click
import gspread
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_credentials():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists("credentials.json"):
                click.echo("Error: 'credentials.json' not found. Please provide it in the current directory.")
                click.echo("Follow the instructions at: https://developers.google.com/sheets/api/quickstart/python")
                raise click.Abort()
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def get_spreadsheet_id(url):
    # Basic extraction of ID from URL
    # https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit#gid=0
    try:
        if "/d/" in url:
            return url.split("/d/")[1].split("/")[0]
        return url
    except Exception:
        return url

@click.command()
@click.argument("urls", nargs=-1, required=True)
@click.option("--output-name", required=True, help="The name of the resulting spreadsheet.")
@click.option("--cache-dir", default=".cache", help="Directory to cache raw data.")
def main(urls, output_name, cache_dir):
    """Merge multiple Google Sheets into a single destination spreadsheet."""
    creds = get_credentials()
    gc = gspread.authorize(creds)
    drive_service = build("drive", "v3", credentials=creds)

    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    merged_data = {} # worksheet_title -> list of dataframes

    for url in urls:
        ss_id = get_spreadsheet_id(url)
        try:
            ss = gc.open_by_key(ss_id)
            click.echo(f"Processing spreadsheet: {ss.title}")
            
            for ws in ss.worksheets():
                click.echo(f"  Reading worksheet: {ws.title}")
                
                # Fetch data
                data = ws.get_all_records()
                if not data:
                    continue
                
                df = pd.DataFrame(data)
                
                # Add source spreadsheet name
                df["source_spreadsheet_name"] = ss.title
                
                # Cache raw data
                cache_file = os.path.join(cache_dir, f"{ss.title}_{ws.title}.csv")
                df.to_csv(cache_file, index=False)
                
                if ws.title not in merged_data:
                    merged_data[ws.title] = []
                merged_data[ws.title].append(df)
                
        except Exception as e:
            click.echo(f"Error processing {url}: {e}")

    if not merged_data:
        click.echo("No data found to merge.")
        return

    # Merge dataframes for each worksheet title
    final_sheets = {}
    for title, dfs in merged_data.items():
        click.echo(f"Merging data for worksheet: {title}")
        # Perform union (outer join)
        combined_df = pd.concat(dfs, axis=0, ignore_index=True, sort=False)
        final_sheets[title] = combined_df

    # Output: Overwrite existing spreadsheet or create new one
    try:
        # Check if spreadsheet exists
        query = f"name = '{output_name}' and mimeType = 'application/vnd.google-apps.spreadsheet' and trashed = false"
        results = drive_service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
        files = results.get('files', [])

        if files:
            for file in files:
                click.echo(f"Overwriting existing spreadsheet: {output_name} (ID: {file['id']})")
                # We can either delete it and recreate, or open it and clear it.
                # Deleting is cleaner for "overwrite" behavior if we want to reset all tabs.
                drive_service.files().delete(fileId=file['id']).execute()
        
        # Create new spreadsheet
        click.echo(f"Creating destination spreadsheet: {output_name}")
        new_ss = gc.create(output_name)
        
        # Write merged data
        for i, (title, df) in enumerate(final_sheets.items()):
            # Fill NaN with empty string for gspread
            df = df.fillna("")
            
            if i == 0:
                # Use the first worksheet created by default
                ws = new_ss.get_worksheet(0)
                ws.update_title(title)
            else:
                ws = new_ss.add_worksheet(title=title, rows="100", cols="20")
            
            # Prepare data for update (headers + values)
            data_to_write = [df.columns.values.tolist()] + df.values.tolist()
            ws.update(data_to_write)
            click.echo(f"  Written {len(df)} rows to worksheet: {title}")

        click.echo("Successfully merged all spreadsheets.")

    except Exception as e:
        click.echo(f"Error during output: {e}")

if __name__ == "__main__":
    main()

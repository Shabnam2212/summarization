# visualize_csv.py

import pandas as pd
from IPython.display import display, HTML

def visualize_csv(csv_file_path):
    try:
        # Load the CSV
        df = pd.read_csv(csv_file_path)

        # Make DOI clickable (only if column exists)
        if 'DOI Link' in df.columns:
            df['DOI Link'] = df['DOI Link'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>' if pd.notna(x) else '')

        # Convert to HTML
        html_table = df.to_html(escape=False, index=False, classes="custom-table")

        # CSS styles
        clean_css = """
        <style>
        .custom-table {
            width: 100%;
            border-collapse: collapse;
            border: 1px solid #ccc;
            table-layout: fixed;
            word-wrap: break-word;
            font-family: Arial, sans-serif;
            font-size: 13px;
        }

        .custom-table th, .custom-table td {
            border: 1px solid #ccc;
            padding: 8px;
            text-align: left;
            vertical-align: top;
            white-space: normal;
        }

        .custom-table th:nth-child(1), .custom-table td:nth-child(1) {
            width: 7.5%;
        }

        .custom-table th:nth-child(2), .custom-table td:nth-child(2) {
            width: 16%;
        }

        .custom-table th:nth-child(3), .custom-table td:nth-child(3) {
            width: 80%;
        }

        .custom-table th {
            background-color: #f2f2f2;
        }
        </style>
        """

        # Display
        display(HTML(clean_css + html_table))

    except Exception as e:
        print(f"[Error] Could not visualize the CSV: {e}")

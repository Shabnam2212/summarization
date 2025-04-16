# visualize_csv.py

import pandas as pd
from IPython.display import display, HTML

def visualize_csv(csv_path):
    # Load your CSV
    df = pd.read_csv(csv_path)

    # Clean up any literal '\n' or newline characters
    for col in ['Folder Name', 'DOI Link', 'Summary']:
        df[col] = df[col].astype(str)
        df[col] = df[col].str.replace(r'\\n', ' ', regex=True)
        df[col] = df[col].str.replace(r'\n', ' ', regex=True)
        df[col] = df[col].str.replace(r'\\\\n', ' ', regex=True)
        df[col] = df[col].str.strip()

    # Pre-process the summary for safe insertion
    df['SummaryHTML'] = df['Summary'].apply(lambda x: x.replace('\n', '<br>'))

    # Combine content into one cell with proper formatting and line breaks
    df['Combined'] = df.apply(lambda row: (
        "<div style='font-family: Arial, sans-serif; font-size: 15px; line-height: 1.5; text-align: left;'>"
        f"<strong>PMCID:</strong> {row['Folder Name']}<br>"
        f"<strong>DOI:</strong> <a href='{row['DOI Link']}' target='_blank'>{row['DOI Link']}</a><br>"
        "<details>"
        "<summary style='margin-top: 4px;'>Click to view summary</summary>"
        f"<div style='margin-top: 5px;'>{row['SummaryHTML']}</div>"
        "</details></div>"
    ), axis=1)

    # HTML output with styling
    html_output = df[['Combined']].to_html(escape=False, index=False, header=False)

    # Add styling
    custom_style = """
    <style>
    table {
        border-collapse: collapse;
        width: 80%;
        font-family: Arial, sans-serif;
        text-align: left;
    }
    td {
        border: 1px solid #ccc;
        padding: 10px;
        vertical-align: top;
        text-align: left;
    }
    </style>
    """

    # Display the final HTML
    display(HTML(custom_style + html_output))


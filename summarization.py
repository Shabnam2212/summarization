import os
import fitz
import nltk
import re
import csv
import argparse
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

nltk.download('punkt_tab')

# Load model/tokenizer once
checkpoint = "sshleifer/distilbart-cnn-12-6"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)
max_input_length = tokenizer.model_max_length

def remove_references_section(text):
    ref_keywords = ["references", "bibliography", "works cited"]
    lines = text.split("\n")
    cleaned_lines = []
    for line in lines:
        if any(keyword in line.strip().lower() for keyword in ref_keywords):
            break
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines)

def extract_doi(text):
    doi_pattern = r'\b10\.\d{4,9}/[-._;()/:A-Z0-9]+'
    matches = re.findall(doi_pattern, text, flags=re.IGNORECASE)
    return matches[0] if matches else "DOI not found"

def summarize_pdf(pdf_path, max_output_length=50):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()

    doi = extract_doi(text)
    cleaned_text = remove_references_section(text)
    sentences = nltk.tokenize.sent_tokenize(cleaned_text)

    chunks = []
    length = 0
    chunk = ""
    for sentence in sentences:
        sentence_length = len(tokenizer.tokenize(sentence))
        if length + sentence_length <= max_input_length:
            chunk += sentence + " "
            length += sentence_length
        else:
            chunks.append(chunk.strip())
            chunk = sentence + " "
            length = sentence_length
    if chunk:
        chunks.append(chunk.strip())

    summaries = []
    for chunk in chunks:
        inputs = tokenizer(chunk, return_tensors="pt", truncation=True, padding=True, max_length=max_input_length)
        output = model.generate(
            **inputs,
            max_length=max_output_length,
            min_length=10,
            length_penalty=0.8,
            early_stopping=True,
            no_repeat_ngram_size=3
        )
        decoded = tokenizer.decode(output[0], skip_special_tokens=True)
        cleaned = re.sub(r'\b(?:figure|fig)\s*\d+', '', decoded)
        cleaned = re.sub(r'\[\d+(?:,\d+)*\]', '', cleaned)
        cleaned = re.sub(r'\d+(\.\d+)+', '', cleaned)
        summaries.append(cleaned.strip())

    return doi, " ".join(summaries)

def main(pdf_dir):
    pdf_paths = []
    for root, dirs, files in os.walk(pdf_dir):
        for file in files:
            if file.endswith(".pdf"):
                pdf_paths.append(os.path.join(root, file))

    print(f"Found {len(pdf_paths)} PDFs.")
    summaries_dict = {}

    for i, pdf_path in enumerate(pdf_paths, 1):
        print(f"Summarizing paper {i}/{len(pdf_paths)}: {os.path.basename(pdf_path)}")
        try:
            doi, summary = summarize_pdf(pdf_path)
            summaries_dict[pdf_path] = {"DOI": doi, "Summary": summary}
            print(f" DOI: {doi}\n Summary: {summary[:200]}...\n")
        except Exception as e:
            print(f"Error summarizing {pdf_path}: {e}")

    #  Export to CSV
    with open("summarized_papers.csv", "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Folder Name", "DOI Link", "Summary"])
        for pdf_file, content in summaries_dict.items():
            folder_name = os.path.basename(os.path.dirname(pdf_file))
            doi = content["DOI"]
            doi_link = f"https://doi.org/{doi}" if doi != "DOI not found" else doi
            summary = content["Summary"]
            writer.writerow([folder_name, doi_link, summary])

    print("\n All summaries written to summarized_papers.csv")
    
# Function to summarize papers from a directory and save results to a CSV
def summarize_papers(pdf_dir, output_csv="summarized_papers.csv"):
    main(pdf_dir)  # Calls the main function with the provided directory
    print(f"Summaries saved in {output_csv}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf_dir", type=str, required=True, help="Directory where PDF files are located")
    args = parser.parse_args()
    main(args.pdf_dir)

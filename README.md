# PDF Summarizer with DOI Detection and CSV Export

This code extracts text from research PDFs, detects DOI links, summarizes the content using a transformer-based NLP model (`distilBART`), and exports the results into a structured CSV file.

---

##  Features

- Automatically finds all PDF files in a specified directory
- Extracts full text from PDFs using PyMuPDF
- Detects DOI (Digital Object Identifier) using regex
- Cleans out references/bibliography sections
- Summarizes content using a pre-trained Hugging Face transformer model
- Exports summary and DOI links into a CSV file


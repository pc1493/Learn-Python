# 1. Import necessary libraries (PyPDF2, re, collections)
from PyPDF2 import PdfReader
import re
import collections
from pathlib import Path


# 2. Define function to extract text from PDF
#    - Open PDF file using PyPDF2
#    - Create PDF reader object
#    - Loop through each page
#    - Extract and concatenate text
#    - Return full text


def extract_text(pdf_path):

    reader = PdfReader(pdf_path)
    pages = [page.extract_text() for page in reader.pages]

    return pages


# 3. Define function to analyze text
#    - Count total words
#    - Find most common words
#    - Calculate average word length
#    - Return statistics dictionary


def analyze_text(pages):

    page_statistics = {}
    document_statistics = {}
    all_words = []
    for i, page in enumerate(pages):
        words = re.findall(r"\b[a-z]+", page.lower())
        if not words:
            page_statistics[f"page {i+1}"] = {
                "most_common": None,
                "average_word_length": 0,
            }
            continue
        all_words.extend(words)

        # Get page statistics
        frequency_page = collections.Counter(words)
        most_common = max(frequency_page.items(), key=lambda x: x[1])
        average_word_length = round(sum([len(word) for word in words]) / len(words), 2)
        page_statistics[f"page {i+1}"] = {
            "most_common": most_common,
            "average_word_length": average_word_length,
        }

    # Get document statistics
    frequency_document = collections.Counter(all_words)
    most_common_document = max(frequency_document.items(), key=lambda x: x[1])
    average_word_length_document = round(
        sum([len(word) for word in all_words]) / len(all_words), 2
    )
    document_statistics["document"] = {
        "most_common": most_common_document,
        "average_word_length": average_word_length_document,
    }

    return page_statistics, document_statistics


# 4. Define function to display statistics
#    - Take statistics dictionary
#    - Format and print various statistics


def display(page_statistics, document_statistics):

    for page, details in page_statistics.items():
        print(
            f'{page} has the common word of "{details["most_common"][0]}" appearing {details["most_common"][1]} times\nwith an average word length of {details["average_word_length"]}'
        )

    print(
        f'The document has the common word of "{document_statistics["document"]["most_common"][0]}" appearing {document_statistics["document"]["most_common"][1]} times\nwith an average word length of {document_statistics["document"]["average_word_length"]}'
    )


# 5. Main program:
#    - Ask user for PDF file path
#    - Extract text from PDF
#    - Analyze extracted text
#    - Display statistics
#    - Ask if user wants to analyze another file


def main():

    while True:
        path = Path(input("enter your file path: "))
        page, document = analyze_text(extract_text(path))
        display(page, document)
        run_again = input("run again? (y/n): ")
        if run_again == "n":
            break


if __name__ == "__main__":
    main()

#    Libraries:

# PyPDF2: For reading PDF files and extracting text

# Install with: pip install PyPDF2


# re: For text processing with regular expressions
# collections: For counting word frequencies

# Implementation Notes:

# You might need to handle PDFs that are scanned images (not directly extractable text)
# Consider adding features like finding specific keywords or phrases

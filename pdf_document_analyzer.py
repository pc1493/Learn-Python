# 1. Import necessary libraries (PyPDF2, re, collections)
# 2. Define function to extract text from PDF
#    - Open PDF file using PyPDF2
#    - Create PDF reader object
#    - Loop through each page
#    - Extract and concatenate text
#    - Return full text
# 3. Define function to analyze text
#    - Count total words
#    - Find most common words
#    - Calculate average word length
#    - Return statistics dictionary
# 4. Define function to display statistics
#    - Take statistics dictionary
#    - Format and print various statistics
# 5. Main program:
#    - Ask user for PDF file path
#    - Extract text from PDF
#    - Analyze extracted text
#    - Display statistics
#    - Ask if user wants to analyze another file

#    Libraries:

# PyPDF2: For reading PDF files and extracting text

# Install with: pip install PyPDF2


# re: For text processing with regular expressions
# collections: For counting word frequencies

# Implementation Notes:

# You might need to handle PDFs that are scanned images (not directly extractable text)
# Consider adding features like finding specific keywords or phrases

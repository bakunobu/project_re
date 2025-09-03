import requests
import pdfplumber
import tempfile
import os

def download_and_parse_pdf(url):
    try:
        # Download the PDF file
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()  # Raise error for bad status codes

        # Create a temporary file to store the downloaded PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(response.content)
            tmp_file_path = tmp_file.name

        # Open and parse the PDF
        with pdfplumber.open(tmp_file_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                full_text += page.extract_text() + "\n"

        # Clean up the temporary file
        os.unlink(tmp_file_path)

        return full_text

    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage
url = "https://gym1358sz.mskobr.ru/attach_files/zakreplennaya-za-gbou-shkola-1358.pdf"
text = download_and_parse_pdf(url)

if text:
    print("Extracted text:")
    print(text[:500])  # Print first 500 characters

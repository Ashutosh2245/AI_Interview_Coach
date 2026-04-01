import PyPDF2
import re


def extract_text(pdf_file):
    """
    Extracts and sanitizes text from PDF resumes.
    """
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text_content = ""

        for page in pdf_reader.pages:
            raw_text = page.extract_text()
            if raw_text:
                text_content += raw_text + "\n"

        # Basic Sanitization
        text_content = re.sub(r'\s+', ' ', text_content)  # Remove extra whitespace
        text_content = text_content.encode("ascii", "ignore").decode()  # Remove non-ascii

        if len(text_content.strip()) < 100:
            return "Error: Resume content is too short or unreadable."

        return text_content
    except Exception as e:
        return f"Extraction Error: {str(e)}"
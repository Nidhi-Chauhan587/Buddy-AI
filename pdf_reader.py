
from pypdf import PdfReader


def extract_text_from_pdf(pdf_file):

    try:
        reader = PdfReader(pdf_file)

        extracted_text = ""

        for page_number, page in enumerate(reader.pages, start=1):

            text = page.extract_text()

            if text:
                extracted_text += (
                    f"\n\nPage {page_number}\n{text}"
                )

        if not extracted_text.strip():
            return "No readable text found in this PDF."

        return extracted_text

    except Exception as e:
        return f"Error reading PDF: {e}"

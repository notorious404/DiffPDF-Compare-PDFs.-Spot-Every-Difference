import PyPDF2
import os
from typing import Dict, BinaryIO

class PDFProcessor:
    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> str:
        """Extract text from a PDF file on disk."""
        text = ""
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text() or ""
                text += page_text + "\n"
        return text.strip()

    @staticmethod
    def extract_text_from_filelike(file_obj: BinaryIO) -> str:
        """Extract text from an in-memory uploaded file."""
        text = ""
        reader = PyPDF2.PdfReader(file_obj)
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n"
        return text.strip()

    @staticmethod
    def process_pdfs_folder(input_folder: str = "input_pdfs") -> Dict[str, str]:
        """Process all PDFs from a folder (CLI / batch mode)."""
        pdf_contents = {}
        for filename in os.listdir(input_folder):
            if filename.lower().endswith(".pdf"):
                pdf_path = os.path.join(input_folder, filename)
                pdf_contents[filename] = PDFProcessor.extract_text_from_pdf(pdf_path)
        return pdf_contents

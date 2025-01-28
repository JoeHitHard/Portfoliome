from abc import ABC, abstractmethod
from pathlib import Path

import PyPDF2
from docx import Document


class BaseFileExtractor(ABC):
    @abstractmethod
    def extract_text(self, file_path: str) -> str:
        pass


class PDFExtractor(BaseFileExtractor):
    def extract_text(self, file_path: str) -> str:
        text = ""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        return text


class DOCXExtractor(BaseFileExtractor):
    def extract_text(self, file_path: str) -> str:
        doc = Document(file_path)
        return '\n'.join([para.text for para in doc.paragraphs])


class FileExtractorFactory:
    @staticmethod
    def get_extractor(file_path: str) -> BaseFileExtractor:
        ext = Path(file_path).suffix.lower()
        if ext == '.pdf':
            return PDFExtractor()
        elif ext == '.docx':
            return DOCXExtractor()
        raise ValueError(f"Unsupported file format: {ext}")

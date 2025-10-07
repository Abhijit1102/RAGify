import openai
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from docx import Document as DocxDocument
from src.config import Config
from typing import List, Dict
import os

class EmbeddingService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(EmbeddingService, cls).__new__(cls)
        return cls._instance

    def __init__(self, embedding_model: str = Config.OPENAI_EMBEDDING_MODEL):
        if hasattr(self, "_initialized") and self._initialized:
            return
        self.model = embedding_model
        openai.api_key = Config.OPENAI_API_KEY
        self._initialized = True

    def process_document(self, file_path: str) -> List[Dict[str, any]]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        ext = os.path.splitext(file_path)[1].lower()
        text_chunks = []

        if ext == ".pdf":
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            for i, doc in enumerate(documents):
                text_chunks.append({"text": doc.page_content, "page_number": i + 1})
        elif ext == ".docx":
            doc = DocxDocument(file_path)
            full_text = "\n".join([p.text for p in doc.paragraphs])
            text_chunks.append({"text": full_text, "page_number": 1})
        elif ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                text_chunks.append({"text": f.read(), "page_number": 1})
        else:
            raise ValueError(f"Unsupported file type: {ext}")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", " ", ""]
        )

        final_chunks = []
        for chunk in text_chunks:
            split_texts = text_splitter.split_text(chunk["text"])
            for st in split_texts:
                final_chunks.append({
                    "text": self.clean_text(st),
                    "page_number": chunk["page_number"]
                })

        return final_chunks

    def embed_text(self, texts: List[str]) -> List[List[float]]:
        embeddings = []
        for i in range(0, len(texts), 100):
            batch = texts[i:i+100]
            response = openai.embeddings.create(model=self.model, input=batch)
            embeddings.extend([d.embedding for d in response.data])
        return embeddings

    def embed_documents_with_metadata(self, file_path: str) -> List[Dict[str, any]]:
        """
        Returns embeddings with metadata:
        - vector
        - text
        - file_name
        - page_number
        """
        chunks = self.process_document(file_path)
        texts = [c["text"] for c in chunks]
        embeddings = self.embed_text(texts)
        file_name = os.path.basename(file_path)

        return [
            {
                "vector": embeddings[i],
                "payload": {
                    "text": chunks[i]["text"],
                    "file_name": file_name,
                    "page_number": chunks[i]["page_number"]
                }
            }
            for i in range(len(chunks))
        ]

    @staticmethod
    def clean_text(text: str) -> str:
        return text.replace("\n", " ").replace("\t", " ").replace('"', " ").replace("'", " ")

# Singleton instance
embedding_service = EmbeddingService()

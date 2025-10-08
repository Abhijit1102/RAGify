import os
from typing import List, Dict
import openai
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from docx import Document as DocxDocument
from src.config import Config
import asyncio
from concurrent.futures import ThreadPoolExecutor

class EmbeddingService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, embedding_model: str = Config.OPENAI_EMBEDDING_MODEL):
        if getattr(self, "_initialized", False):
            return
        self.model = embedding_model
        openai.api_key = Config.OPENAI_API_KEY
        self._executor = ThreadPoolExecutor(max_workers=4)
        self._initialized = True

    def process_document(self, file_path: str) -> List[Dict]:
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

    async def embed_text_async(self, texts: List[str]) -> List[List[float]]:
        """
        Async wrapper for embedding texts in batches using threads.
        """
        loop = asyncio.get_event_loop()
        embeddings = []

        for i in range(0, len(texts), 100):
            batch = texts[i:i+100]
            batch_embeddings = await loop.run_in_executor(self._executor, self.embed_text_sync, batch)
            embeddings.extend(batch_embeddings)
        return embeddings

    def embed_text_sync(self, texts: List[str]) -> List[List[float]]:
        """
        Synchronous batch embedding call to OpenAI
        """
        response = openai.embeddings.create(model=self.model, input=texts)
        return [d.embedding for d in response.data]

    @staticmethod
    def clean_text(text: str) -> str:
        return text.replace("\n", " ").replace("\t", " ").replace('"', " ").replace("'", " ")

# Singleton instance
embedding_service = EmbeddingService()

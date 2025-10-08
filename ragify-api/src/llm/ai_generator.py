from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List, Dict
import asyncio

class DocumentAnswer(BaseModel):
    text: str
    file_name: str = None
    page_number: int = None
    score: float = 0.0

class LLMGenerator:
    def __init__(self, model_name: str = "gpt-3.5-turbo", temperature: float = 0.0):
        self.model = ChatOpenAI(model_name=model_name, temperature=temperature)
        self.parser = JsonOutputParser(pydantic_object=DocumentAnswer)
        self.prompt_template = PromptTemplate(
            template=(
                "You are an AI assistant. Based on the following document snippets, answer the query:\n\n"
                "Query: {query}\n"
                "Document Snippets:\n{snippets}\n\n"
                "Summarize and answer concisely in JSON format following these instructions:\n"
                "{format_instructions}"
            ),
            input_variables=["query", "snippets"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )
        self.chain = self.prompt_template | self.model | self.parser

    def generate(self, context: List[Dict], query: str) -> dict:
        if not query.strip():
            return {"error": "Invalid input query", "status_code": 400}
        if not context:
            return {"text": "", "file_name": None, "page_number": None, "score": 0.0}

        snippets = "\n\n".join(
            [f"{d['text']} (File: {d['file_name']}, Page: {d['page_number']}, Score: {d['score']})" for d in context]
        )

        try:
            return self.chain.invoke({"query": query, "snippets": snippets})
        except Exception as e:
            return {"text": f"LLM generation failed: {str(e)}", "file_name": None, "page_number": None, "score": 0.0}

    async def generate_async(self, context: List[Dict], query: str) -> dict:
        return await asyncio.to_thread(self.generate, context, query)

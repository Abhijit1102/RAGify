import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from utils.api_response import api_response
from utils.error_handler import error_handler

app = FastAPI(title="RAGify API")

# Register error handlers
app.add_exception_handler(RequestValidationError, error_handler.validation_error_handler)
app.add_exception_handler(Exception, error_handler.generic_error_handler)

@app.get("/ping")
async def ping():
    return api_response.success(message="RAGify API is running 🚀")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

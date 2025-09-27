import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from src.utils.api_response import api_response
from src.utils.error_handler import error_handler
from src.config import Config

# Import routers
from src.routers import auth, health_check

app = FastAPI(title="RAGify API")

# Register error handlers
app.add_exception_handler(RequestValidationError, error_handler.validation_error_handler)
app.add_exception_handler(Exception, error_handler.generic_error_handler)

# Include routers with API version prefix
API_PREFIX = "/api/v1"

app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(health_check.router, prefix=API_PREFIX)

@app.get(f"{API_PREFIX}/ping")
async def ping():
    return api_response.success(message="RAGify API is running 🚀")

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=Config.PORT, reload=True)

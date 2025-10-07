import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from src.utils.api_response import api_response
from src.utils.error_handler import error_handler
from src.config import Config

# Import routers
from src.routers import auth_router, health_check_router, user_router, document_router, search_router, chat_router
app = FastAPI(title="RAGify API")

# --- CORS Middleware ---
origins = [
    Config.CLIENT_URL, 
]

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Error Handlers ---
app.add_exception_handler(RequestValidationError, error_handler.validation_error_handler)
app.add_exception_handler(Exception, error_handler.generic_error_handler)

# --- Routers ---
API_PREFIX = "/api/v1"
app.include_router(health_check_router.router, prefix=API_PREFIX)
app.include_router(auth_router.router, prefix=API_PREFIX)
app.include_router(user_router.router, prefix=API_PREFIX)
app.include_router(document_router.router, prefix=API_PREFIX)
app.include_router(search_router.router, prefix=API_PREFIX)
app.include_router(chat_router.router, prefix=API_PREFIX)


@app.get(f"{API_PREFIX}/ping")
async def ping():
    return api_response.success(message="RAGify API is running 🚀")

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=Config.PORT, reload=True)

from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

class ErrorHandler:
    @staticmethod
    async def validation_error_handler(request: Request, exc):
        return JSONResponse(
            status_code=422,
            content={
                "status": "error",
                "message": "Validation error",
                "details": exc.errors(),
            },
        )

    @staticmethod
    async def generic_error_handler(request: Request, exc):
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "Internal server error",
                "details": str(exc),
            },
        )

# Singleton instance
error_handler = ErrorHandler()

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

class ApiResponse:
    def success(self, data=None, message="Success", status_code=200, extra=None):
        response_content = {
            "status": "success",
            "message": message,
            "data": data
        }
        if extra:
            response_content.update(extra)
        
        # ✅ Safely convert datetime & non-JSON types
        response_content = jsonable_encoder(response_content)
        
        return JSONResponse(status_code=status_code, content=response_content)

    def error(self, message="Error occurred", status_code=400, details=None):
        response_content = {
            "status": "error",
            "message": message,
            "details": details
        }

        # ✅ Also safe for exceptions or Pydantic errors
        response_content = jsonable_encoder(response_content)

        return JSONResponse(status_code=status_code, content=response_content)

# Singleton instance
api_response = ApiResponse()

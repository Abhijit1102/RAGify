from fastapi.responses import JSONResponse

class ApiResponse:
    def success(self, data=None, message="Success", status_code=200):
        return JSONResponse(
            status_code=status_code,
            content={
                "status": "success",
                "message": message,
                "data": data
            }
        )

    def error(self, message="Error occurred", status_code=400, details=None):
        return JSONResponse(
            status_code=status_code,
            content={
                "status": "error",
                "message": message,
                "details": details
            }
        )

# Singleton instance
api_response = ApiResponse()

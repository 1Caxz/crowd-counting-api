from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import json
import traceback

class ResponseMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        try:
            response: Response = await call_next(request)
            # Bypass if already a JSONResponse with "status"
            if isinstance(response, JSONResponse):
                try:
                    body = json.loads(response.body.decode())
                    if isinstance(body, dict) and "status" in body:
                        return response
                except Exception:
                    pass

            # Parse original response
            content = await response.body()
            try:
                data = json.loads(content)
            except Exception:
                data = content.decode()

            # Wrap the response
            wrapped = {
                "status": "success",
                "message": "Request successful",
                "data": data
            }
            return JSONResponse(content=wrapped, status_code=response.status_code)

        except Exception as e:
            traceback.print_exc()
            return JSONResponse(
                status_code=500,
                content={
                    "status": "error",
                    "message": str(e),
                    "data": None
                }
            )

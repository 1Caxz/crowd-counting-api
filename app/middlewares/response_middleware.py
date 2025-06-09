from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from starlette.concurrency import iterate_in_threadpool
import json
import traceback

EXCLUDE_PATHS = ["/uploads"]

class ResponseMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # Lewati middleware jika exclude route
        if any(request.url.path.startswith(p) for p in EXCLUDE_PATHS):
            return await call_next(request)
        
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

            response_body = [chunk async for chunk in response.body_iterator]
            response.body_iterator = iterate_in_threadpool(iter(response_body))
            # Parse original response
            content = response_body[0].decode()
            try:
                data = json.loads(content)
            except Exception:
                data = content.decode()
                
            # Wrap the error response
            if 'error_message' in data:
                wrapped = {
                    "status": "error",
                    "message": data['error_message'],
                    "data": None
                }
                return JSONResponse(content=wrapped, status_code=400)
            
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

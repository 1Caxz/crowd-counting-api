from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from jwt import DecodeError, ExpiredSignatureError
from app.utils.jwt_helper import decode_access_token

PUBLIC_PATHS = ["/login", "/register", "/posts/list"]

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Lewati middleware jika public route
        if any(request.url.path.startswith(p) for p in PUBLIC_PATHS):
            return await call_next(request)

        # Ambil Authorization Header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=401, content={
                "status": "error",
                "message": "Authorization header missing or invalid",
                "data": None
            })

        token = auth_header.split(" ")[1]
        try:
            payload = decode_access_token(token)
            request.state.user_id = payload.get("user_id")
        except ExpiredSignatureError:
            return JSONResponse(status_code=401, content={
                "status": "error",
                "message": "Token expired",
                "data": None
            })
        except DecodeError:
            return JSONResponse(status_code=401, content={
                "status": "error",
                "message": "Invalid token",
                "data": None
            })
        return await call_next(request)

from fastapi import FastAPI
from app.routers import post_router, user_router
from app.core.database import Base, engine
from app.middlewares.response_middleware import ResponseMiddleware
from app.middlewares.auth_middleware import AuthMiddleware
from app.exceptions import handlers
from fastapi.exceptions import RequestValidationError, HTTPException

app = FastAPI(title="Crowd Counting API")

# Register Middlewares
app.add_middleware(AuthMiddleware)
app.add_middleware(ResponseMiddleware)

# Error handlers
app.add_exception_handler(HTTPException, handlers.custom_http_exception_handler)
app.add_exception_handler(RequestValidationError, handlers.validation_exception_handler)
app.add_exception_handler(Exception, handlers.general_exception_handler)

# DB Init
Base.metadata.create_all(bind=engine)

# Register Routers
app.include_router(post_router.router)
app.include_router(user_router.router)
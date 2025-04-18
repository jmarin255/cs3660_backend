from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from services.login_service import LoginService

app = FastAPI()

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        PUBLIC_PATHS = {"/api/login", "/health", "/openapi.json"}
        path = request.url.path

        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split("Bearer ")[1]
            try:
                LoginService.verify_token(token)
            except Exception as e:
                return JSONResponse(status_code=401, content={"detail": str(e)})
        elif path not in PUBLIC_PATHS:
            # If it's not a public path, and token is missing or malformed
            return JSONResponse(status_code=401, content={"detail": "missing authorization token"})

        return await call_next(request)
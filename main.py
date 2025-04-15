from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from fastapi.middleware.cors import CORSMiddleware

from controllers import login_controller
from config import settings

from middleware.api_gateway_middleware import ApiGatewayAuthMiddleware
from middleware.auth_middleware import AuthMiddleware
from schemas.message_schema import MessageResponse


app = FastAPI(title="CS3660 Backend Project", version="1.0.0")

app.add_middleware(AuthMiddleware)

if settings.app_env == "local":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allow_origins,  
        allow_credentials=True,
        allow_methods=["*"],  
        allow_headers=["*"],  
    )

if settings.app_env == "prod":
    app.add_middleware(ApiGatewayAuthMiddleware)  





app.include_router(login_controller.router)

@app.get("/", response_model=MessageResponse)
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/health", response_model=MessageResponse)
def health():
    return {"message": "Ok"}



from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.api.commons.middlewares.validate_jwt import validate_jwt

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        authorization: str = request.headers.get("Authorization")
        path_whitelist = [
            "/docs",      # Swagger UI
            "/openapi.json",  # Swagger JSON
            "/",          # Homepage (optional)
            "/favicon.ico"  # Favicon (optional, some browsers request this automatically)
        ]

        if request.url.path in path_whitelist:
            return await call_next(request)
        if not authorization:
            return JSONResponse(status_code=401, content={"message": "Authorization header missing"})

        token = authorization.split(" ")[1]
        user = validate_jwt(token)
        if not user:
            return JSONResponse(status_code=401, content={"message": "Unauthroized Invalid Token"})


        response = await call_next(request)
        return response

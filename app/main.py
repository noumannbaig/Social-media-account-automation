from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.config import api_prefix
from app.api.commons.middlewares.error_handler.middleware import add_exception_handlers
from app.api.avatar_groups.views import router as avatar_group_router


api_router = APIRouter(
    prefix=api_prefix,
)
api_router.include_router(avatar_group_router, prefix="/avatar-groups", tags=["Avatar Management"])


app = FastAPI(title="Avatar Management")

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api_router.get("/test")
async def Test():
    return {"message": "Server Running Properly"}


app.include_router(api_router)

add_exception_handlers(app)

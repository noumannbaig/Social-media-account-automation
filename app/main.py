from pytz import utc
import json
import random
from fastapi import Depends, FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler

from app.api.commons.sms_provider import (
    find_country_by_name,
    get_activation,
    get_countries,
    get_phone_number,
    get_sms_activation,
)
from app.api.jobs.service import run_avatar_generation_scheduler
from app.config import api_prefix
from app.api.commons.middlewares.error_handler.middleware import add_exception_handlers
from app.api.avatar_groups.views import router as avatar_group_router
from app.api.avatar_creation.views import router as avatar_creation_router
from app.api.look_up_tables.views import router as look_ups
from app.api.jobs.views import router as jobs


api_router = APIRouter(
    prefix=api_prefix,
)
api_router.include_router(
    avatar_group_router, prefix="/avatar-groups", tags=["Avatar Groups"]
)
api_router.include_router(
    avatar_creation_router, prefix="/avatar-creation", tags=["Avatar Creation"]
)
api_router.include_router(
    look_ups, prefix="/look-ups", tags=["Look ups"]
)
api_router.include_router(
    jobs, prefix="/jobs", tags=["Jobs"]
)


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

@app.on_event("startup")
def start_scheduler():
    scheduler = BackgroundScheduler(timezone=utc)
    scheduler.add_job(run_avatar_generation_scheduler, 'interval', hours=1)
    scheduler.start()
    print("Scheduler started...")
app.include_router(api_router)

add_exception_handlers(app)

from typing import List
from aiogram import Router
from .default_handlers import router as default_router
from .add_video_handlers import router as add_video_router
from .get_video_handler import router as get_video_router


def get_handlers_routers() -> Router:
    main_loader = Router()
    routers: List[Router] = [default_router, add_video_router, get_video_router]
    main_loader.include_routers(*routers)
    return main_loader

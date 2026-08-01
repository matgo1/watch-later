import aiohttp
from tg_bot.config import BACKEND_URL
from typing import Dict


class ApiError(Exception):
    """Error handling of API"""

    def __init__(self, status: int, message: str = ""):
        self.status = status
        self.message = message
        super().__init__(f"API error {status}: {message}")


async def add_video(link: str, title: str, description: str | None = None) -> None:
    payload: Dict = {"title": title, "link": link, "description": description}
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{BACKEND_URL}/add", json=payload) as resp:
            if resp.status == 201:
                return
            if resp.status == 400:
                raise ApiError(400, "Invalid link or empty title")
            raise ApiError(resp.status, "Backend error")


async def get_random_video() -> Dict:
    """Returns a video struct"""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BACKEND_URL}/random") as resp:
            if resp.status == 200:
                return await resp.json()
            raise ApiError(resp.status, "Backend error")


async def remove_video(link: str) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{BACKEND_URL}/remove", json=link) as resp:
            if resp.status == 204:
                return
            if resp.status == 400:
                raise ApiError(400, "Failed to delete from data")
            raise ApiError(resp.status, "Backend error")

from typing import Dict
from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tg_bot.utils.states import DefaultStates
from tg_bot.client import get_random_video, ApiError

router = Router()


@router.message(Command("get_ran"), StateFilter(DefaultStates.active))
async def cmd_get(message: Message, state: FSMContext):
    try:
        video: Dict[str, str] = await get_random_video()
        await message.answer(f"{video.get('title')}")
        await message.answer(f"{video.get('link')}")
    except ApiError as e:
        await message.answer(f"Couldn't save video ({e.status}).")
    finally:
        await state.set_state(DefaultStates.active)

from typing import Dict
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from tg_bot.utils.states import DefaultStates, RemoveVideoStates
from tg_bot.utils.keyboards import choose_action_kb
from tg_bot.client import get_random_video, remove_video, ApiError

router = Router()


@router.message(Command("get_ran"), StateFilter(DefaultStates.active))
async def cmd_get(message: Message, state: FSMContext):
    """
    We get random video, print it and give use choice:
    1. Choose this vide;
    2. Skip and show another
    """
    try:
        video: Dict[str, str] = await get_random_video()
        await message.answer(
            f"{video.get('title')}\n{video.get('link')}",
            reply_markup=choose_action_kb(),
        )
    except ApiError as e:
        await message.answer(f"Couldn't save video ({e.status}).")
    finally:
        await state.set_state(RemoveVideoStates.waiting_for_resp)
        await state.update_data(link=video.get("link"))


@router.callback_query(
    F.data == "next_video", StateFilter(RemoveVideoStates.waiting_for_resp)
)
async def change_video(callback: CallbackQuery, state: FSMContext):
    """
    If user chose to watch another video,
    show him another video
    """
    await callback.answer()
    try:
        video: Dict[str, str] = await get_random_video()
        await callback.message.edit_text(
            f"{video.get('title')}\n{video.get('link')}",
            reply_markup=choose_action_kb(),
        )
    except ApiError as e:
        await callback.answer(f"Couldn't save vide ({e.status}).")
    finally:
        await state.update_data(link=video.get("link"))


@router.callback_query(
    F.data == "remove_video", StateFilter(RemoveVideoStates.waiting_for_resp)
)
async def remove_chosen_video(callback: CallbackQuery, state: FSMContext):
    """
    If user chose to watch the video,
    delete the video from file.
    """
    await callback.answer()
    data = await state.get_data()
    link = data.get("link") or ""

    await remove_video(link)

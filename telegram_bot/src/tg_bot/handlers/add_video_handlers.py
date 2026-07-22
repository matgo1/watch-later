from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tg_bot.utils.states import AddVideoStates, DefaultStates
from tg_bot.client import add_video, ApiError

router = Router()


@router.message(Command("add"), StateFilter(DefaultStates.active))
async def cmd_add(message: Message, state: FSMContext):
    await state.set_state(AddVideoStates.waiting_for_link)
    await message.answer("Send link")


@router.message(StateFilter(AddVideoStates.waiting_for_link))
async def process_link(message: Message, state: FSMContext):
    link = message.text.strip()
    if not (link.startswith("http://") or link.startswith("https://")):
        await message.answer("Wrong link")
        return

    await state.update_data(link=link)
    await state.set_state(AddVideoStates.waiting_for_title)
    await message.answer("Got it. Now send me a title.")


@router.message(StateFilter(AddVideoStates.waiting_for_title))
async def process_title(message: Message, state: FSMContext):
    title = message.text.strip()
    if not title:
        await message.answer("Title can't be empty be empty. Try again")
        return

    data = await state.get_data()
    link = data["link"]

    try:
        await add_video(link, title)
        await message.answer(f"Saved: {title}")
    except ApiError as e:
        await message.answer(f"Couldn't save video ({e.status}).")
    finally:
        await state.clear()

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from tg_bot.utils.states import DefaultStates

# Construct router
router = Router()


@router.message(Command("start"), StateFilter(None))
async def cmd_start_nonactive(message: Message, state: FSMContext):
    # Start from not active
    await state.set_state(DefaultStates.active)
    await message.answer("Successfully launched")


@router.message(Command("start"), StateFilter(DefaultStates.active))
async def cmd_start_active(message: Message):
    # Start if already started
    await message.answer("✅ Already started")


@router.message(Command("stop"), ~StateFilter(None))
async def cmd_stop(message: Message, state: FSMContext):
    # Stop command
    await state.set_state(None)
    await message.answer("🤖 Bot stopped")

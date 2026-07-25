from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def choose_action_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text="Choose this video", callback_data="remove_video"),
        InlineKeyboardButton(text="Next", callback_data="next_video"),
        width=1,
    )

    return builder.as_markup()

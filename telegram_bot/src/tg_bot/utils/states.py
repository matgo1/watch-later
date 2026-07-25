from aiogram.fsm.state import StatesGroup, State


class DefaultStates(StatesGroup):
    active = State()


class AddVideoStates(StatesGroup):
    waiting_for_link = State()
    waiting_for_title = State()


class RemoveVideoStates(StatesGroup):
    waiting_for_resp = State()

from aiogram.fsm.state import State, StatesGroup


class PhotoTextStates(StatesGroup):
    waiting_for_photo = State()


class AskImageStates(StatesGroup):
    waiting_for_photo = State()
    waiting_for_question = State()


class TextToPhotoStates(StatesGroup):
    waiting_for_prompt = State()

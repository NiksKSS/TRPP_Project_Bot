from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.core.session_manager import session_manager

router = Router()


@router.message(Command("cancel"))
async def cmd_cancel(message: types.Message, state: FSMContext):
    """Отмена любой активной операции."""
    user_id = message.from_user.id
    current_state = await state.get_state()
    if not current_state:
        await message.answer("✅ Нет активных операций.\n\n")
        return
    session_manager.cleanup(user_id)
    await state.clear()
    await message.answer("❌ Операция отменена\n" "Напиши /help для списка команд.")

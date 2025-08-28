from aiogram import Router, types
from aiogram.filters import Command
#kb_import
from Keyboards.to_menu_kb import to_menu_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

from aiogram import F

#user states
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from States.user_states import FSM

router = Router()

@router.callback_query(F.data == "achievements", FSM.Depalka)
async def show_info(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
                        f"Тут ничего нет, возвращайся позже",
                        reply_markup=to_menu_kb)

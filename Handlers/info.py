from aiogram import Router, types
from aiogram.filters import Command
#kb_import
from Keyboards.info_kb import info_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
#user states
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from States.user_states import FSM

from database.bd_handler import eballs_balance

router = Router()

@router.message(Command("info"), FSM.Depalka)
async def show_info(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(f"Никнейм: {data['username']}\n"
                         f"Е-баллы: {eballs_balance(data['username'])}",
                         reply_markup=info_kb)

async def get_data(state: FSMContext, key: str):
    data = await state.get_data()
    return str(data.get(key))

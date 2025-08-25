from aiogram import Router, types
from aiogram.filters import Command
#kb_import
from Keyboards.to_menu_kb import to_menu_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
#user states
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from States.user_states import FSM

from database.bd_handler import eballs_balance

router = Router()

@router.message(Command('pravda'), FSM.Depalka)
async def upload_photo(message: types.Message):
    photo = FSInputFile("pravda.jpg")
    await message.answer_photo(
            photo,
            caption="что вас ждёт",
    )
    await message.answer("Ня (костыль небольшой, забейте)", reply_markup=to_menu_kb)
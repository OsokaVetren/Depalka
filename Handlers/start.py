from aiogram import Router, types
from aiogram.filters import Command
#kb_import
from Keyboards.auth_kb import auth_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
#user states
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from States.user_states import FSM

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Привет, брательник! На всякий случай - ты вошёл в додепалку, тг-бот для розыгрыша е-баллов. Есть два стула", reply_markup=auth_kb)
    await state.set_state(FSM.RegLogState)

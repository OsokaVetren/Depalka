from aiogram import Router, types
from aiogram.filters import Command

from Keyboards.to_menu_kb import to_menu_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

from database.bd_handler import get_top_players

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from States.user_states import FSM

router = Router()

@router.message(Command("top"), FSM.Depalka)
async def show_top(message: types.Message, state: FSMContext):
    top_players = get_top_players(10)
    
    top_text = f"📊 Топ самых богатеньких депальщиков:\n\n"
    
    for i, player in enumerate(top_players, 1):
        top_text += f"{i}. {player['username']} - {player['eballs']} хатсуне мику\n"
    
    await message.answer(top_text, reply_markup=to_menu_kb)


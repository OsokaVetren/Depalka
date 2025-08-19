from aiogram import Router, types
from aiogram.filters import Command

from Keyboards.get_games_kb import get_games_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

from aiogram import F

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from States.user_states import FSM

router = Router()

@router.callback_query(FSM.Depalka, F.data == "games")
async def choose_game(callback: types.CallbackQuery):
    await callback.message.edit_text("Выбери игру", reply_markup=get_games_kb)

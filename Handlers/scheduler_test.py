from aiogram import Router, types
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# kb_import
from Keyboards.info_kb import info_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

from aiogram import F

# user states
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from States.user_states import FSM

from database.bd_handler import eballs_balance, eballs_change
from apscheduler.schedulers.asyncio import AsyncIOScheduler

router = Router()
scheduler = AsyncIOScheduler()


async def death_in_poverty(state: FSMContext):
    data = await state.get_data()
    username = data["username"]
    if eballs_balance(data["username"]) < 10:
        eballs_change(username, +10)
        print('вова лох')


def schedule_job():
    scheduler.add_job(death_in_poverty, "interval", minutes=1)


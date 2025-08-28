from aiogram import Router, types
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# kb_import
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

from aiogram import F

# user states
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from States.user_states import FSM

from database.bd_handler import eballs_balance, eballs_change, dodep_update_all
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()


def schedule_job():
    scheduler.add_job(dodep_update_all, "interval", days=1)
def scheduler_start():
    scheduler.start()
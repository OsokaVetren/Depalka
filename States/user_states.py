from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage

class FSM(StatesGroup):
    RegLogState = State()
    Login = State()
    Password = State()
    Depalka = State()
    User_Data_Change = State()
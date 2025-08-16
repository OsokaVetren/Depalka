#user states
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from States.user_states import FSM

from aiogram import F

from aiogram import Router, types
from aiogram.filters import Command
#db_handler
from database.bd_handler import is_user_valid, new_user

router = Router()

@router.callback_query(FSM.RegLogState, F.data == "register")
async def process_register(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(type = "register")
    await callback.message.answer("Введи логин:")
    await state.set_state(FSM.Login)

@router.callback_query(FSM.RegLogState, F.data == "login")
async def process_login(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(type = "login")
    await callback.message.answer("Введи логин:")
    await state.set_state(FSM.Login)

@router.message(FSM.Login)
async def login_getter(message: types.Message, state: FSMContext):
    await state.update_data(username = message.text)
    await message.answer("Введи пароль:")
    await state.set_state(FSM.Password)
 
@router.message(FSM.Password)
async def password_getter(message: types.Message, state: FSMContext):
    await state.update_data(password = message.text)
    username = await get_data(state, "username")
    password = await get_data(state, "password")
    type = await get_data(state, "type")
    await message.answer("Ваш логин и пароль: " + username + " " + password)
    user_id = message.from_user.id
    if type == "login":
        if is_user_valid(username, password):
            await message.answer("Вы успешно вошли! Вновь приветствуем Вас в депалке! Напишите /info, чтобы открыть меню")
            await state.set_state(FSM.Depalka)
        else:
            await message.answer("Ебать ты лох, данные не верны)")
            await state.set_state(FSM.RegLogState)
    if type == "register":
        if new_user(user_id, username, password):
            await message.answer("Вы успешно зарегестрировались! Добро пожаловать в Депалку! Напишите /info, чтобы открыть меню")
            await state.set_state(FSM.Depalka)
        else:
            await message.answer("Ебать ты лох, никнейм занят)")
            await state.set_state(FSM.RegLogState)

async def get_data(state: FSMContext, key: str):
    data = await state.get_data()
    return str(data.get(key))
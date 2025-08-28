from aiogram import Router, types
from aiogram.filters import Command
#kb_import
from Keyboards.profile_kb import profile_kb
from Keyboards.yes_no_kb import yes_no_kb
from Keyboards.to_menu_kb import to_menu_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

from aiogram import F

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage

#user states
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from States.user_states import FSM

from database.bd_handler import eballs_balance, stats_advanced, eballs_change, update_user

router = Router()

@router.callback_query(F.data == "profile", FSM.Depalka)
async def show_info(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    spins_count, dep_amount = stats_advanced(data['username'])
    await callback.message.edit_text(f"Никнейм: {data['username']}\n"
                         f"Е-баллы: {eballs_balance(data['username'])}\n"
                         f"Количество круток: " + str(spins_count) + "\n"
                         f"Суммарно депнуто: " + str(dep_amount) + " хатсуне мику" + "\n",
                         reply_markup=profile_kb)
    
@router.callback_query(F.data == "new_login", FSM.Depalka)
async def login_change(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(profile_change = "login")
    await callback.message.edit_text(f"Стоимость услуги - 10 е-баллов, вы хотите продолжить?",
                         reply_markup=yes_no_kb)

@router.callback_query(F.data == "new_password", FSM.Depalka)
async def password_change(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(profile_change = "password")
    await callback.message.edit_text(f"Стоимость услуги - 10 е-баллов, вы хотите продолжить?",
                         reply_markup=yes_no_kb)

@router.callback_query(F.data == "yes", FSM.Depalka)
async def value_getter(callback: types.CallbackQuery, state: FSMContext):
    change_type = await get_data(state, "profile_change")
    eballs = eballs_balance(await get_data(state, "username"))
    if eballs < 10:
        await callback.message.edit_text(f"У тебя баллов мало, нищета",
                         reply_markup=to_menu_kb)
    else:
        eballs_change(await get_data(state, "username"), -10)
        if change_type == "login":
            await callback.message.edit_text(f"Введите новый логин:")
        else:
            await callback.message.edit_text(f"Введите новый пароль")
        await state.set_state(FSM.User_Data_Change)

@router.message(FSM.User_Data_Change)
async def user_data_change(message: types.Message, state: FSMContext):
    value = message.text
    change_type = await get_data(state, "profile_change")
    username = await get_data(state, "username")
    password = await get_data(state, "password")
    user_id = message.from_user.id
    if change_type == "login":
        if not update_user(username, value, password):
            await message.answer(f"Что-то пошло не так. Приносим свои изменения. Е-баллы не вернём", reply_markup = to_menu_kb)
            await state.set_state(FSM.Depalka)
            return
        await state.update_data(username = value)
    else:
        if not update_user(username, username, value):
            await message.answer(f"Что-то пошло не так. Приносим свои изменения. Е-баллы не вернём", reply_markup = to_menu_kb)
            await state.set_state(FSM.Depalka)
            return
        await state.update_data(password = value)
    if change_type == "login":
        await message.answer(f"Ваше что-то там было изменено! \n"
                                "Новое погоняло - " + value + "\n"
                                "Старый пароль - " + password + "\n"
                                , reply_markup = to_menu_kb)
        await state.set_state(FSM.Depalka)
    if change_type == "password":
        await message.answer(f"Ваше что-то там было изменено! \n"
                                "Старая кликуха - " + username + "\n"
                                "Новый код безопасности - " + value + "\n"
                                , reply_markup = to_menu_kb)
        await state.set_state(FSM.Depalka)

async def get_data(state: FSMContext, key: str):
    data = await state.get_data()
    return str(data.get(key))

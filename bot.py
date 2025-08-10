#импорт разных библиотек нахуй
import asyncio
import logging
from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from Config.config_reader import config
from bd_handler import is_user_valid
from bd_handler import new_user

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=config.bot_token.get_secret_value())
# Диспетчер
dp = Dispatcher()

class FSM(StatesGroup):
    RegLogState = State()
    Login = State()
    Password = State()
    Depalka = State()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Привет, брательник! На всякий случай - ты вошёл в додепалку, тг-бот для розыгрыша е-баллов. Есть два стула", reply_markup=get_start_keyboard())
    await state.set_state(FSM.RegLogState)

#need to implement login/logout interface

def get_start_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Регистрация", callback_data="register"),
            InlineKeyboardButton(text="Вход", callback_data="login")
        ]
    ])
    return keyboard

@dp.callback_query(FSM.RegLogState, F.data == "register")
async def process_register(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(type = "register")
    await callback.message.answer("Введи логин:")
    await state.set_state(FSM.Login)

@dp.callback_query(FSM.RegLogState, F.data == "login")
async def process_register(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(type = "login")
    await callback.message.answer("Введи логин:")
    await state.set_state(FSM.Login)

@dp.message(FSM.Login)
async def Login_getter(message: types.Message, state: FSMContext):
    await state.update_data(username = message.text)
    await message.answer("Введи пароль:")
    await state.set_state(FSM.Password)

@dp.message(FSM.Password)
async def Password_getter(message: types.Message, state: FSMContext):
    await state.update_data(password = message.text)
    username = await get_data(state, "username")
    password = await get_data(state, "password")
    type = await get_data(state, "type")
    await message.answer("Ваш логин и пароль: " + username + " " + password)
    user_id = message.from_user.id
    if type == "login":
        if is_user_valid(username, password):
            await message.answer("Вы успешно вошли! Вновь приветствуем Вас в депалке!")
            await state.set_state(FSM.Depalka)
        else:
            await message.answer("Ебать ты лох, данные не верны)")
            await state.set_state(FSM.RegLogState)
    if type == "register":
        if new_user(user_id, username, password):
            await message.answer("Вы успешно зарегестрировались! Добро пожаловать в Депалку!")
            await state.set_state(FSM.Depalka)
        else:
            await message.answer("Ебать ты лох, никнейм занят)")
            await state.set_state(FSM.RegLogState)

async def get_data(state: FSMContext, key: str):
    data = await state.get_data()
    return str(data.get(key))

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
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
from bd_handler import is_user_valid, new_user, eballs_balance

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
async def process_login(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(type = "login")
    await callback.message.answer("Введи логин:")
    await state.set_state(FSM.Login)

@dp.message(FSM.Login)
async def login_getter(message: types.Message, state: FSMContext):
    await state.update_data(username = message.text)
    await message.answer("Введи пароль:")
    await state.set_state(FSM.Password)

@dp.message(FSM.Password)
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

# Хэндлер на команду /info
@dp.message(Command("info"), FSM.Depalka)
async def show_info(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(f"Никнейм: {data["username"]}\n"
                         f"Е-баллы: {eballs_balance(data["username"])}",
                         reply_markup=get_info_keyboard())
    
def get_info_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Игры", callback_data="games"),
            InlineKeyboardButton(text="Помощь", callback_data="help"),
        ], [
            InlineKeyboardButton(text="Выход из аккаунта", callback_data="logout"),
        ]
    ])
    return keyboard

@dp.callback_query(FSM.Depalka, F.data == "logout")
async def logout(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Вы вышли из аккаунта. Чтобы войти снова, напишите /start")
    await state.set_state(FSM.RegLogState)

@dp.callback_query(FSM.Depalka, F.data == "help")
async def get_help(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("В депалке есть множество способов поднять е-баллов и стать самым крутым в садике😎\n\n"
                                  "🪙 Монетка - выбираешь сторону и бросаешь монетку. "
                                  "Если выбранная сторона окажется верной, ставочка приумножится x2, а если неверной, то гуляй вася жуй опилки\n"
                                  "💰 Рулетка - нуээ там крч колесо крутится и ставить можно по-разному, сами разберётесь крч\n"
                                  "💣 Сапёр - есть сетка из плиток, в каждой из них либо приз, либо мина. После каждой плитки можно либо вывести приз, либо продолжить гэмблить. "
                                  "Наступил на мину - поздравляю, ты лох)",
                                  reply_markup=get_help_keyboard())
    
def get_help_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="В меню", callback_data="info")
        ]
    ])
    return keyboard

@dp.callback_query(FSM.Depalka, F.data == "games")
async def choose_game(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Выбери игру", reply_markup=get_games_keyboard())

def get_games_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Монетка", callback_data="money_flip"),
            InlineKeyboardButton(text="Рулетка", callback_data="roulette"),
        ], [
            InlineKeyboardButton(text="Сапёр", callback_data="dig"),
            InlineKeyboardButton(text="В меню", callback_data="info"),
        ]
    ])
    return keyboard

@dp.callback_query(FSM.Depalka, F.data == "info")
async def back_to_info(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.answer(f"Никнейм: {data["username"]}\n"
                         f"Е-баллы: {eballs_balance(data["username"])}",
                         reply_markup=get_info_keyboard())

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
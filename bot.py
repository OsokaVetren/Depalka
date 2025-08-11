#импорт разных библиотек нахуй
import asyncio
import logging
import random
from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from Config.config_reader import config
from bd_handler import is_user_valid, new_user, eballs_balance, eballs_change


# кто откатит коммит тот гей

#⠀⠀⠀⠀⠀⠀⠀⢀⣤⣴⣶⣶⣶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⢀⣴⣿⠟⠛⠛⠛⠛⠛⢿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⢀⣾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠙⢷⡄⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⣾⣁⣤⣴⣶⣤⣀⢀⣴⣶⣶⣦⣸⣷⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⢀⣿⠿⣿⣿⣿⣿⠟⠛⢿⣿⣿⣿⠛⣿⢦⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⣏⡏⠀⠙⠛⠋⣡⣴⣦⣼⡍⠉⠁⠀⢸⢺⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠻⣽⠀⠀⠀⠀⠀⠉⣈⡉⠁⠀⠀⠀⣸⠊⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⢣⠀⠀⠀⠀⠀⠛⠋⠀⠀⠀⢠⠃⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⢀⣤⣶⣷⣤⣤⣀⣀⠀⠤⠤⣤⣶⣿⣿⣶⣦⡄⠀⠀⠀⠀
#⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⢄⣾⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀
#⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⠋⠉⡚⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀
#⠀⠀⠀⠀⠻⢿⣿⣿⣿⣿⣧⣧⣿⣷⣿⣿⣿⣿⡿⢿⣿⠿⠀⠀⠀
#⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀
#⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣀⠀⠀⠀⠀
#⠀⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀
#⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀
#⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣇
#⢸⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⡇
#⠀⢿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⠃
#⠀⠘⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀
#⠀⠀⢻⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⢺⣿⡻⣿⡿⠟⠋⠀⠀⠀⠀
#⠀⠀⠨⠿⣿⠛⢻⡅⠀⠀⠀⠀⠀⠀⠀⠙⣧⣷⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⡜⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠈⠋⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⢸⠿⡋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

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
    await message.answer(f"Никнейм: {data['username']}\n"
                         f"Е-баллы: {eballs_balance(data['username'])}",
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
    await callback.message.edit_text("Вы вышли из аккаунта. Чтобы войти снова, напишите /start")
    await state.set_state(FSM.RegLogState)

@dp.callback_query(FSM.Depalka, F.data == "help")
async def get_help(callback: types.CallbackQuery):
    await callback.message.edit_text("В депалке есть множество способов поднять е-баллов и стать самым крутым в садике😎\n\n"
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

@dp.callback_query(FSM.Depalka, F.data == "info")
async def back_to_info(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.edit_text(f"Никнейм: {data['username']}\n"
                                  f"Е-баллы: {eballs_balance(data['username'])}",
                                  reply_markup=get_info_keyboard())

@dp.callback_query(FSM.Depalka, F.data == "games")
async def choose_game(callback: types.CallbackQuery):
    await callback.message.edit_text("Выбери игру", reply_markup=get_games_keyboard())

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

@dp.callback_query(FSM.Depalka, F.data == "dig")
async def start_dig_game(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(DigFSM.Bet)
    await callback.message.edit_text("💰 Введи сумму ставки (>= 5):")

class DigFSM(StatesGroup):
    Bet = State()
    Playing = State()

@dp.message(DigFSM.Bet)
async def set_bet(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        bet = int(message.text)
        if bet < 5:
            raise ValueError
        if eballs_balance(data["username"]) < bet:
            await message.answer("Ебать ты лох, деняк не хватает)")
            return
    except ValueError:
        await message.answer("Введи число >= 5, мамкин тестер")
        return
    
    eballs_change(data["username"], -bet)
    field = generate_field()
    await state.update_data(
        bet=bet,
        field=field,
        opened=[],
        profit=0
    )
    await state.set_state(DigFSM.Playing)
    await message.answer(
        f"Ставка принята: {bet} е-баллов\n"
        "Выбирай клетку:",
        reply_markup=get_field_keyboard([])
    )

SIZE = 5
MINES_COUNT = 5

def generate_field(size=SIZE, mines_count=MINES_COUNT):
    field = [[0] * size for i in range(size)]
    mines = set()
    while len(mines) < mines_count:
        r = random.randint(0, size - 1)
        c = random.randint(0, size - 1)
        mines.add((r, c))
    for r, c in mines:
        field[r][c] = 1
    return field

def get_field_keyboard(opened, size=SIZE):
    keyboard = []
    for r in range(size):
        row = []
        for c in range(size):
            if (r, c) in opened:
                row.append(InlineKeyboardButton(text="✅", callback_data="norm"))
            else:
                row.append(InlineKeyboardButton(text="⬜", callback_data=f"dig_{r}_{c}"))
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton(text="💰 Забрать", callback_data="cashout")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

@dp.callback_query(DigFSM.Playing, F.data.startswith("dig_"))
async def dig_cell(callback: types.CallbackQuery, state: FSMContext):
    r, c = map(int, callback.data.split("_")[1:])
    data = await state.get_data()
    field = data["field"]
    opened = data["opened"]
    profit = data["profit"]
    bet = data["bet"]

    if field[r][c] == 1:
        await state.update_data(profit=0)
        await callback.message.edit_text(
            f"💥 Бум! Ты просрал {bet} е-баллов!"
        )
        await state.set_state(FSM.Depalka)
    else:
        opened.append((r, c))
        profit += int(round(bet * 0.2))
        await state.update_data(opened=opened, profit=profit)
        await callback.message.edit_text(
            f"Текущий выигрыш: {profit} е-баллов",
            reply_markup=get_field_keyboard(opened)
        )

@dp.callback_query(DigFSM.Playing, F.data == "cashout")
async def cashout(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    profit = data["profit"]
    bet = data["bet"]
    eballs_change(data["username"], profit)
    await callback.message.edit_text(
        f"Ты забрал {profit} е-баллов со ставки {bet}"
    )
    await state.set_state(FSM.Depalka)

@dp.message(Command('pravda'), FSM.Depalka)
async def upload_photo(message: types.Message):
    # Сюда будем помещать file_id отправленных файлов, чтобы потом ими воспользоваться
    file_ids = []
    photo = FSInputFile("pravda.jpg")
    await message.answer_photo(
            photo,
            caption="что вас ждёт"
    )

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

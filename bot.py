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
from bd_handler import is_user_valid, new_user, eballs_balance, eballs_change, log_game, get_user_stats


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
                                  "💰 Рулетка - там крч колесо крутится и ставить можно по-разному, сами разберётесь крч\n"
                                  "💣 Сапёр - есть сетка из плиток, в каждой из них либо приз, либо мина. После каждой плитки можно либо вывести приз, либо продолжить гэмблить. "
                                  "Наступил на мину - поздравляю, ты лох)\n"
                                  "🃏 Блекджек - тихий и стандартный, цель - набрать больше очков, чем дилер, но не более 21. "
                                  "Присутствует смелая возможность удвоить ставочку на первом ходу, но и шанс оподливиться станет выше\n\n"
                                  "P.S.: напиши /stats, чтобы посмотреть статку последних 5 игр, или /pravda, чтобы узнать секрет🤫",
                                  reply_markup=get_help_keyboard())
    
def get_help_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="В меню", callback_data="info")
        ]
    ])
    return keyboard

@dp.callback_query(F.data == "info")
async def back_to_info(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.set_state(FSM.Depalka)
    await callback.message.edit_text(f"Никнейм: {data['username']}\n"
                                  f"Е-баллы: {eballs_balance(data['username'])}",
                                  reply_markup=get_info_keyboard())

@dp.callback_query(FSM.Depalka, F.data == "games")
async def choose_game(callback: types.CallbackQuery):
    await callback.message.edit_text("Выбери игру", reply_markup=get_games_keyboard())

def get_games_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Монетка", callback_data="coinflip"),
            InlineKeyboardButton(text="Рулетка", callback_data="roulette"),
        ], [
            InlineKeyboardButton(text="Сапёр", callback_data="dig"),
            InlineKeyboardButton(text="Блекджек", callback_data="blackjack"),
        ], [
            InlineKeyboardButton(text="В меню", callback_data="info"),
        ]
    ])
    return keyboard


# -------------------- Сапёр --------------------
@dp.callback_query(FSM.Depalka, F.data == "dig")
async def start_dig_game(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(DigFSM.Bet)
    await callback.message.edit_text("💰 Введи сумму ставки (>= 5):")

class DigFSM(StatesGroup):
    Bet = State()
    Playing = State()

@dp.message(DigFSM.Bet)
async def set_dig_bet(message: types.Message, state: FSMContext):
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
    username = data["username"]

    if field[r][c] == 1:
        await state.update_data(profit=0)
        details = {
            "opened_cells": len(opened),
            "hit_mine_at": f"{r},{c}"
        }
        log_game(username, "dig", bet, "lose", 0, details)
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
    username = data["username"]
    opened = data["opened"]

    eballs_change(data["username"], profit)
    details = {
        "opened_cells": len(opened),
        "cashout_profit": profit
    }
    log_game(username, "dig", bet, "win", profit, details)
    await callback.message.edit_text(
        f"Ты забрал {profit} е-баллов со ставки {bet}"
    )
    await state.set_state(FSM.Depalka)


# -------------------- Монетка --------------------
@dp.callback_query(FSM.Depalka, F.data == "coinflip")
async def start_coin_game(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(CoinFSM.Bet)
    await callback.message.edit_text("💰 Введи сумму ставки (>= 5):")

class CoinFSM(StatesGroup):
    Bet = State()
    Playing = State()

@dp.message(CoinFSM.Bet)
async def set_coin_bet(message: types.Message, state: FSMContext):
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

    await state.update_data(bet=bet)
    await state.set_state(CoinFSM.Playing)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Орел", callback_data="coin_heads"),
            InlineKeyboardButton(text="Решка", callback_data="coin_tails")
        ],
        [InlineKeyboardButton(text="В меню", callback_data="info")]
    ])
    await message.answer("Выбери сторону:", reply_markup=keyboard)
    

@dp.callback_query(CoinFSM.Playing, F.data.startswith("coin_"))
async def coin_result(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    username = data["username"]
    bet = data["bet"]
    user_choice = callback.data.split("_")[1]

    eballs_change(username, -bet)  # списываем ставку
    flip_result = random.choices(["heads", "tails", "edge"], weights=[49, 49, 2])[0]

    details = {
        "user_choice": user_choice,
        "flip_result": flip_result
    }

    if flip_result == user_choice:
        prize = bet * 2
        eballs_change(username, prize)
        log_game(username, "coinflip", bet, "win", prize, details)
        await callback.message.edit_text(
            f"🪙 {'Выпал Орел' if flip_result == 'heads' else 'Выпала Решка'}!\n"
            f"Ты выиграл {prize} е-баллов 🎉"
        )
    elif flip_result == "edge":
        bonus = bet//2
        eballs_change(username, bonus)
        log_game(username, "coinflip", bet, "draw", bonus, details)
        await callback.message.edit_text(
            f"🪙 Монетка встала на ребро! 🤯\n"
            f"Ставочка не сыграла, но кэшбек {bonus} е-баллов!"
        )
    else:
        log_game(username, "coinflip", bet, "lose", 0, details)
        await callback.message.edit_text(
            f"🪙 {'Выпал Орел' if flip_result == 'heads' else 'Выпала Решка'}!\n"
            f"Ты просрал {bet} е-баллов 💀"
        )

    await state.set_state(FSM.Depalka)


# -------------------- Блекджек --------------------
@dp.callback_query(FSM.Depalka, F.data == "blackjack")
async def start_blackjack_game(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(BlackjackFSM.Bet)
    await callback.message.edit_text("💰 Введи сумму ставки (>= 5):")

class BlackjackFSM(StatesGroup):
    Bet = State()
    Playing = State()

@dp.message(BlackjackFSM.Bet)
async def set_blackjack_bet(message: types.Message, state: FSMContext):
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
    deck = create_deck()
    player_hand = [draw_card(deck), draw_card(deck)]
    dealer_hand = [draw_card(deck), draw_card(deck)]
    
    await state.update_data(
        bet=bet,
        deck=deck,
        player_hand=player_hand,
        dealer_hand=dealer_hand,
        game_over=False
    )
    await state.set_state(BlackjackFSM.Playing)
    
    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)
    
    details = {
        "player_hand": player_hand,
        "dealer_hand": dealer_hand,
        "player_score": player_score,
        "dealer_score": dealer_score,
        "doubled": False
    }

    if player_score == 21 and dealer_score == 21:
        eballs_change(data["username"], bet)
        log_game(data["username"], "blackjack", bet, "draw", bet, details)
        await message.answer(
            f"🃏 BLACKJACK!\n\n"
            f"Твои карты: {format_hand(player_hand)} = {player_score}\n"
            f"Карты дилера: {format_hand(dealer_hand)} = {dealer_score}\n\n"
            f"Ничья! Ставка возвращена: {bet} е-баллов"
        )
        await state.set_state(FSM.Depalka)
    elif player_score == 21:
        prize = int(bet * 2.5)
        eballs_change(data["username"], prize)
        log_game(data["username"], "blackjack", bet, "win", prize, details)
        await message.answer(
            f"🃏 BLACKJACK!\n\n"
            f"Твои карты: {format_hand(player_hand)} = {player_score}\n"
            f"Карты дилера: {format_hand(dealer_hand, hide_first=True)}\n\n"
            f"🎉 Блекджек! Ты выиграл {prize} е-баллов!"
        )
        await state.set_state(FSM.Depalka)
    else:
        await message.answer(
            f"Твои карты: {format_hand(player_hand)} = {player_score}\n"
            f"Карты дилера: {format_hand(dealer_hand, hide_first=True)}\n\n"
            f"Что делаем?",
            reply_markup=get_blackjack_keyboard(player_hand)
        )

def create_deck():
    suits = ['♠', '♥', '♦', '♣']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = []
    for suit in suits:
        for rank in ranks:
            deck.append(f"{rank}{suit}")
    random.shuffle(deck)
    return deck

def draw_card(deck):
    return deck.pop()

def card_value(card):
    rank = card[:-1]
    if rank in ['J', 'Q', 'K']:
        return 10
    elif rank == 'A':
        return 11
    else:
        return int(rank)

def calculate_score(hand):
    score = 0
    aces = 0
    
    for card in hand:
        value = card_value(card)
        if value == 11:  # туз
            aces += 1
        score += value
    
    while score > 21 and aces > 0:
        score -= 10
        aces -= 1
    
    return score

def format_hand(hand, hide_first=False):
    if hide_first:
        return f"🎴 {' '.join(hand[1:])}"
    return ' '.join(hand)

def get_blackjack_keyboard(player_hand):
    keyboard = [
        [
            InlineKeyboardButton(text="🃏 Взять", callback_data="bj_hit"),
            InlineKeyboardButton(text="✋ Стоп", callback_data="bj_stand")
        ]
    ]
    
    if len(player_hand) == 2:  # первый ход
        keyboard.append([InlineKeyboardButton(text="⚡ Удвоить", callback_data="bj_double")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

@dp.callback_query(BlackjackFSM.Playing, F.data == "bj_hit")
async def blackjack_hit(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    deck = data["deck"]
    player_hand = data["player_hand"]
    dealer_hand = data["dealer_hand"]
    bet = data["bet"]
    username = data["username"]
    
    player_hand.append(draw_card(deck))
    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)
    
    await state.update_data(player_hand=player_hand, deck=deck)
    
    details = {
        "player_hand": player_hand,
        "dealer_hand": dealer_hand,
        "player_score": player_score,
        "dealer_score": dealer_score,
        "doubled": False
    }

    if player_score > 21:
        log_game(username, "blackjack", bet, "lose", 0, details)
        await callback.message.edit_text(
            f"Твои карты: {format_hand(player_hand)} = {player_score}\n"
            f"Карты дилера: {format_hand(dealer_hand, hide_first=True)}\n\n"
            f"💀 Перебор! Ты просрал {bet} е-баллов"
        )
        await state.set_state(FSM.Depalka)
    elif player_score == 21:
        await dealer_turn(callback.message, state)
    else:
        await callback.message.edit_text(
            f"Твои карты: {format_hand(player_hand)} = {player_score}\n"
            f"Карты дилера: {format_hand(dealer_hand, hide_first=True)}\n\n"
            f"Что делаем?",
            reply_markup=get_blackjack_keyboard(player_hand)
        )

@dp.callback_query(BlackjackFSM.Playing, F.data == "bj_stand")
async def blackjack_stand(callback: types.CallbackQuery, state: FSMContext):
    await dealer_turn(callback.message, state)

@dp.callback_query(BlackjackFSM.Playing, F.data == "bj_double")
async def blackjack_double(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    bet = data["bet"]
    username = data["username"]
    
    if eballs_balance(username) < bet:
        await callback.answer("Не хватает денег для удвоения!")
        return
    
    eballs_change(username, -bet)
    
    deck = data["deck"]
    player_hand = data["player_hand"]
    dealer_hand = data["dealer_hand"]
    
    player_hand.append(draw_card(deck))
    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)
    
    await state.update_data(
        player_hand=player_hand,
        deck=deck,
        bet=bet * 2
    )
    
    details = {
        "player_hand": player_hand,
        "dealer_hand": dealer_hand,
        "player_score": player_score,
        "dealer_score": dealer_score,
        "doubled": True
    }

    if player_score > 21:
        log_game(username, "blackjack", bet*2, "lose", 0, details)
        await callback.message.edit_text(
            f"Твои карты: {format_hand(player_hand)} = {player_score}\n"
            f"Карты дилера: {format_hand(dealer_hand, hide_first=True)}\n\n"
            f"💀 Перебор! Ты просрал {bet * 2} е-баллов"
        )
        await state.set_state(FSM.Depalka)
    else:
        await dealer_turn(callback.message, state, doubled=True)

async def dealer_turn(message, state, doubled=False):
    data = await state.get_data()
    deck = data["deck"]
    player_hand = data["player_hand"]
    dealer_hand = data["dealer_hand"]
    bet = data["bet"]
    username = data["username"]
    
    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)
    
    while dealer_score < 17:
        dealer_hand.append(draw_card(deck))
        dealer_score = calculate_score(dealer_hand)
    
    result_text = (
        f"Твои карты: {format_hand(player_hand)} = {player_score}\n"
        f"Карты дилера: {format_hand(dealer_hand)} = {dealer_score}\n\n"
    )
    
    details = {
        "player_hand": player_hand,
        "dealer_hand": dealer_hand,
        "player_score": player_score,
        "dealer_score": dealer_score,
        "doubled": doubled
    }

    if dealer_score > 21:
        prize = bet * 2
        eballs_change(username, prize)
        log_game(username, "blackjack", bet, "win", prize, details)
        result_text += f"🎉 Дилер перебрал! Ты выиграл {prize} е-баллов!"
    elif player_score > dealer_score:
        prize = bet * 2
        eballs_change(username, prize)
        log_game(username, "blackjack", bet, "win", prize, details)
        result_text += f"🎉 Ты выиграл {prize} е-баллов!"
    elif player_score == dealer_score:
        eballs_change(username, bet)
        log_game(username, "blackjack", bet, "draw", bet, details)
        result_text += f"🤝 Ничья! Ставка возвращена: {bet} е-баллов"
    else:
        log_game(username, "blackjack", bet, "lose", 0, details)
        result_text += f"💀 Дилер выиграл! Ты просрал {bet} е-баллов"
    
    await message.edit_text(result_text)
    await state.set_state(FSM.Depalka)


# -------------------- Рулетка --------------------
@dp.callback_query(FSM.Depalka, F.data == "roulette")
async def start_roulette_game(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(RouletteFSM.Bet)
    await callback.message.edit_text("💰 Введи сумму ставки (>= 5):")

class RouletteFSM(StatesGroup):
    Bet = State()
    Playing = State()

@dp.message(RouletteFSM.Bet)
async def set_roulette_bet(message: types.Message, state: FSMContext):
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

    await state.update_data(bet=bet)
    await state.set_state(RouletteFSM.Playing)
    await message.answer(
        "🎰 Выбери тип ставки:\n\n"
        "🔴 Красное (x2) - числа: 1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36\n"
        "⚫ Чёрное (x2) - числа: 2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35\n"
        "🟢 Зеро (x36) - число 0\n"
        "📊 Чётное/Нечётное (x2)\n"
        "📈 Высокие/Низкие (x2) - низкие: 1-18, высокие: 19-36\n"
        "🎯 Конкретное число (x36) от 1 до 36",
        reply_markup=get_roulette_keyboard()
    )

def get_roulette_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔴 Красное", callback_data="roulette_red"),
            InlineKeyboardButton(text="⚫ Чёрное", callback_data="roulette_black"),
            InlineKeyboardButton(text="🟢 Зеро", callback_data="roulette_zero")
        ],
        [
            InlineKeyboardButton(text="Чётное", callback_data="roulette_even"),
            InlineKeyboardButton(text="Нечётное", callback_data="roulette_odd")
        ],
        [
            InlineKeyboardButton(text="Низкие (1-18)", callback_data="roulette_low"),
            InlineKeyboardButton(text="Высокие (19-36)", callback_data="roulette_high")
        ],
        [
            InlineKeyboardButton(text="🎯 Конкретное число", callback_data="roulette_number")
        ],
        [
            InlineKeyboardButton(text="В меню", callback_data="info")
        ]
    ])
    return keyboard

RED_NUMBERS = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
BLACK_NUMBERS = {2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35}

@dp.callback_query(RouletteFSM.Playing, F.data.startswith("roulette_"))
async def roulette_bet_handler(callback: types.CallbackQuery, state: FSMContext):
    bet_type = callback.data.split("_")[1]
    
    if bet_type == "number":
        await callback.message.edit_text(
            "Введи число от 1 до 36:",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Назад", callback_data="roulette_back")]
            ])
        )
        await state.update_data(awaiting_number=True)
        return
    
    await state.update_data(bet_type=bet_type)
    await spin_roulette(callback, state)

@dp.message(RouletteFSM.Playing)
async def number_input_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if not data.get("awaiting_number"):
        return
        
    try:
        number = int(message.text)
        if not (1 <= number <= 36):
            raise ValueError
    except ValueError:
        await message.answer("Это не от 1 до 36 ало")
        return
    
    await state.update_data(bet_type="number", chosen_number=number, awaiting_number=False)
    await spin_roulette_message(message, state)

@dp.callback_query(RouletteFSM.Playing, F.data == "roulette_back")
async def roulette_back(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(awaiting_number=False)
    await callback.message.edit_text(
        "🎰 Выбери тип ставки:\n\n"
        "🔴 Красное (x2) - числа: 1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36\n"
        "⚫ Чёрное (x2) - числа: 2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35\n"
        "🟢 Зеро (x36) - число 0\n"
        "📊 Чётное/Нечётное (x2)\n"
        "📈 Высокие/Низкие (x2) - низкие: 1-18, высокие: 19-36\n"
        "🎯 Конкретное число (x36) от 1 до 36",
        reply_markup=get_roulette_keyboard()
    )

async def spin_roulette(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Крутим рулетку... 🎰")
    await asyncio.sleep(2)
    
    winning_number = random.randint(0, 36)
    
    data = await state.get_data()
    bet = data["bet"]
    bet_type = data["bet_type"]
    username = data["username"]
    
    if winning_number == 0:
        color_emoji = "🟢"
        color_name = "ЗЕРО"
    elif winning_number in RED_NUMBERS:
        color_emoji = "🔴"
        color_name = "красное"
    else:
        color_emoji = "⚫"
        color_name = "чёрное"
    
    win = False
    multiplier = 0
    
    if bet_type == "red" and winning_number in RED_NUMBERS:
        win = True
        multiplier = 2
    elif bet_type == "black" and winning_number in BLACK_NUMBERS:
        win = True
        multiplier = 2
    elif bet_type == "zero" and winning_number == 0:
        win = True
        multiplier = 36
    elif bet_type == "even" and winning_number > 0 and winning_number % 2 == 0:
        win = True
        multiplier = 2
    elif bet_type == "odd" and winning_number % 2 == 1:
        win = True
        multiplier = 2
    elif bet_type == "low" and 1 <= winning_number <= 18:
        win = True
        multiplier = 2
    elif bet_type == "high" and 19 <= winning_number <= 36:
        win = True
        multiplier = 2
    
    eballs_change(username, -bet)
    
    result_text = f"🎰 Выпало: {color_emoji} {winning_number} ({color_name})\n\n"

    details = {
        "bet_type": bet_type,
        "winning_number": winning_number
    }

    if win:
        prize = bet * multiplier
        eballs_change(username, prize)
        log_game(username, "roulette", bet, "win", prize, details)
        result_text += f"🎉 Ты выиграл {prize} е-баллов! (x{multiplier})"
    else:
        log_game(username, "roulette", bet, "lose", 0, details)
        result_text += f"💀 Ты просрал {bet} е-баллов"
    
    await callback.message.edit_text(result_text)
    await state.set_state(FSM.Depalka)

async def spin_roulette_message(message: types.Message, state: FSMContext):
    await message.answer("Крутим рулетку... 🎰")
    await asyncio.sleep(2)

    winning_number = random.randint(0, 36)
    
    data = await state.get_data()
    bet = data["bet"]
    bet_type = data["bet_type"]
    username = data["username"]
    chosen_number = data.get("chosen_number")
    
    if winning_number == 0:
        color_emoji = "🟢"
        color_name = "ЗЕРО"
    elif winning_number in RED_NUMBERS:
        color_emoji = "🔴"
        color_name = "красное"
    else:
        color_emoji = "⚫"
        color_name = "чёрное"
    
    win = winning_number == chosen_number
    multiplier = 36 if win else 0
    
    eballs_change(username, -bet)
    
    result_text = f"🎰 Выпало: {color_emoji} {winning_number} ({color_name})\n"
    result_text += f"Твоя ставка была на: {chosen_number}\n\n"
    
    details = {
        "bet_type": "number",
        "chosen_number": chosen_number,
        "winning_number": winning_number
    }

    if win:
        prize = bet * multiplier
        eballs_change(username, prize)
        log_game(username, "roulette", bet, "win", prize, details)
        result_text += f"🎉 ДЖЕКПОТ! Ты угадал точное число! Выиграл {prize} е-баллов! (x{multiplier})"
    else:
        log_game(username, "roulette", bet, "lose", 0, details)
        result_text += f"💀 Ты просрал {bet} е-баллов"
    
    await message.answer(result_text)
    await state.set_state(FSM.Depalka)


# Хэндлер на команду /stats
@dp.message(Command("stats"), FSM.Depalka)
async def show_stats(message: types.Message, state: FSMContext):
    data = await state.get_data()
    username = data["username"]
    
    # Получаем последние 5 игр пользователя
    user_stats = get_user_stats(username, 5)
    
    if not user_stats:
        await message.answer("Так ты же не играл еще")
        return
    
    stats_text = f"📊 Твоя статистика последних игр:\n\n"
    
    for i, game in enumerate(user_stats, 1):
        game_type_names = {
            'coinflip': '🪙 Монетка',
            'roulette': '💰 Рулетка', 
            'blackjack': '🃏 Блекджек',
            'dig': '💣 Сапёр'
        }
        
        result_emoji = {
            'win': '🎉',
            'lose': '💀', 
            'draw': '🤝'
        }
        
        game_name = game_type_names.get(game['game_type'])
        result = result_emoji.get(game['result'])
        
        stats_text += f"{i}. {game_name}\n"
        stats_text += f"   Ставка: {game['bet_amount']} | Приз: {game['prize_amount']} {result}\n\n"
    
    await message.answer(stats_text)


# Хэндлер на команду /pravda
@dp.message(Command('pravda'), FSM.Depalka)
async def upload_photo(message: types.Message):
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

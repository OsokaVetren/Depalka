from aiogram import Router, types
from aiogram.filters import Command
import asyncio

from Keyboards.to_menu_kb import to_menu_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

from aiogram import F

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from States.user_states import FSM

from Config.config_reader import config
from database.bd_handler import is_user_valid, new_user, eballs_balance, eballs_change, log_game, get_user_stats

import random

router = Router()

# -------------------- Рулетка --------------------
@router.callback_query(FSM.Depalka, F.data == "roulette")
async def start_roulette_game(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(RouletteFSM.Bet)
    await callback.message.edit_text("💰 Введи сумму ставки (>= 5):")

class RouletteFSM(StatesGroup):
    Bet = State()
    Playing = State()

@router.message(RouletteFSM.Bet)
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

@router.callback_query(RouletteFSM.Playing, F.data.startswith("roulette_"))
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

@router.message(RouletteFSM.Playing)
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

@router.callback_query(RouletteFSM.Playing, F.data == "roulette_back")
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
    
    await callback.message.edit_text(result_text, reply_markup=to_menu_kb)
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
    
    await message.answer(result_text, reply_markup=to_menu_kb)
    await state.set_state(FSM.Depalka)

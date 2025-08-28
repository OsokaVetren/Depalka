from aiogram import Router, types
from aiogram.filters import Command

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

@router.callback_query(FSM.Depalka, F.data == "dig")
async def start_dig_game(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(DigFSM.Bet)
    await callback.message.edit_text("💰 Введи сумму ставки (>= 5):")

class DigFSM(StatesGroup):
    Bet = State()
    Playing = State()

@router.message(DigFSM.Bet)
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
        f"Ставка принята: {bet} хатсуне мику\n"
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

@router.callback_query(DigFSM.Playing, F.data.startswith("dig_"))
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
            f"💥 Бум! Ты просрал {bet} хатсуне мику!", reply_markup=to_menu_kb
        )
        await state.set_state(FSM.Depalka)
    else:
        opened.append((r, c))
        profit += int(round(bet * 0.2))
        await state.update_data(opened=opened, profit=profit)
        await callback.message.edit_text(
            f"Текущий выигрыш: {profit} хатсуне мику",
            reply_markup=get_field_keyboard(opened)
        )

@router.callback_query(DigFSM.Playing, F.data == "cashout")
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
        f"Ты забрал {profit} хатсуне мику со ставки {bet}", reply_markup=to_menu_kb
    )
    await state.set_state(FSM.Depalka)
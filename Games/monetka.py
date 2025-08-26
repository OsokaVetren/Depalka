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

@router.callback_query(FSM.Depalka, F.data == "coinflip")
async def start_coin_game(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(CoinFSM.Bet)
    await callback.message.edit_text("💰 Введи сумму ставки (>= 5):")

class CoinFSM(StatesGroup):
    Bet = State()
    Playing = State()

@router.message(CoinFSM.Bet)
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
    

@router.callback_query(CoinFSM.Playing, F.data.startswith("coin_"))
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
            f"Ты выиграл {prize} хатсуне мику 🎉", reply_markup=to_menu_kb
        )
    elif flip_result == "edge":
        bonus = bet//2
        eballs_change(username, bonus)
        log_game(username, "coinflip", bet, "draw", bonus, details)
        await callback.message.edit_text(
            f"🪙 Монетка встала на ребро! 🤯\n"
            f"Ставочка не сыграла, но кэшбек {bonus} хатсуне мику", reply_markup=to_menu_kb
        )
    else:
        log_game(username, "coinflip", bet, "lose", 0, details)
        await callback.message.edit_text(
            f"🪙 {'Выпал Орел' if flip_result == 'heads' else 'Выпала Решка'}!\n"
            f"Ты просрал {bet} хатсуне мику 💀", reply_markup=to_menu_kb
        )

    await state.set_state(FSM.Depalka)

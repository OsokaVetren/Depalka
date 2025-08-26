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

# -------------------- Блекджек --------------------
@router.callback_query(FSM.Depalka, F.data == "blackjack")
async def start_blackjack_game(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(BlackjackFSM.Bet)
    await callback.message.edit_text("💰 Введи сумму ставки (>= 5):")

class BlackjackFSM(StatesGroup):
    Bet = State()
    Playing = State()
from database.bd_handler import get_user_stats
@router.message(BlackjackFSM.Bet)
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
            f"Ничья! Ставка возвращена: {bet} хатсуне мику", reply_markup=to_menu_kb
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
            f"🎉 Блекджек! Ты выиграл {prize} е-баллов!", reply_markup=to_menu_kb
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

@router.callback_query(BlackjackFSM.Playing, F.data == "bj_hit")
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
            f"💀 Перебор! Ты просрал {bet} хатсуне мику", reply_markup=to_menu_kb
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

@router.callback_query(BlackjackFSM.Playing, F.data == "bj_stand")
async def blackjack_stand(callback: types.CallbackQuery, state: FSMContext):
    await dealer_turn(callback.message, state)

@router.callback_query(BlackjackFSM.Playing, F.data == "bj_double")
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
            f"💀 Перебор! Ты просрал {bet * 2} е-баллов", reply_markup=to_menu_kb
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
        result_text += f"🎉 Дилер перебрал! Ты выиграл {prize} хатсуне мику!"
    elif player_score > dealer_score:
        prize = bet * 2
        eballs_change(username, prize)
        log_game(username, "blackjack", bet, "win", prize, details)
        result_text += f"🎉 Ты выиграл {prize} хатсуне мику!"
    elif player_score == dealer_score:
        eballs_change(username, bet)
        log_game(username, "blackjack", bet, "draw", bet, details)
        result_text += f"🤝 Ничья! Ставка возвращена: {bet} хатсуне мику!"
    else:
        log_game(username, "blackjack", bet, "lose", 0, details)
        result_text += f"💀 Дилер выиграл! Ты просрал {bet} хатсуне мику!"
    
    await message.edit_text(result_text, reply_markup=to_menu_kb)
    await state.set_state(FSM.Depalka)


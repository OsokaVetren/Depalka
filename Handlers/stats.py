from aiogram import Router, types
from aiogram.filters import Command

from Keyboards.to_menu_kb import to_menu_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from States.user_states import FSM

from database.bd_handler import get_user_stats

router = Router()

@router.message(Command("stats"), FSM.Depalka)
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
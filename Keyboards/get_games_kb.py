from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

get_games_kb = InlineKeyboardMarkup(inline_keyboard=[
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
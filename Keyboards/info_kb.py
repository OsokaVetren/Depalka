from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

info_kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Игры", callback_data="games"),
            InlineKeyboardButton(text="Помощь", callback_data="help"),
        ], [
            InlineKeyboardButton(text="Выход из аккаунта", callback_data="logout"),
        ]
    ])
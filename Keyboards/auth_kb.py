from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile


auth_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Регистрация", callback_data="register"),
        InlineKeyboardButton(text="Вход", callback_data="login")
    ]
])
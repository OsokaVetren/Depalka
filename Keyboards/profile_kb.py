from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

profile_kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Сменить логин", callback_data="new_login"),
            InlineKeyboardButton(text="Сменить пароль", callback_data="new_password")
        ], [
            InlineKeyboardButton(text="Достижения", callback_data="achievements")
        ], [
            InlineKeyboardButton(text="В меню", callback_data="info")
        ]
    ])
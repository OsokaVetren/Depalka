from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

to_menu_kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="В меню", callback_data="info")
        ]
    ])
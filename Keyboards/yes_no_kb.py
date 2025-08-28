from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

yes_no_kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅", callback_data="yes"),
            InlineKeyboardButton(text="❌", callback_data="no"),
        ]
    ])
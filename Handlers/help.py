from aiogram import Router, types
from aiogram.filters import Command

from Keyboards.to_menu_kb import to_menu_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

from aiogram import F

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from States.user_states import FSM

router = Router()

@router.callback_query(FSM.Depalka, F.data == "help")
async def get_help(callback: types.CallbackQuery):
    await callback.message.edit_text("В депалке есть множество способов поднять е-баллов и стать самым крутым в садике😎\n\n"
                                  "🪙 Монетка - выбираешь сторону и бросаешь монетку. "
                                  "Если выбранная сторона окажется верной, ставочка приумножится x2, а если неверной, то гуляй вася жуй опилки\n"
                                  "💰 Рулетка - там крч колесо крутится и ставить можно по-разному, сами разберётесь крч\n"
                                  "💣 Сапёр - есть сетка из плиток, в каждой из них либо приз, либо мина. После каждой плитки можно либо вывести приз, либо продолжить гэмблить. "
                                  "Наступил на мину - поздравляю, ты лох)\n"
                                  "🃏 Блекджек - тихий и стандартный, цель - набрать больше очков, чем дилер, но не более 21. "
                                  "Присутствует смелая возможность удвоить ставочку на первом ходу, но и шанс оподливиться станет выше\n\n"
                                  "P.S.: напиши /stats, чтобы посмотреть статку последних 5 игр, или /pravda, чтобы узнать секрет🤫",
                                  reply_markup=to_menu_kb)
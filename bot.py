#импорт разных библиотек нахуй
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, Router

#handlers
from Handlers import start, auth_loop, info, help, games, pravda, stats, scheduler_test, profile, achievements
from Games import saper, monetka, ruletka, blackjack

from Config.config_reader import config


# кто откатит коммит тот гей

#⠀⠀⠀⠀⠀⠀⠀⢀⣤⣴⣶⣶⣶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⢀⣴⣿⠟⠛⠛⠛⠛⠛⢿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⢀⣾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠙⢷⡄⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⣾⣁⣤⣴⣶⣤⣀⢀⣴⣶⣶⣦⣸⣷⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⢀⣿⠿⣿⣿⣿⣿⠟⠛⢿⣿⣿⣿⠛⣿⢦⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⣏⡏⠀⠙⠛⠋⣡⣴⣦⣼⡍⠉⠁⠀⢸⢺⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠻⣽⠀⠀⠀⠀⠀⠉⣈⡉⠁⠀⠀⠀⣸⠊⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⢣⠀⠀⠀⠀⠀⠛⠋⠀⠀⠀⢠⠃⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⢀⣤⣶⣷⣤⣤⣀⣀⠀⠤⠤⣤⣶⣿⣿⣶⣦⡄⠀⠀⠀⠀
#⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⢄⣾⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀
#⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⠋⠉⡚⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀
#⠀⠀⠀⠀⠻⢿⣿⣿⣿⣿⣧⣧⣿⣷⣿⣿⣿⣿⡿⢿⣿⠿⠀⠀⠀
#⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀
#⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣀⠀⠀⠀⠀
#⠀⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀
#⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀
#⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣇
#⢸⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⡇
#⠀⢿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⠃
#⠀⠘⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀
#⠀⠀⢻⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⢺⣿⡻⣿⡿⠟⠋⠀⠀⠀⠀
#⠀⠀⠨⠿⣿⠛⢻⡅⠀⠀⠀⠀⠀⠀⠀⠙⣧⣷⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⡜⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠈⠋⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⢸⠿⡋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=config.bot_token.get_secret_value())
# Диспетчер
dp = Dispatcher()

dp.include_router(start.router)
dp.include_router(auth_loop.router)
dp.include_router(info.router)
dp.include_router(help.router)
dp.include_router(games.router)
dp.include_router(pravda.router)
dp.include_router(stats.router)
dp.include_router(top.router)
dp.include_router(saper.router)
dp.include_router(ruletka.router)
dp.include_router(monetka.router)
dp.include_router(blackjack.router)
dp.include_router(profile.router)
dp.include_router(achievements.router)

# Запуск процесса поллинга новых апдейтов
async def main():
    scheduler_test.schedule_job()
    scheduler_test.scheduler_start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

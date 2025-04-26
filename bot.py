# bot.py
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.methods import DeleteWebhook

from config import config
from handlers.start import router as start_router
from handlers.groups import router as groups_router
from handlers.duplication import router as dup_router
from handlers.messages import router as messages_router

async def main():
    bot = Bot(token=config.TOKEN)
    dp  = Dispatcher()

    # Подключаем роутеры
    dp.include_router(start_router)
    dp.include_router(groups_router)
    dp.include_router(dup_router)
    dp.include_router(messages_router)

    # Сбрасываем вебхуки
    await bot(DeleteWebhook(drop_pending_updates=True))

    # Запуск polling
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
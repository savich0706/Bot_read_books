import asyncio

from aiogram import Bot, Dispatcher
from configuration.config import load_config


async def main():
    '''инициализация бота и диспетчера, создание цикла
        событий добавление диспетчера в Event Loop'''
        
    
    # Инициализация бота и диспетчера
    bot = Bot(token=load_config())
    dp = Dispatcher()
    
    # Пропускаем накопившиеся апдейты и запускаем полинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
asyncio.run(main())
import asyncio
import logging

from aiogram import Bot, Dispatcher
from configuration.config import load_config
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from hendlers import user_handlers, other_handlers
from menu.menu import set_menu

logger = logging.getLogger(__name__)

async def main():
    '''инициализация бота и диспетчера, создание цикла
        событий добавление диспетчера в Event Loop'''
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
                '[%(asctime)s] - %(name)s - %(message)s')
    
    # Вывод информации о старте бота в консоль
    logger.info('Запуск бота')   
    
    # Инициализация бота и диспетчера
    bot = Bot(token=load_config(),
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    
    # Регистрируем роутеры в диспетчере для корректной обработки
    # диспетчером апдейтов от телеграма
    dp.include_router(user_handlers.router)
     
    #устанавливаем меню с командами
    await set_menu(bot)
    
    # Пропускаем накопившиеся апдейты и запускаем полинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
asyncio.run(main())
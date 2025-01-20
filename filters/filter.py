from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


# фильтр обработки удаления закладок 
class DelBookmarks(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.endswith('del') and callback.data[:-3].isdigit()
    

# фильтр обработки нажатия на закладку для перехода на сохраненную страницу
class IsDigitCallback(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.isdigit()
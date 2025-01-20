from copy import deepcopy

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery

from lexicon.lexicon import LEXICON
from database.database import user_db, data_template
from services.book import book

from keyboards.inline_leyboard import create_keyboard
from keyboards.bookmarks import create_bookmarks_keyboard, create_edit_bookmarks

from filters.filter import DelBookmarks, IsDigitCallback


router = Router()

# Этот хэндлер будет срабатывать на команду "/start" -
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@router.message(CommandStart())
async def command_start(message: Message):
    await message.answer(LEXICON[message.text])
    if message.from_user.id not in user_db:
        user_db[message.from_user.id] = deepcopy(data_template)
        
        
# Хендлер для обработки команды "/help"
@router.message(Command(commands='help'))
async def command_help(message: Message):
    await message.answer(LEXICON[message.text])
    

# Хендлер обработки команды "/beginning"
# и отправляет пользователю первую страницу книги
@router.message(Command(commands='beginning'))
async def command_beginning(message: Message):
    user_db[message.from_user.id]['page'] = 1
    text = book[1]
    await message.answer(
        text=text,
        reply_markup=create_keyboard(
            f'{user_db[message.from_user.id]['page']}/{len(book)}',
            'forward')
        )
    

# Хендлер обрабатывающий /continue
@router.message(Command(commands='continue'))
async def process_command_continue(message: Message):
    await message.answer(
        text=book[user_db[message.from_user.id]['page']],
        reply_markup=create_keyboard(*(
            'backward',
             f'{user_db[message.from_user.id]['page']}/{len(book)}',
            'forward'
            ) 
            if user_db[message.from_user.id]['page'] != 1 and user_db[message.from_user.id]['page'] != len(book)
            else (
                (f'{user_db[message.from_user.id]['page']}/{len(book)}',
                'forward') 
                if user_db[message.from_user.id]['page'] == 1 
                else
                ('backward',
                f'{user_db[message.from_user.id]['page']}/{len(book)}')
                )))


# Хендлер обработки callback 'forward' будет отправлять 
# следующую страницу книги    
@router.callback_query(F.data == 'forward')
async def process_command_forward(callback: CallbackQuery):

    user_db[callback.from_user.id]['page'] += 1
    text = book[user_db[callback.from_user.id]['page']]
    
    await callback.message.edit_text(
        text=text,
        reply_markup=create_keyboard(
            *('backward', f'{user_db[callback.from_user.id]['page']}/{len(book)}', 'forward')  
                if not user_db[callback.from_user.id]['page'] == len(book)
                else ('backward', f'{user_db[callback.from_user.id]['page']}/{len(book)}')
    ))
        
        
# Хендлер обработки callback 'backward' будет отправлять 
# следующую страницу книги    
@router.callback_query(F.data == 'backward')
async def process_command_backward(callback: CallbackQuery):
    if user_db[callback.from_user.id]['page'] > 2:
        user_db[callback.from_user.id]['page'] -= 1
        text = book[user_db[callback.from_user.id]['page']]
        
        await callback.message.edit_text(
            text=text,
            reply_markup=create_keyboard(
                'backward', 
                f'{user_db[callback.from_user.id]['page']}/{len(book)}', 
                'forward'
            ))
    else:
        user_db[callback.from_user.id]['page'] -= 1
        text = book[user_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_keyboard(
                f'{user_db[callback.from_user.id]['page']}/{len(book)}', 
                'forward'
            ))
        
        
# Хендлер добавляющий в закладки нужную страницу
@router.callback_query(lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
async def process_page_press(callback: CallbackQuery):
    if user_db[callback.from_user.id]['page'] not in user_db[callback.from_user.id]['bookmarks']:
        user_db[callback.from_user.id]['bookmarks'].add(
            user_db[callback.from_user.id]['page'])
        await callback.answer('Страница добавлена в закладки!')
    else:
        await callback.answer('Страница сохранена в закладках ранее!')
        
        
# Хендлер обрабатывающий "/bookmarks"
@router.message(Command(commands='bookmarks'))
async def process_bookmarks(message: Message):
    if not user_db[message.from_user.id]['bookmarks']:
        await message.answer(text=LEXICON['no_bookmarks'])
    else:
        await message.answer(
            text='Ваши сохраненные закладки:',
            reply_markup=create_bookmarks_keyboard(*user_db[message.from_user.id]['bookmarks']))
      
        
# Хендлер обработки callback "Редактировать"
@router.callback_query(F.data == 'edit_bookmarks')
async def process_edit_bookmarks(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON[callback.data],
        reply_markup=create_edit_bookmarks(
            *user_db[callback.from_user.id]['bookmarks']
        )
    )
    

# Хендлер удаляющий закладки по нажатию на инлайн кнопки
@router.callback_query(DelBookmarks())
async def delete_bookmarks(callback: CallbackQuery):
    user_db[callback.from_user.id]['bookmarks'].remove(
        int(callback.data[:-3])
    )
    if user_db[callback.from_user.id]['bookmarks']:
        await callback.message.edit_text(
            text=LEXICON['/bookmarks'],
            reply_markup=create_edit_bookmarks(
                *user_db[callback.from_user.id]['bookmarks']
            )
        )
    else:
        await callback.message.edit_text(text=LEXICON['no_bookmarks'])
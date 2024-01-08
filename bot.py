from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ParseMode
from aiogram.dispatcher.filters import Text
from config import TOKEN

import sqlite3
import requests

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Подключение sqlite db
conn = sqlite3.Connection("lib_book.db")
cur = conn.cursor()


# Начало
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    # Обычные кнопки
    start_button = ['Поиск', 'Random']
    keyboards = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboards.add(*start_button)

    # Inline кнопки
    link_buttons = [
        InlineKeyboardButton(
            text='GitHub', url='https://github.com/ZeroNiki/FBook-bot')
    ]
    link_keyboards = InlineKeyboardMarkup(row_width=1)
    link_keyboards.add(*link_buttons)

    await message.answer("Привет! Я бот поиска и устоновки книг FBook.\n", reply_markup=link_keyboards)
    await message.answer("↑↑ GITHUB ↑↑", reply_markup=keyboards)


# Inline button 'download' (fb2) (Random)
@dp.callback_query_handler(text="random_fb2")
async def inline_keyboard_fb2(call: types.CallbackQuery):
    await call.message.answer("Идёт устоновка")

    id = book_id
    name = book_name

    url = f'https://flibusta.is/b/{id}/fb2'

    response = requests.get(url)

    if response.status_code == 200:
        with open(f'book/{name}.zip', 'wb') as file:
            file.write(response.content)
            print("Файл успешно скачан")
    else:
        print("Ошибка при скачивании файла")


# Inline button 'download' (fb2) (Specific)
@dp.callback_query_handler(text="fb2_specific")
async def inline_keyboard_fb2(call: types.CallbackQuery):
    await call.message.answer("Кнопка пока что не работает скачиваете через ссылку")


# Random function
@dp.message_handler(Text(equals="Random"))
async def rand_book(message: types.Message):
    # global values
    global book_id
    global book_name

    # inline keyboard
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(text='FB2', callback_data='random_fb2'))

    # db
    cur.execute(
        "SELECT id, name_book, author, genre_book, download_link, discription, img FROM books ORDER BY RANDOM() LIMIT 1")
    book = cur.fetchone()

    # message
    msg_text = (
        f"*{book[1]}*\n\n"
        f"_{book[2]}_\n\n"
        f"_{book[3]}_\n\n"
        f"{book[5]}\n\n"
        f"[Ссылка на скачивание]({book[4]})\n\n"
        f"[Ссылка на изоброжение]({book[6]})"
    )
    await message.answer(msg_text, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)

    book_id = book[0]
    book_name = book[1]


# Search
@ dp.message_handler(Text(equals="Поиск"))
async def search(message: types.Message):
    await message.answer("Введите название книги: ")


@ dp.message_handler(content_types="text")
async def search_book(message: types.Message):
    # inline keyboard
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(
        text='Пока не работает', callback_data='fb2_specific'))

    book_name_search = message.text

    cur.execute("SELECT id, name_book, author, genre_book, download_link, discription, img FROM books WHERE name_book LIKE ?",
                ('%' + book_name_search + '%',))

    items = cur.fetchall()

    for item in items:
        msg_text = (
            f"*{item[1]}*\n\n"
            f"_{item[2]}_\n\n"
            f"_{item[3]}_\n\n"
            f"{item[5]}\n\n"
            f"[Ссылка на скачивание]({item[4]})\n\n"
            f"[Ссылка на изоброжение]({item[6]})"
        )
        await message.answer(msg_text, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
    conn.close()

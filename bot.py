from aiogram import Bot, Dispatcher, types, executor
from config import TOKEN

import sqlite3


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Подключение sqlite db
conn = sqlite3.Connection("lib_book.db")
cur = conn.cursor()


# Начало
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я FBook bot.\nИспользуй /help чтобы увидеть список комманд")


# Command list
@dp.message_handler(commands=['help'])
async def command_list(message: types.Message):
    await message.reply("/search - посик по названию книги\n/random - книги на угад")


# Search
@dp.message_handler(commands=['search'])
async def search(message: types.Message):
    await message.answer("Введите название книги: ")


@dp.message_handler()
async def search_book(message: types.Message):
    book_name = message.text

    cur.execute("SELECT name_book, author, genre_book, download_link FROM books WHERE name_book LIKE ?",
                ('%' + book_name + '%',))

    items = cur.fetchall()

    for item in items:
        await message.answer(f"{} {} {} {}")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
    conn.close()

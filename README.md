# FBook-bot
- `aiogram 2.23.1`
- `requests`
- `sqlite3`

Бот для поиска и устоновки книг с применением бд sqlite


## Установка (GNU/LINUX)

1:
```sh
git clone https://github.com/ZeroNiki/FBook-bot.git
cd FBook-bot
```

2:
```sh
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```
3: 
[Ссылка на бд для скачивания (Google Drive)](https://drive.google.com/file/d/1Mdt1kpnSiwIwWgcC1uE77B37oyliEblM/view?usp=drive_link)
Переместите файл `lib_book.db` в `FBook-bot/`

4:
создайте файл `config.py` и впешите в нём:
```python
TOKEN = "Ваш токен бота телеграмма"
```
и вставьте в переменную ваш токен

5:
```sh
python3 bot.py
```




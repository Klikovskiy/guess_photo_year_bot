# Guess Photo Year - игровой телеграм бот.

Telegram-бот, предлагает угадать год по событию, которое происходит на фото. Для запуска игры необходимо использовать кодовые фразы `Играть, Хочу играть` и т.д. Бот пришлет изображение и несколько дат на выбор, пользователь должен угадать дату события.

В случае успешного угадывания даты, бот подробнее расскажет о событии. Если, пользователь ошибся, то дополнительно будет указана правильная дата.

**Команды**:

 - `/start` - запустить бота.
 - `/help` - правила игры и команды.
 - `/cancel` - выход из режима игры.

Бот хранит данные о пользователе в словаре "users_base", поэтому потеряет информацию после остановки. Данные для вопросов, хранятся в "data.json".

# Зависимости 

    Python 3.10+
    aiogram 3+

# Установка

1. Скопировать репозиторий:

```bash
git clone https://github.com/klikovskiy/guess_photo_year_bot.git
```

2. Создать виртуальное окружение и установить зависимости:

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

```

4. Заполнить файл `.env.dist` и переименовать его `.env`.

5. Запуск бота.

```bash
python bot.py
```
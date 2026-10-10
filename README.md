# Telegram Task Bot

Простой Telegram-бот для командной работы. Пользователи могут добавлять задачи, просматривать список и получать его в CSV-файле.

## Установка

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Настройка

1. Создайте файл `.env` на основе `.env.example`.
2. Укажите токен Telegram-бота:

```text
BOT_TOKEN=ваш_telegram_token
```

3. Запустите бота:

```bash
python main.py
```

## Команды

- `/start` — приветствие.
- `/add` — начать добавление задачи.
- `/list` — показать все задачи.
- `/list_csv` — отправить задачи в CSV-файле.

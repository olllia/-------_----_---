# Telegram Face Detection Bot 🎥🤖

Этот проект представляет собой Telegram-бота, который выполняет детекцию лиц на фото и видео, а также определяет пол для обнаруженных лиц. Бот полностью написан на Python с использованием библиотек `telegram.ext`, `torch`, `cv2`, и других.

## 🚀 Возможности

- 🎬 Принимает видео от пользователей.
- 🕵️‍♂️ Выполняет детекцию лиц на видео.
- 👩‍🦰👨 Определяет пол для каждого обнаруженного лица.
- 🔄 Обрабатывает видео с обрезкой до заданной длины.
- 💬 Интерактивный интерфейс через Telegram.

## 📂 Структура проекта

- `bot.py` — Основной файл для запуска Telegram-бота.
- `handlers.py` — Логика обработки сообщений и команд.
- `video_processing.py` — Модуль обработки видео, включая детекцию лиц и классификацию пола.
- `config.py` — Конфигурации и ключи, включая токен Telegram-бота.
- `gender_classification.pth` — Предобученные веса модели для классификации пола.

## 🛠 Установка

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/yourusername/telegram-face-detection-bot.git
    cd telegram-face-detection-bot
    ```

2. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

3. Укажите свой Telegram Bot API токен в `config.py`:
    ```python
    TOKEN = "your_telegram_bot_token"
    ```

4. Убедитесь, что файл модели `gender_classification.pth` находится в корне проекта.

## 🔧 Запуск

Запустите бота:
```bash
python bot.py

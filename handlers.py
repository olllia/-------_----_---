import logging
from moviepy.video.io.VideoFileClip import VideoFileClip
from telegram import ReplyKeyboardMarkup, Update
from config import TOKEN, MAX_VIDEO_DURATION
from video_processing import process_video_with_faces
import os


import logging
import tempfile
from telegram import ReplyKeyboardMarkup, Update
from config import MAX_VIDEO_DURATION
from video_processing import process_video_with_faces
import os


# Обработчик команды /start
async def start(update: Update, context):
    keyboard = [
        ['🎬 Отправить видео', '🆘 Помощь']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    welcome_message = (
        "👋 Привет! Отправь видео — я найду на нём лица!\n\n"
        "💡 Команды:\n"
        "📹 'Отправить видео' - Обработка видео\n"
        "🆘 'Помощь' - Помощь\n"
    )
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)


# Обработчик текстовых сообщений
async def handle_text(update: Update, context):
    text_received = update.message.text
    if text_received == '🎬 Отправить видео':
        await update.message.reply_text("Отправьте видео для анализа.")
    elif text_received == '🆘 Помощь':
        await update.message.reply_text("Я ищу лица на видео!")
    else:
        await update.message.reply_text("Выберите команду из меню.")

# Обработчик видео
async def handle_video(update: Update, context):
    logging.info("Получено видео")
    
    # Получаем объект файла из сообщения
    video_file = await update.message.video.get_file()

    # Создаем временные файлы для загрузки и обработки видео
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video_file:
        temp_video_path = temp_video_file.name
        temp_video_file.write(await video_file.download_as_bytearray())  # Скачиваем видео в виде байтов и записываем
        
    output_video_path = f"{temp_video_path}_processed.mp4"

    try:
        await update.message.reply_text("Обрабатываю видео для обнаружения лиц...")

        # Обработка видео с обрезкой до MAX_VIDEO_DURATION при необходимости
        gender_list = process_video_with_faces(temp_video_path, output_video_path)  # Получаем список полов

        # Отправка обработанного видео пользователю
        with open(output_video_path, 'rb') as video:
            await update.message.reply_video(video=video)

    except Exception as e:
        logging.error(f"Ошибка при обработке видео: {e}")
        await update.message.reply_text("Произошла ошибка при обработке видео. Пожалуйста, попробуйте снова.")

    finally:
        # Удаление временных файлов после обработки
        os.remove(temp_video_path)
        if os.path.exists(output_video_path):
            os.remove(output_video_path)

    logging.info("Видео успешно обработано")




import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import TOKEN
from handlers import start, handle_text, handle_video

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT, handle_text))
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))
    application.run_polling()


if __name__ == '__main__':
    main()

import os
import logging.config

from time import sleep
from dotenv import load_dotenv
from intent import detect_intent_texts
from settings import logger_config

from telegram import Update, ForceReply
from telegram.ext import CallbackContext
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


logging.config.dictConfig(logger_config)
logger = logging.getLogger('app_logger')
logger.debug('Бот telegram_chat запущен.')


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    logger.debug("Пользователь выполнил команду /start")

    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Здравствуйте {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def auto_response(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    texts = []
    chat_id = update.message.from_user.id
    text = update.message.text
    texts.append(text)
    project_id = os.getenv('PROJECT_ID')
    logger.debug(f"Текст который прислал пользователь {text} отправляем его на "
                f"обработку в dialogflow")
    intent_response = detect_intent_texts(
        project_id, chat_id, texts, language_code='ru'
    )
    update.message.reply_text(intent_response.fulfillment_text)


def main() -> None:
    """Start the bot."""
    load_dotenv()
    TIMEOUT = 120
    api_tg_token = os.getenv('API_TG_TOKEN')

    while True:
        try:
            updater = Updater(api_tg_token)

            dispatcher = updater.dispatcher

            dispatcher.add_handler(CommandHandler("start", start))
            dispatcher.add_handler(CommandHandler("help", help_command))
            dispatcher.add_handler(
                MessageHandler(Filters.text & ~Filters.command, auto_response)
            )

            updater.start_polling()
            updater.idle()
        except Exception:
            logger.exception("Бот упал с ошибкой")
            sleep(TIMEOUT)


if __name__ == '__main__':
    main()

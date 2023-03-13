import os
import logging

from time import sleep
from dotenv import load_dotenv
from intent import detect_intent_texts

from telegram import Update, ForceReply, Bot
from telegram.ext import CallbackContext
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


logger = logging.getLogger(__name__)
exception_logger = logging.getLogger('exception_logger')


class TelegramLogsHandler(logging.Handler):

    def __init__(self, api_tg_token, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = Bot(token=api_tg_token)

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    logger.info("Пользователь выполнил команду /start")

    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Здравствуйте {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def get_auto_reply(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.from_user.id
    text = update.message.text
    project_id = os.getenv('PROJECT_ID')
    logger.info(f"Текст который прислал пользователь {text} отправляем его на "
                f"обработку в dialogflow")
    intent_response = detect_intent_texts(
        project_id, chat_id, text, language_code='ru'
    )
    update.message.reply_text(intent_response.fulfillment_text)


def main() -> None:
    load_dotenv()
    TIMEOUT = 120
    chat_id = os.getenv('TG_CHAT_ID')
    api_tg_token = os.getenv('API_TG_TOKEN')

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - '
                               '%(message)s', datefmt='%d-%m-%Y %I:%M:%S %p',
                        level=logging.INFO)

    exception_logger.setLevel(logging.ERROR)
    exception_logger.addHandler(TelegramLogsHandler(api_tg_token, chat_id))

    while True:
        try:
            updater = Updater(api_tg_token)

            dispatcher = updater.dispatcher

            dispatcher.add_handler(CommandHandler("start", start))
            dispatcher.add_handler(
                MessageHandler(Filters.text & ~Filters.command, get_auto_reply)
            )

            updater.start_polling()
            updater.idle()
        except Exception:
            exception_logger.exception("Бот упал с ошибкой")
            sleep(TIMEOUT)


if __name__ == '__main__':
    main()

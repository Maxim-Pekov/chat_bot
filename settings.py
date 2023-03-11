import logging
import os
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()
chat_id = os.getenv('TG_CHAT_ID')
API_TG_TOKEN = os.getenv('API_TG_TOKEN')
logger = logging.getLogger('app_logger')


class TelegramLogsHandler(logging.Handler):

    def __init__(self, API_TG_TOKEN, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = Bot(token=API_TG_TOKEN)

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


logger_config = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'std_format': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': '%d-%m-%Y %I:%M:%S %p',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'std_format',
        },
        'telegram': {
            '()': TelegramLogsHandler,
            'level': 'ERROR',
            'API_TG_TOKEN': API_TG_TOKEN,
            'chat_id': chat_id,
            'formatter': 'std_format'
        }
    },
    'loggers': {
        'app_logger': {
            'level': 'DEBUG',
            'handlers': ['console', 'telegram'],
            'propagate': False,
        },
    }
}
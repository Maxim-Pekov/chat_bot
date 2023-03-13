import os
import random
import logging

import vk_api as vk
from time import sleep
from telegram_chat import TelegramLogsHandler
from dotenv import load_dotenv
from intent import detect_intent_texts
from vk_api.longpoll import VkLongPoll, VkEventType


logger = logging.getLogger(__name__)
exception_logger = logging.getLogger('exception_logger')


def get_auto_reply(event, vk_api):
    """Отправляет текст принятого сообщения на обработку в dialogflow, а
    сгенерированный ответ посылает обратно пользователю."""
    text = event.text
    session_id = event.user_id
    project_id = os.getenv('PROJECT_ID')

    logger.info(f"Текст который прислал пользователь texts='{texts}'"
                 f" отправляем его на обработку в dialogflow")
    response_text = detect_intent_texts(
        project_id, session_id, text, language_code='ru'
    )
    if not response_text.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=response_text.fulfillment_text,
            random_id=random.random()
        )


if __name__ == "__main__":
    load_dotenv()
    TIMEOUT = 120
    vk_session = vk.VkApi(token=os.getenv('VK_API_KEY'))
    chat_id = os.getenv('TG_CHAT_ID')
    api_tg_token = os.getenv('API_TG_TOKEN')

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - '
                               '%(message)s', datefmt='%d-%m-%Y %I:%M:%S %p',
                        level=logging.INFO)

    exception_logger.setLevel(logging.ERROR)
    exception_logger.addHandler(TelegramLogsHandler(api_tg_token, chat_id))

    while True:
        try:
            vk_api = vk_session.get_api()
            longpoll = VkLongPoll(vk_session)

            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    logger.info('Пришло сообщение в ВК от: ', event.user_id)
                    get_auto_reply(event, vk_api)
        except Exception:
            exception_logger.exception("Бот упал с ошибкой")
            sleep(TIMEOUT)

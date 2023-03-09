import os
import random

import vk_api as vk
from dotenv import load_dotenv
from intent import detect_intent_texts
from vk_api.longpoll import VkLongPoll, VkEventType


def auto_response(event, vk_api):
    """Отправляет текст принятого сообщения на обработку в dialogflow, а
    сгенерированный ответ посылает обратно пользователю."""
    texts = [event.text]
    session_id = event.user_id
    project_id = os.getenv('PROJECT_ID')
    response_text = detect_intent_texts(
        project_id, session_id, texts, language_code='ru'
    )
    if not response_text.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=response_text.fulfillment_text,
            random_id=random.random()
        )


if __name__ == "__main__":
    load_dotenv()

    vk_session = vk.VkApi(token=os.getenv('VK_API_KEY'))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            print('Для меня от: ', event.user_id)
            auto_response(event, vk_api)

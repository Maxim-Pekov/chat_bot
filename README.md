![Typing SVG](https://readme-typing-svg.herokuapp.com?color=%2336BCF7&lines=CHAT+BOT)


Этот проект бота чата тех. поддержки для ВК и Телеграмм. Который можно гибко 
обучать с помошью [https://dialogflow.cloud.google.com](https://dialogflow.cloud.google.com)

## Пример общения телеграмм бота.
<img src="static/demo_tg_bot.gif" width="300">

## Пример общения VK бота.
<img src="static/demo_vk_bot.gif" width="300">


## Готовых ботов вы можете протестировать по ссылкам:
* telegram - @chat_secretary_bot
* vk_bot - [https://vk.com/im?peers=c25&sel=-219276102](https://vk.com/im?peers=c25&sel=-219276102)

## Проект содержит три скрипта:
* `vk_chat.py` - Скрипт проверяет полученные сообщения в чате группы ВК и 
  отвечает на них с помошью dialogflow.
* `telegram_chat.py` - Скрипт при получении сообщения в ТГ отвечает на них 
  генерируя ответ с помошью dialogflow.
* `intent.py` - Скрипт обучает бота с помошью переданного в него json с 
  набором вопросов и ответами на них.

## Установка

Используйте данную инструкцию по установке этого скрипта

1. Установить

```python
git clone https://github.com/Maxim-Pekov/chat_bot.git
```

2. Создайте виртуальное окружение:

```python
python -m venv venv
```

3. Активируйте виртуальное окружение:
```python
.\venv\Scripts\activate    # for Windows
```
```python
source ./.venv/bin/activate    # for Linux
```

4. Перейдите в директорию `chat_bot`
5. Установите зависимости командой ниже:
```python
pip install -r devman_bot/requirements.txt
```

6. Создайте файл с названием `.env`

7. Запишите в данном файле, ваш API токен с сайта ВК, телеграмм токен 
   вашего бота и PROJECT_ID полученный на сайте dialogflow.
```python
VK_API_KEY='vk1.a.bNnlnbblk47y5l4........'
PROJECT_ID='red-flowers-566321'
TG_CHAT_ID='7418955261'
```

## About me

[<img align="left" alt="maxim-pekov | LinkedIn" width="30px" src="https://img.icons8.com/color/48/000000/linkedin-circled--v3.png" />https://www.linkedin.com/in/maxim-pekov/](https://www.linkedin.com/in/maxim-pekov/)
</br>

[<img align="left" alt="maxim-pekov" width="28px" src="https://upload.wikimedia.org/wikipedia/commons/5/5c/Telegram_Messenger.png" />https://t.me/MaxPekov/](https://t.me/MaxPekov/)
</br>

[//]: # (Карточка профиля: )
![](https://github-profile-summary-cards.vercel.app/api/cards/profile-details?username=Maxim-Pekov&theme=solarized_dark)

[//]: # (Статистика языков в коммитах:)

[//]: # (Статистика языков в репозиториях:)
![](https://github-profile-summary-cards.vercel.app/api/cards/most-commit-language?username=Maxim-Pekov&theme=solarized_dark)
![](https://github-profile-summary-cards.vercel.app/api/cards/repos-per-language?username=Maxim-Pekov&theme=solarized_dark)


[//]: # (Статистика профиля:)

[//]: # (Данные по коммитам за сутки:)
![](https://github-profile-summary-cards.vercel.app/api/cards/stats?username=Maxim-Pekov&theme=solarized_dark)
![](https://github-profile-summary-cards.vercel.app/api/cards/productive-time?username=Maxim-Pekov&theme=solarized_dark)

[//]: # ([![trophy]&#40;https://github-profile-trophy.vercel.app/?username=Maxim-Pekov&#41;]&#40;https://github.com/ryo-ma/github-profile-trophy&#41;)


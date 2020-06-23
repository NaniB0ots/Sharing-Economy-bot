# Sharing-Economy-bot
Чат бот для поиска объявлений в социальных сетях о безвозмездной передаче еды в рамках проекта 1 МЛН ТОНН
[Ccылка](https://t.me/sharing_economy_bot) на бота в telegram

## Функционал бота:
1. Регистрация пользователя. Реализовано путем записи данных пользователя в базу данных: chat_id, город, указанный при регистрации и категории продуктов 
2. Настройки бота. Пользователь может изенить город, а так же категории продуктов 
3. Получение сообщений о новых постах из групп Вконтакте 
4. Разделение постов (продуктов) на категории, используя нейросеть 

## Cтек разработки:
Python/Django

Основные библиотеки:
  - `Telegram Bot API` - для создания чат бота telegram
  - `tensorflow.keras` - для создания нейросети

## Подготовка среды
Python 3.7/3.8
1. Устанавливаем необходимые библиотеки
  $ pip install - r requirements.txt
2. В файле `SharingEconomybot/settings.py` укажите:
  - `ALLOWED_HOSTS = []` (для запуска сервера в режиме `DEBUG=False`)
  - В самом низу `TG_TOKEN` (Токен бота телеграм)
  - `BOT_HOST` (Хостинг сервера в формате https://test.com/')

## Запуск бота
1. Старт сервера
  $ python manage.py runserver
2. Для запуска бота при `DEBUG=True` перейдитие по ссылке 
   http://127.0.0.1:8000/bot/start

***Код бота находится в файле `/bot/views.py`***


## Запуск парсера 
1. Перейдите по [ссылке](https://colab.research.google.com/drive/1UkBDShocbdq--K2nR6_3agB0poBV3Bfv?usp=sharing) на 
Google Colaboratory
2. Скоприуйте блокнот к себе на гугл диск: `file->Save a copy in Drive`
3. Загрузите фаил с весами модели в бокнот. [Ссылка](https://drive.google.com/file/d/1NvZqCR4VFU9YTzPg-nzKKLBImtz4JyTY/view?usp=sharing) на скачивание файла с весами к себе на компьютер.
![alt text](https://sun1-47.userapi.com/5Svac6I49a_dWBKkNxOatPHvLv3rSC9QKvkxhA/fwenw4bU7Lo.jpg)
![alt text](https://sun1-88.userapi.com/NRu_lkfLyt7dy8VsjvFPPRF7duk5z7bMboq_Pg/-hRYyOzWdgk.jpg)
4. Укажите путь к файлу весов в разделе `Веса модели`
5. Запустите блокнот: `Runtime->Run all` или последовательно запуская каждый скрипт

 ***Копия блокнота Google Colaboratory находится папке `neural_network`***

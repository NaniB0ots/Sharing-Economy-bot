import telebot
import json
import requests
from telebot import types
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render
from django.conf import settings
from time import sleep

from .models import TGUsers
from vk_parser.models import Cities, ProductСategory, VKGroups

from django.views.decorators.csrf import csrf_exempt

bot = telebot.TeleBot(settings.TG_TOKEN, threaded=False)


@csrf_exempt
def webhook(request):
    bot.process_new_updates([telebot.types.Update.de_json(request.body.decode("utf-8"))])
    return HttpResponse(status=200)


def makeInlineKeyboard_chooseCity(status_registration=False, chat_id: int = None):
    cities = Cities.objects.all()
    old_city = ''
    # Если пользователь меняет город в настройках
    if not status_registration:
        if chat_id:
            user = TGUsers.objects.get(chat_id=chat_id)
            old_city = user.city

    markup = types.InlineKeyboardMarkup()
    for city in cities:
        data = json.dumps({"city_id": city.id, "registration": status_registration})
        status = ''
        if city == old_city:  # Если пользователь меняет город в настройках, дописываем ✅ в конец слова
            status = ' ✅'

        markup.add(types.InlineKeyboardButton(text=str(city) + status, callback_data=data))
    return markup


def makeInlineKeyboard_chooseCategory():
    categories = ProductСategory.objects.all()
    markup = types.InlineKeyboardMarkup()
    for cat in categories:
        data = json.dumps({"category_id": cat.id})
        markup.add(types.InlineKeyboardButton(text=str(cat), callback_data=data))
    return markup


def makeReplyKeyboard_main_menu():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn = types.KeyboardButton('Настройки')
    markup.add(btn)
    return markup


def makeInlineKeyboard_setting():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Изменить город', callback_data='edit_city'))
    markup.add(types.InlineKeyboardButton(text='Изменить категории', callback_data='edit_category'))
    markup.add(types.InlineKeyboardButton(text='Закрыть', callback_data='close'))
    return markup


# Команда /start
@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id

    # Если пользователь уже есть в БД, удаляем его
    user = TGUsers.objects.filter(chat_id=chat_id)
    if user:
        user.delete()

    user = TGUsers()
    user.chat_id = chat_id  # Записываем в БД chat_id пользователя
    user.save()

    bot.send_message(chat_id=chat_id,
                     text='Доброго времени суток! Вас приветствует «Фудшеринг-бот». '
                          'Теперь Вам не нужно тратить время на поиск тематических групп и листать объявления, '
                          'в попытке найти актуальное. Чат-бот готов помочь Вам не только в поиске свежих '
                          'объявлений о раздаче еды в Вашем городе, но и может присылать уведомления, '
                          'чтобы Вы не пропустили что-то важное и вкусное')
    bot.send_message(chat_id=chat_id,
                     text='Для того чтобы начать пользоваться моими функциями, пройдите небольшую регистрацию\n'
                          'Выберите город',
                     reply_markup=makeInlineKeyboard_chooseCity(status_registration=True))


# Команда /info
@bot.message_handler(commands=['info'])
def info(message):
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id,
                     text='Краткое описание «Что такое фудшеринг?»\n'
                          'Фудшеринг— это движение, участники которого бесплатно отдают '
                          'или забирают себе еду. Как правило, речь идёт об излишках продуктов, '
                          'иногда — с истекающим сроком годности.\n\n'
                          'Чат бот предназначен для для поиска объявлений в социальных '
                          'сетях о безвозмездной передаче еды в рамках проекта 1 МЛН ТОНН')


# Команда /change_city
@bot.message_handler(commands=['change_city'])
def change_city(message):
    chat_id = message.chat.id

    markup = makeInlineKeyboard_chooseCity(chat_id=chat_id)
    markup.add(types.InlineKeyboardButton(text='Сохранить', callback_data='save'))
    bot.send_message(chat_id=chat_id, text='Изменить город',
                     reply_markup=markup)


# Команда /change_categories
@bot.message_handler(commands=['change_categories'])
def change_categories(message):
    chat_id = message.chat.id

    markup = edit_category(chat_id)
    bot.send_message(chat_id=chat_id, text='Изменить категории',
                     reply_markup=markup)


# Команда /help
@bot.message_handler(commands=['help'])
def help_command(message):
    chat_id = message.chat.id

    bot.send_message(chat_id=chat_id, text='Основные команды:\n'
                                           '/info - что такое Фудшеринг\n'
                                           '/change_city - изменить город\n'
                                           '/change_categories - изменить категории\n'
                                           '/help - список основных команд\n',
                     reply_markup=makeReplyKeyboard_main_menu())


last_data = {}  # Информация о последней нажатой кнопке пользователем


# ==================== Обработка Inline кнопок START ==================== #
@bot.callback_query_handler(func=lambda call: True)
def handle_query(message):
    global last_data
    chat_id = message.message.chat.id
    message_id = message.message.message_id
    data = message.data

    # Проверка что пользователь не нажал одну и ту же кнопку неколько раз (с одной и той же информацией)
    if chat_id in last_data.keys() and data == last_data[chat_id]:
        return
    last_data[chat_id] = data
    print('callback_data:', data)

    # После того как пользователь выбрал город
    if 'city_id' in data:
        data = json.loads(data)

        user = TGUsers.objects.get(chat_id=chat_id)
        city = Cities.objects.get(id=data['city_id'])  # город по id
        user.city = city  # Записываем в БД город пользователя
        user.save()

        if data['registration']:  # Если пользователь проходит регистрацию
            # Выводим сообщение со списком категорий
            markup = makeInlineKeyboard_chooseCategory()
            markup.add(types.InlineKeyboardButton(text='Назад', callback_data='chooseCity'))
            markup.add(types.InlineKeyboardButton(text='➡️ Завершить регистрацию ⬅️', callback_data='end_reg'))
            bot.edit_message_text(message_id=message_id, chat_id=chat_id,
                                  text='Выберите категории продуктов о которых вам будут приходить уведомления\n\n'
                                       'Категории можено будет позже изменить в настройках',
                                  reply_markup=markup)
        else:  # Если пользователь меняет город в настройках
            markup = makeInlineKeyboard_chooseCity(chat_id=chat_id)
            markup.add(types.InlineKeyboardButton(text='Сохранить', callback_data='save'))
            bot.edit_message_reply_markup(message_id=message_id, chat_id=chat_id,
                                          reply_markup=markup)

    # Кнопка назад при выборе категории при регистрации
    elif 'chooseCity' in data:
        user = TGUsers.objects.get(chat_id=chat_id)
        user.city = None  # Записываем в БД город пользователя
        user.save()
        bot.edit_message_text(message_id=message_id, chat_id=chat_id,
                              text='Для того чтобы начать пользоваться моими функциями, '
                                   'пройдите небольшую регистрацию\n'
                                   'Выберите город',
                              reply_markup=makeInlineKeyboard_chooseCity(status_registration=True))

    # При нажатии на категорию
    elif 'category_id' in data:
        data = json.loads(data)
        old_markup = message.message.json['reply_markup']['inline_keyboard']
        markup = types.InlineKeyboardMarkup()

        for item in old_markup:
            callback_data = item[0]['callback_data']
            text = item[0]['text']
            if callback_data == message.data:
                category = ProductСategory.objects.get(id=data['category_id'])
                if text[-1] == '✅':
                    text = text[:-1]
                    user = TGUsers.objects.get(chat_id=chat_id)
                    user.categories.remove(category)  # Удаляем одну категорию
                    user.save()
                else:
                    text += '✅'
                    user = TGUsers.objects.get(chat_id=chat_id)
                    user.categories.add(category)  # Добавляем категорию
                    user.save()
            markup.add(types.InlineKeyboardButton(text=text, callback_data=callback_data))

        bot.edit_message_reply_markup(message_id=message_id, chat_id=chat_id,
                                      reply_markup=markup)
        del last_data[chat_id]

    elif 'end_reg' in data:
        # Проверка, выбрал ли пользователь хоть одну категорию
        user = TGUsers.objects.get(chat_id=chat_id)
        if not user.categories.all():
            bot.send_message(chat_id=chat_id, text='Вы не выбрали ни одной категории!')
            return
        bot.delete_message(message_id=message_id, chat_id=chat_id)
        bot.send_message(chat_id=chat_id, text='Вы успешно завершили регистрацию!😉\n'
                                               'Скоро Вы начнете получать уведомления о новых раздачах\n\n'
                                               'Теперь вам доступны настройки.\n'
                                               'Там можно изменить город и категории продуктов '
                                               'о которых вы хотите получать уведомления')

        bot.send_message(chat_id=chat_id, text='Основные команды:\n'
                                               '/info - что такое Фудшеринг\n'
                                               '/change_city - изменить город\n'
                                               '/change_categories - изменить категории\n'
                                               '/help - список основных команд\n',
                         reply_markup=makeReplyKeyboard_main_menu())
    elif 'edit_category' in data:

        markup = edit_category(chat_id=chat_id)
        bot.edit_message_text(message_id=message_id, chat_id=chat_id, text='Изменить категории',
                              reply_markup=markup)

    elif 'edit_city' in data:
        markup = makeInlineKeyboard_chooseCity(chat_id=chat_id)
        markup.add(types.InlineKeyboardButton(text='Сохранить', callback_data='save'))
        bot.edit_message_text(message_id=message_id, chat_id=chat_id, text='Изменить город',
                              reply_markup=markup)

    elif 'close' in data:
        bot.delete_message(chat_id=chat_id, message_id=message_id)

    elif 'save' in data:
        bot.delete_message(chat_id=chat_id, message_id=message_id)
        bot.send_message(chat_id=chat_id, text='Настройки успешно сохранены')


# ==================== Обработка Inline кнопок END ==================== #
def edit_category(chat_id: int):
    user = TGUsers.objects.get(chat_id=chat_id)
    user_categories = user.categories.all()
    categories = ProductСategory.objects.all()
    markup = types.InlineKeyboardMarkup()

    for cat in categories:
        if cat in user_categories:
            status = ' ✅'
        else:
            status = ''
        callback_data = json.dumps({"category_id": cat.id})
        markup.add(types.InlineKeyboardButton(text=str(cat) + status, callback_data=callback_data))
    markup.add(types.InlineKeyboardButton(text='Сохранить', callback_data='save'))
    return markup


# ==================== Обработка текста START==================== #
@bot.message_handler(content_types=['text'])
def text(message):
    chat_id = message.chat.id
    data = message.text

    if 'Настройки' in data:
        bot.send_message(chat_id=chat_id, text='Настройки ⚙️', reply_markup=makeInlineKeyboard_setting())
    else:
        bot.send_message(chat_id=chat_id, text='Ой, эту информацию люди от меня скрывают.'
                                               'Однако для Вас у меня есть нечто интересное:\n')
        bot.send_message(chat_id=chat_id, text='Основные команды:\n'
                                               '/info - что такое Фудшеринг\n'
                                               '/change_city - изменить город\n'
                                               '/change_categories - изменить категории\n'
                                               '/help - список основных команд\n',
                         reply_markup=makeReplyKeyboard_main_menu())


# ==================== Обработка текста END==================== #

def start_bot(request):
    if settings.DEBUG:
        bot.skip_pending = True
        bot.remove_webhook()
        print('Бот запущен')
        bot.polling(none_stop=True, interval=0)
    else:
        return HttpResponse('DEBUG False')


def get_data_to_parser_from_db(request):
    if request.COOKIES['parser_key'] == '12345678':  # проверяем, что запрос от парсера
        groups = VKGroups.objects.all()
        if groups:
            cities = []
            data = []
            for group in groups:
                for name_city in group.city.all():
                    cities.append(str(name_city))
                data.append(
                    {
                        'title': group.title,
                        'city': cities,
                        'group_id': group.group_id
                    }
                )
            data = json.dumps(data)
            return HttpResponse(data)
    return HttpResponseNotFound


def send_post(request):
    if request.COOKIES['parser_key'] == '12345678':  # проверяем, что запрос от парсера
        post = request.GET
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text='Перейти к посту',
                                         url=post.get('link'))
        markup.add(btn)
        users = TGUsers.objects.all()
        for user in users:
            bot.send_message(chat_id=user.chat_id, text=post.get('category') + '\n' + post.get('link'),
                             reply_markup=markup)

        return HttpResponse('ok')
    else:
        return HttpResponseBadRequest()


# ==================== WEBHOOK ==================== #
if not settings.DEBUG:
    bot.remove_webhook()
    sleep(1)
    bot.set_webhook(url=settings.BOT_HOST + 'bot/' + settings.TG_TOKEN)

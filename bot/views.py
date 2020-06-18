import telebot
import json
from telebot import types
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from time import sleep

from .models import TGUsers
from vk_parser.models import Cities, ProductСategory

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

    bot.send_message(chat_id=chat_id, text='Привет!\nЯ бот для фудшеринга')
    bot.send_message(chat_id=chat_id,
                     text='Для того чтобы начать пользоваться моими функциями, пройдите небольшую регистрацию\n'
                          'Выберите город',
                     reply_markup=makeInlineKeyboard_chooseCity(status_registration=True))


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
    print(data)

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
                                  text='Выберите категории продуктов о которых вам будут приходить уведомления',
                                  reply_markup=markup)
        else:  # Если пользователь меняет город в настройках
            markup = makeInlineKeyboard_chooseCity(chat_id=chat_id)
            markup.add(types.InlineKeyboardButton(text='Сохранить', callback_data='save'))
            bot.edit_message_reply_markup(message_id=message_id, chat_id=chat_id,
                                          reply_markup=markup)

    # Кнопка назад при выборе категории при регистрации
    elif 'chooseCity' in data:
        # Удаляем пользователя из БД
        user = TGUsers.objects.filter(chat_id=chat_id)
        user.delete()
        bot.edit_message_text(message_id=message_id, chat_id=chat_id,
                              text='Для того чтобы начать пользоваться моими функциями, '
                                   'пройдите небольшую регистрацию\n'
                                   'Выберите город',
                              reply_markup=makeInlineKeyboard_chooseCity())

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
        bot.edit_message_text(message_id=message_id, chat_id=chat_id,
                              text='Вы успешно завершили регистрацию!😉\n'
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
        bot.send_message(chat_id=chat_id, text='Настройки успешно изменены')


# ==================== Обработка Inline кнопок END ==================== #


# ==================== Обработка текста START==================== #
@bot.message_handler(content_types=['text'])
def text(message):
    chat_id = message.chat.id
    data = message.text

    if 'Настройки' in data:
        bot.send_message(chat_id=chat_id, text='Настройки ⚙️', reply_markup=makeInlineKeyboard_setting())


# ==================== Обработка текста END==================== #

def start_bot(request):
    if settings.DEBUG:
        bot.skip_pending = True
        bot.remove_webhook()
        print('Бот запущен')
        bot.polling(none_stop=True, interval=0)
    else:
        return HttpResponse('DEBUG False')


# ==================== WEBHOOK ==================== #
if not settings.DEBUG:
    bot.remove_webhook()
    sleep(1)
    bot.set_webhook(url=settings.BOT_HOST + 'bot/' + settings.TG_TOKEN)

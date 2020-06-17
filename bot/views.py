import telebot
import json
from telebot import types
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from time import sleep

from vk_parser.models import Cities

from django.views.decorators.csrf import csrf_exempt

bot = telebot.TeleBot(settings.TG_TOKEN, threaded=False)


@csrf_exempt
def webhook(request):
    bot.process_new_updates([telebot.types.Update.de_json(request.body.decode("utf-8"))])
    return HttpResponse(status=200)


@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id, text='Привет!\nЯ бот для фудшеринга\n\n'
                                           'Основные команды:\n'
                                           '/info - что такое Фудшеринг\n'
                                           '/help - список основных команд\n')
    bot.send_message(chat_id=chat_id,
                     text='Для того чтобы начать пользоваться моими функциями, пройдите небольшую регистрацию\n'
                          'Выберите город',
                     reply_markup=makeInlineKeyboard_chooseCity())


last_data = {}  # Информация о последней нажатой кнопке пользователем


# ==================== Обработка Inline кнопок ==================== #
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

        # Записываем в БД chat_id пользователя
        # Записываем в БД город пользователя

        # Выводим сообщение со списком категорий
        markup = makeInlineKeyboard_chooseCategory()
        markup.add(types.InlineKeyboardButton(text='➡️ Завершить регистрацию ⬅️', callback_data='end_reg'))
        bot.edit_message_text(message_id=message_id, chat_id=chat_id,
                              text='Выберите категории продуктов о которых вам будут и не будут приходить уведомления',
                              reply_markup=markup)


def makeInlineKeyboard_chooseCity():
    cities = Cities.objects.all()
    markup = types.InlineKeyboardMarkup()
    for city in cities:
        data = json.dumps({"city_id": city.id})
        markup.add(types.InlineKeyboardButton(text=str(city), callback_data=data))
    return markup


def makeInlineKeyboard_chooseCategory():
    categories = ['Овощи фрукты, орехи ✅', 'Крупы, макаронные изделия ✅', 'Мясное, рыба ✅', 'Соки, воды ✅',
                  'Хлебобулочные и кондитерские изделия ✅', 'Консервы ✅', 'Алкоголь ✅', 'Молочная продукция ✅',
                  'Готовые блюда ✅']

    markup = types.InlineKeyboardMarkup()
    for category in categories:
        data = json.dumps({"category_id": ''})
        markup.add(types.InlineKeyboardButton(text=category, callback_data=data))
    return markup


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

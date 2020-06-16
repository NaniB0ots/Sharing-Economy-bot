import telebot
import json
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from time import sleep

bot = telebot.TeleBot(settings.TG_TOKEN, threaded=False)


def webhook(request):
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return HttpResponse('ok')


@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id, text='Привет!\nЯ бот для фудшеринга')
    bot.send_message(chat_id=chat_id, text='Основные команды:\n'
                                           '/info - что такое Фудшеринг\n'
                                           '/help - список основных команд\n')
    bot.send_message(chat_id=chat_id,
                     text='Для того чтобы начать пользоваться моими функциями, пройдите небольшую регистрацию')


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

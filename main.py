# -*- coding: utf8 -*-

import config
import telebot
import json
import inspect
from db_manager import DbManager
from telebot import types
from settings import token, ORDER_LIDGEN_ID, CHATBOT_ORDER_CONTROLLER
from client import Client
from menu import Menu
from survey import Survey
from cron import Crons

bot = telebot.TeleBot(token)
crons = Crons()
progressChats = {}


def router(client, **kwargs):
    if '/' in client.message.text and client.message.text.find('/') == 0:
        return False

    if 'callback_data' in kwargs:
        if '/' in kwargs['callback_data'] and kwargs['callback_data'].find('/') == 0:
            return False
        client.message.old_text = client.message.text
        client.message.text = kwargs['callback_data']

    if client.message.text == 'Отменить обучение':
        client.message.chat.old_id = client.message.chat.id
        client.answer['lesson_done'] = False
        client.answer['answer_done'] = False
        client.set_status(status=False, without_text=True)
        client.send_button('Обучение отменено', types.ReplyKeyboardRemove())
        return True

    survey = Survey(message=client.message, client=client)
    if survey.link:
        menu = Menu()
        events = inspect.getmembers(menu, predicate=inspect.ismethod)
        for event in events:
            if 'screen' in event[0] and 'dynamic' in event[0]:
                event[1](get_survey=True, survey=survey)

    if Menu.CANCEL_BUTTON in client.message.text:
        survey.cancel()
        return True
    if survey.is_exist():
        survey.set_answer(text=client.message.text)
        return True

    return False


@bot.message_handler(commands=['home'])
def reactStart(message):
    menu = Menu(message=message)
    menu.redirect('/home')
    crons = Crons()
    # db_manager = DbManager()
    # db_manager.update(table='role_group', where='role_group_id = 4', set='caption = \'Сервис\'')
    # db_manager.update(table='role', where='role_id = 8', set='caption = \'Админ\'')
    # db_manager.update(table='lesson', where='number = 1', set='url = \'https://docs.google.com/spreadsheets/d/1Sj8pcx00r4M7iR6HWz0_ehQJRdbh7SlJTiyjyOyzdKs/edit?usp=sharing\'')
    # db_manager.update(table='lesson', where='number = 2', set='url = \'https://docs.google.com/spreadsheets/d/1VNSqAkSRy7L_qnt6QiGLOtw1NaOZfNPBtEQK8pOl93s/edit?usp=sharing\', name=\'Постановка гипотезы\''  )
    # db_manager.update(table='lesson', where='number = 3', set='url = \'https://docs.google.com/spreadsheets/d/1BihG6nHVxrb8PSSUqrmOZEoAoFDV0smAAvpMgRKbV2E/edit?usp=sharing\', name=\'Делегирование\'')
    # db_manager.update(table='lesson', where='number = 4', set='url = \'https://docs.google.com/spreadsheets/d/1EMQXqULnFcW4SKTqwDBuL-Sa6spj98pDYFcvrCgrbTs/edit?usp=sharing\', name=\'Анализ конкурентов и конкурентная разведка\'' )
    # db_manager.update(table='lesson', where='number = 5', set='url = \'https://docs.google.com/spreadsheets/d/1nJQfawwxgIcVZMMr-ANuUrVcjtCIAgNwteGPT5cM1e8/edit?usp=sharing\', name=\'Работа с целевой аудиторией\'' )
    # db_manager.update(table='lesson', where='number = 6', set='url = \'https://docs.google.com/spreadsheets/d/1NupSRKgkkctvda-E_k35Grnu32FL5GLehM4qSDwKpaA/edit?usp=sharing\', name=\'Трафик\'' )
    # db_manager.update(table='lesson', where='number = 7', set='url = \'https://docs.google.com/spreadsheets/d/1et-TicKoC7pHawEj-JO6Mwl8OJXnGusqHXpfTEa7NYo/edit?usp=sharing\', name=\'Продажи\'' )
    # db_manager.update(table='lesson', where='number = 8', set='url = \'https://docs.google.com/spreadsheets/d/1brm3YIcCsU1w1o729ER6vKwcrGagczAaXu6RGP0YKTU/edit?usp=sharing\', name=\'Аналитика и автоматизация\'' )
    # db_manager.update(table='lesson', where='number = 9', set='url = \'https://docs.google.com/spreadsheets/d/1N0ParGV3Pzq7Tj6p9-CisR84pM2ldfrYGbEB6mlleE0/edit?usp=sharing\', name=\'Поставщики и подрядчики\''  )
    # db_manager.update(table='lesson', where='number = 10', set='url = \'https://docs.google.com/spreadsheets/d/1gbC0jW0hYbCL2tmueUnrc2D6SsTHEqG21t45TVYCoFg/edit?usp=sharing\', name=\'Формирование MVP\'',  )
    # db_manager.update(table='lesson', where='number = 11', set='url = \'https://docs.google.com/spreadsheets/d/1TOPuDKo3bJQ_LO9AJiV8F80vvlYwpXYLomGibvaXzn8/edit?usp=sharing\', name=\'Инвестиционный проект\''  )
    # db_manager.update(table='lesson', where='number = 12', set='url = \'https://docs.google.com/spreadsheets/d/1R5am4mHvN3LdPTnM73egUIGZozR-uvluMY6DAo8xR2c/edit?usp=sharing\', name=\'Запуск компании\'' )
    # db_manager.update(table='lesson', where='number = 13', set='url = \'https://docs.google.com/spreadsheets/d/1pSa40vwup1eS0nmUFThxTYBKqUAdFeo8olo1LboYBgg/edit?usp=sharing\', name=\'Атестация\'' )
    # db_manager.update(table='lesson', where='number = 14', set='url = \'https://docs.google.com/spreadsheets/d/1ivANOIQXAw0XRx7pAkd-Yu6OJNd20JhLTqcOL7A5Dks/edit?usp=sharing\', name=\'Отзывы о курсе\'' )


@bot.message_handler(commands=['help'])
def reactStart(message):
    menu = Menu(message=message)
    menu.redirect('/help')


@bot.message_handler(commands=['start'])
def reactStart(message):
    menu = Menu(message=message)
    params = message.text.split(' ')

    if len(params) > 1:
        if params[1] == 'leadgeneration_invite':
            menu.events('/lidogenerator')
            menu.redirect('/lidogenerator')
            return True
        if params[1] == 'chatbot_develop_invite':
            menu.events('/order_chatbot_develop')
            menu.redirect('/order_chatbot_develop')
            return True

    menu.redirect('/home')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        params = call.data.split('[=_=]')

        if len(params) > 1:
            if Client.SEND_COMMAND in call.data:
                call.message.from_user.username = params[1]
                client = Client(call.message)
                client.send_answer()

            elif Client.VALIDATOR_RIGHT_COMMAND in call.data or Client.VALIDATOR_WRONG_COMMAND in call.data:
                call.message.from_user.username = params[1]
                client = Client(call.message)
                client.message.chat.old_id = client.message.chat.id
                client.message.chat.id = client.user['chat']
                if Client.VALIDATOR_RIGHT_COMMAND in call.data:
                    client.set_status(True)
                    return True
                else:
                    client.set_status(False)
                    return False

            call.message.from_user.username = params[1]
            client = Client(call.message)
            if router(client, callback_data=params[0]):
                return False

            data = Menu().__get_link_list__()
            for i in data:
                if i:
                    if i in call.data:
                        call.message.from_user.username = params[1]
                        menu = Menu(message=call.message)
                        menu.one_screen()
                        menu.events(params[0])
                        menu.redirect(i)
                        break
        else:
            if '/exit' in call.data:
                menu = Menu(message=call.message)
                menu.close()


@bot.message_handler(content_types=['text'])
# @bot.message_handler(func=lambda message: True, content_types=['text'])
# @bot.message_handler(commands=['Следующий урок'])
def reatNext(message):
    client = Client(message)
    if router(client):
        return False
    if client.is_learner():
        if client.NEXT_BUTTON in message.text:
            ky = types.ReplyKeyboardRemove()
            bot.send_message(message.chat.id,'Курс начался', reply_markup=ky)
            client.get_lesson()
        else:
            if client.answer['lesson_done'] and not client.answer['answer_done']:
                client.set_answer()


if __name__ == '__main__':
    bot.polling(none_stop=True)


# -*- coding: utf8 -*-

import telebot
import time
import config
import json
import inspect
from telebot import types
from flask import Flask, render_template, request
from settings import *
from db_manager import DbManager
from google_drive import Sheet, get_column_type_options
from parser import Getuniq
from menu import Menu
from survey import Survey


bot = telebot.TeleBot(token)
app = Flask(__name__)


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
    # if call.message:
    #     params = call.data.split('[=_=]')
    #
    #     if len(params) > 1:
    #         if Client.SEND_COMMAND in call.data:
    #             call.message.from_user.username = params[1]
    #             client = Client(call.message)
    #             client.send_answer()
    #
    #         elif Client.VALIDATOR_RIGHT_COMMAND in call.data or Client.VALIDATOR_WRONG_COMMAND in call.data:
    #             call.message.from_user.username = params[1]
    #             client = Client(call.message)
    #             client.message.chat.old_id = client.message.chat.id
    #             client.message.chat.id = client.user['chat']
    #             if Client.VALIDATOR_RIGHT_COMMAND in call.data:
    #                 client.set_status(True)
    #                 return True
    #             else:
    #                 client.set_status(False)
    #                 return False
    #
    #         call.message.from_user.username = params[1]
    #         client = Client(call.message)
    #         if router(client, callback_data=params[0]):
    #             return False
    #
    #         data = Menu().__get_link_list__()
    #         for i in data:
    #             if i:
    #                 if i in call.data:
    #                     call.message.from_user.username = params[1]
    #                     menu = Menu(message=call.message)
    #                     menu.one_screen()
    #                     menu.events(params[0])
    #                     menu.redirect(i)
    #                     break
    #     else:
    #         if '/exit' in call.data:
    #             menu = Menu(message=call.message)
    #             menu.close()
    pass

@bot.message_handler(content_types=['text'])
# @bot.message_handler(func=lambda message: True, content_types=['text'])
# @bot.message_handler(commands=['Следующий урок'])
def reatNext(message):
    # client = Client(message)
    # if router(client):
    #     return False
    # if client.is_learner():
    #     if client.answer['lesson_done'] and not client.answer['answer_done']:
    #         client.set_answer()
    pass
#--------------
#Работа с ботом
#--------------
@app.route(bot_url + '/run', methods=["POST"])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app.route(bot_url, methods=['GET'])
def webhook():
    bot.remove_webhook()
    time.sleep(0.1)
    bot.set_webhook(url=site_url + bot_url + '/run')
    return "!", 200
#--------------------
#Конец работы с ботом
#--------------------

#------------------------
#Работа с веб интерфейсом
#------------------------

@app.route("/")
def hello():
    return render_template("index.html", title='Accelerator', static=static)


@app.route(result_url, methods=['POST'])
def result():
    id = request.form.get('InvId')
    out_sum = request.form.get('OutSum')
    signature_value = request.form.get('SignatureValue')
    rk = Robokassa(out_sum=out_sum, inv_id=id, checksum=True, signature_value=signature_value)
    verify = rk.verify_response()
    db_manager = DbManager()
    client = Client('', trans_hash=str(id), db_manager=db_manager)

    if client.user['chat']:
        if verify:
            role = db_manager.get_item(table='role', where='name = \'learner\'')

            if role:

                db_manager.update(table='transactions', where='trans_id =' + str(client.tran['trans_id']),
                                  set='is_paid = True, date = now()')
                db_manager.add_additional_role(user_id=str(client.user['user_id']), role_id=role['role_id'])
                client.send(text='Ваш платёж получен. \nВы можете пройти курс выбрав его в меню /home',
                            chat_id=client.user['chat'])

    return render_template("result.html", result_text=str(verify), static=static)


@app.route(google_sheet_column_url, methods=['GET'])
def sheet_column_types():
    types = get_column_type_options()
    result = ''
    i = 0
    for cl_type in types:
        i += 1
        separator = '[=_=]' if i != len(types) else ''
        result += cl_type + separator
    return render_template("api.html", content=result)


@app.route(tarifs_url, methods=['GET'])
def tarifs():
    return render_template("tarifs.html", title='Тарифы', static=static)


@app.route(test_url, methods=['GET'])
def test():
    getuniq = Getuniq(login=GETUNIQ_LOGIN, password=GETUNIQ_PASSWORD).authorization()
    result = getuniq.set_access_vk(user_vk_url='https://vk.com/id312886680')
    result = 'успешно добавлено' if result else 'не добавлено'
    return render_template("test.html", title='Тарифы', content=result, static=static)


@app.route(success_url, methods=['POST'])
def success():
    return render_template("success.html", title='Status', static=static)


@app.route(fail_url, methods=['POST'])
def fail():
    return render_template("fail.html", title='Status', static=static)


# @app.route(get_content_url, methods=['POST'])
# def get_content():
#     if not 'token' in request.form:
#         return render_template("api.html", title='Status', content=str(False))
#
#     # content = Content(token=str(request.form.get('token')))
#
#     # if not content.verify:
#     #     return render_template("api.html", title='Status', content=str(content.verify))
#     #
#     items = ''
#     response = ''
#
#     if not items:
#         response = str(items)
#         return render_template("api.html", title='Status', content=response)
#
#     i = 0
#     for item in items:
#         i += 1
#         separator = '[=_=]' if i < len(items) else ''
#         response += item['key'] + ':::' + item['text'] + separator
#
#     return render_template("api.html", title='Status', content=response)


# @app.route(set_content_url, methods=['POST'])
# def set_content():
#     if not 'token' in request.form:
#         return render_template("api.html", title='Status', content=str(False))
#
#     content = Content(token=str(request.form.get('token')))
#
#     if not content.verify:
#         return render_template("api.html", title='Status', content=str(content.verify))
#
#     api_response = str(request.form.get('response'))
#     api_items = api_response.split('[=_=]')
#     if len(api_items) < 1:
#         return render_template("api.html", title='Status', content=str(False))
#
#     items = []
#     for api_item in api_items:
#         api_content = api_item.split(':::')
#         if len(api_content) > 1:
#             items.append(api_content)
#
#     if not items:
#         return render_template("api.html", title='Status', content=str(False))
#
#     response = content.set_content(items)
#     return render_template("api.html", title='Status', content=str(response))


#------------------------------
#Конец работа с веб интерфейсом
#------------------------------


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
    # bot.polling(none_stop=True)


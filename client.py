# -*- coding: utf8 -*-

import telebot
import hashlib

from db_manager import DbManager
from telebot import types
from settings import *
from google_drive import Sheet
from content import Content

bot = telebot.TeleBot(token)
content = Content(token=GOOGLE_RESPONSE_TOKEN, init_items=True)


class Client:
    SEND_COMMAND = 'senddata'
    VALIDATOR_RIGHT_BUTTON = 'верно'
    VALIDATOR_WRONG_BUTTON = 'не верно'
    VALIDATOR_RIGHT_COMMAND = 'vlr_right'
    VALIDATOR_WRONG_COMMAND = 'vlr_wrong'
    ROLE_LEARNER = 'learner'
    ROLE_VALIDATOR = 'validator'
    ROLE_STARTUP = 'startup'
    ROLE_WORKER = 'worker'
    ROLE_PARTNER = 'partner'
    ROLE_ADMIN = 'admin'
    user = False
    message = False
    role = False
    lesson = False
    answer = False
    tran = False
    question_id = 0
    question_length = 0
    current_lesson = 1

    def __init__(self, message, **kwargs):
        db_manager = kwargs['db_manager'] if 'db_manager' in kwargs else DbManager()
        if message != '':
            self.message = message
            if message.from_user and message.from_user.username:
                login = message.from_user.username

                self.user = db_manager.get_item(table="account", where='login = \'' + login + '\'')
                if not self.authorization_user(db_manager):
                    lesson = db_manager.get_item(table="lesson", where='number = 1')
                    if lesson:
                        self.lesson = lesson
                        if lesson['lesson_id']:
                            db_manager.add_account(login=login, lesson_id=str(lesson['lesson_id']))
                            self.user = db_manager.get_item(table="account", where='login = \'' + login + '\'')
                            if self.authorization_user(db_manager):
                                db_manager.add_answer(answer="  ", lesson_done=str(False), answer_done=str(False),
                                                      user_id=str(self.user['user_id']))

                # db_manager.update(table='lesson', set='questions = \'Как вас зовут? [=_=]Сколько вам лет? [=_=]Из какого вы города? [=_=]Какие у вас компетенции?[=_=]Был ли опыт работы с сотрудниками?[=_=]Был ли опыт делегирования задач фрилансерам?[=_=]Был ли опыт работы с инвесторами? [=_=]Есть ли опыт управления, какой?[=_=]С какими экспретами работали?[=_=]Какие знания есть?[=_=]Цель прохождения данного курса?[=_=]Какой максимальный результат хотите получить от прохождения курса?\'', where='number = 1')
        else:
            if 'trans_hash' in kwargs:
                trans = db_manager.get_items(table='transactions')
                for tran in trans:
                    hash_id = user_encode_key + str(tran['trans_id'])
                    if hash_id == kwargs['trans_hash']:
                        self.tran = tran
                        self.user = db_manager.get_item(table='account', where='user_id =' + str(tran['user_id']))
                        if self.user['chat']:
                            self.authorization_user(db_manager=db_manager)

        if not 'db_manager' in kwargs:
            db_manager.close()

    def authorization_user(self, db_manager):
        if not self.user:
            return False

        if not self.user['chat']:
            self.user['chat'] = self.message.chat.id
            db_manager.update(table='account',
                              set='chat = ' + str(self.user['chat']),
                              where='user_id = ' + str(self.user['user_id']))

        if self.user['role_id']:
            role = db_manager.get_item(table="role", where='role_id = ' + str(self.user['role_id']))
            self.role = role if role else self.role
            if self.is_learner():
                lesson = db_manager.get_item(table="lesson", where='lesson_id = ' + str(self.user['lesson_id']))
                self.lesson = lesson if lesson else self.lesson
                answer = db_manager.get_item(table="user_answer", where='user_id = ' + str(self.user['user_id']))
                self.answer = answer if answer else self.answer

            # if not self.role:
            #     return False

        return True

    def get_lesson(self):
        if self.is_end_lesson():
            self.get_question()
            return False

        if not self.lesson or self.is_answer_send():
            return False

        if self.lesson['number'] < 13:
            caption = 'Урок ' + str(self.lesson['number']) + '. ' + str(self.lesson['name']) + '.'
        else:
            caption = str(self.lesson['name']) + '.'

        self.send(caption)

        sheet = Sheet().open_sheet(sheet_link=self.lesson['url'])
        items = sheet.get_first_list(return_items=True, column='lesson_text')
        questions = sheet.get_first_list(return_items=True, column='lesson_question')
        questions_str = ''
        db_manager = DbManager()

        for item in items:
            self.send(item)

        i = 0
        for question in questions:
            i += 1
            separator = '[=_=]' if i < len(questions) else ''
            questions_str += question + separator

        if self.lesson['questions'] != questions_str:
            db_manager.update(table='lesson',
                              set='questions = \'' + questions_str + '\'',
                              where='lesson_id = ' + str(self.lesson['lesson_id']))
            self.lesson['questions'] = questions_str

        db_manager.update(table='user_answer',
                          set='lesson_done = ' + str(True),
                          where='user_id = ' + str(self.user['user_id']))
        db_manager.close()
        self.get_question()

    def get_question(self):
        if self.is_last_question():
            all_answer = self.get_all_answer()
            if not self.answer['answer_done']:
                buttons = []
                buttons.append(
                    types.InlineKeyboardButton(text=content.load_item('client_send_to_valid'),
                                               callback_data=self.SEND_COMMAND + '[=_=]' + self.user['login']))
                self.send_html_buttons(all_answer, buttons)
            else:
                self.send(content.get_item('client_send_wait_message'))

            return False

        if not self.lesson:
            return False

        questions = self.parse_question()
        btnm = telebot.types.ReplyKeyboardMarkup().row(content.get_item('client_cancel_learning'))
        btnm.resize_keyboard = True
        self.send_button(questions[self.get_question_id()], btnm)

    def get_question_id(self):
        if self.parse_answer() == 0:
            return 0
        return len(self.parse_answer()) - 1

    def get_all_answer(self, **kwargs):
        if not 'parse_answer' in kwargs and not 'question' in kwargs:
            parse_answer = self.parse_answer()
            question = self.parse_question()
        else:
            parse_answer = kwargs['parse_answer']
            question = kwargs['question']

        if parse_answer == 0:
            return False

        result = ''
        j = 0
        for i in parse_answer:
            if j < len(question):
                result += '<b>' + content.load_item('cleint_send_answer_question_caption') + ' ' + str(j+1) + \
                          '. </b>\n' + question[j]  + '\n<b>' + content.get_item('cleint_send_answer_answer_caption') + \
                          '</b>' + i + '\n\n'
                j += 1
        return result

    def get_accounts_by_role(self, role, **kwargs):
        db_manager = DbManager() if not 'db_manager' in kwargs else kwargs['db_manager']

        if not role:
            return False

        accounts = []
        roles = db_manager.get_items(table="account", where='role_id = ' + str(role['role_id']))
        for role in roles:
            accounts.append(role)

        roles = db_manager.query('SELECT account.chat, account.user_id, account.login, account.lesson_id FROM account INNER JOIN user_role_additional ON account.user_id = user_role_additional.user_id AND user_role_additional.role_id = ' + str(role['role_id']))
        for role in roles:
            accounts.append(role)

        return accounts

    def get_role_from_account(self, **kwargs):
        db_manager = DbManager() if not 'db_manager' in kwargs else kwargs['db_manager']
        add_roles = False
        roles = []

        if not 'client' in kwargs:
            if self.role:
                roles.append(self.role['role_id'])

            add_roles = db_manager.get_items(table='user_role_additional', where='user_id =' + str(self.user['user_id']) )
        else:
            user = db_manager.get_item(table='account', where='login = \'' + kwargs['client'] + '\'')
            if user:
                if user['role_id']:
                    roles.append(user['role_id'])
                add_roles = db_manager.get_items(table='user_role_additional',
                                                 where='user_id =' + str(user['user_id']))

        if not add_roles:
            return roles

        for role in add_roles:
            if role['role_id']:
                roles.append( role['role_id'] )

        return roles

    def get_taken_orders(self, **kwargs):
        db_manager = kwargs['db_manager'] if 'db_manager' in kwargs else DbManager()
        return db_manager.query('SELECT * FROM orders INNER JOIN user_order ON user_order.order_id = orders.order_id AND user_order.user_id = ' + str(self.user['user_id']))

    def set_answer(self):
        if self.message.text == "" or self.is_answer_send():
            return False

        self.answer['answer'] = self.answer['answer'] + self.message.text + '[=_=]'
        db_manager = DbManager()
        db_manager.update(table='user_answer',
                          set='answer = \'' + str(self.answer['answer']) + '\'',
                          where='user_id = ' + str(self.user['user_id']))
        db_manager.close()
        self.get_question()

    def set_status(self, status, **kwargs):
        response = content.load_item('client_answer_status_wrong')
        db_manager = DbManager()
        db_manager.update(table='user_answer',
                          set='answer = \' \', lesson_done = ' + str(False) + ', answer_done = ' + str(False),
                          where='user_id = ' + str(self.user['user_id']))
        if status:
            lesson = db_manager.get_item(table="lesson", where='number = ' + str(self.next_lesson()))

            if not lesson:
                db_manager.close()
                return False

            db_manager.update(table='account',
                              set='lesson_id = ' + str(lesson['lesson_id']),
                              where='user_id = ' + str(self.user['user_id']))

            response = content.get_item('client_answer_status_right')

        db_manager.close()
        self.delete()

        if 'without_text' in kwargs:
            if kwargs['without_text']:
                return False

        self.send(content.get_item('client_answer_status_check'))

    def send(self, text, **kwargs):
        if text == '':
            return False
        chat_id = kwargs['chat_id'] if 'chat_id' in kwargs else self.message.chat.id
        bot.send_message(chat_id, text)

    def send_html(self, text):
        if text == '':
            return False
        bot.send_message(self.message.chat.id, text, parse_mode = 'HTML')

    def send_button(self, text, button, **kwargs):
        if text == '':
            return False
        bot.send_message(self.message.chat.id, text, reply_markup=button)

    def send_buttons(self, text, buttons, **kwargs):
        if text == '':
            return False
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*buttons)
        if 'custom_chat' in kwargs:
            bot.send_message(kwargs['custom_chat'], text, reply_markup=keyboard)
        else:
            bot.send_message(self.message.chat.id, text, reply_markup=keyboard)

    def send_html_buttons(self, text, buttons, **kwargs):
        if text == '':
            return False
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*buttons)
        if 'add_keyboard' in kwargs:
            keyboard.add(kwargs['add_keyboard'])
        if 'custom_chat' in kwargs:
            bot.send_message(kwargs['custom_chat'], text, reply_markup=keyboard, parse_mode = 'HTML')
        else:
            bot.send_message(self.message.chat.id, text, reply_markup=keyboard, parse_mode = 'HTML')

    def send_answer(self):
        db_manager = DbManager()

        role = db_manager.get_item(table="role", where='name = \'' + self.ROLE_VALIDATOR + '\'')
        all_answer = self.get_all_answer()

        if not role:
            return False

        if not self.answer['lesson_done']:
            return False

        db_manager.update(table='user_answer',
                          set='answer_done = ' + str(True) ,
                          where='user_id = ' + str(self.user['user_id']))
        db_manager.close()

        self.edit_html(text=all_answer)
        self.send_button(content.load_item('client_send_answer_status_wait'), types.ReplyKeyboardRemove())

        return False

    def edit(self, text):
        bot.edit_message_text(chat_id=self.message.chat.id,  message_id=self.message.message_id, text=text)

    def edit_html(self, text):
        bot.edit_message_text(chat_id=self.message.chat.id, message_id=self.message.message_id, text=text,
                              parse_mode = 'HTML')

    def delete(self):
        bot.delete_message(self.message.chat.old_id, self.message.message_id)

    def parse_question(self):
        return self.lesson['questions'].split('[=_=]')

    def parse_answer(self):
        if not self.answer:
            return 0

        if not '[=_=]' in self.answer['answer']:
            return 0

        return self.answer['answer'].split('[=_=]')

    def is_learner(self):
        if not self.role:
            return False
        return self.role['name'] == self.ROLE_LEARNER

    def is_validator(self):
        if not self.role:
            return False
        return self.role['name'] == self.ROLE_VALIDATOR

    def is_startup(self):
        if not self.role:
            return False
        return self.role['name'] == self.ROLE_STARTUP

    def is_worker(self):
        if not self.role:
            return False
        return self.role['name'] == self.ROLE_WORKER

    def is_partner(self):
        if not self.role:
            return False
        return self.role['name'] == self.ROLE_PARTNER

    def is_last_question(self):
        return self.get_question_id() > len(self.parse_question()) - 1

    def is_end_lesson(self):
        if not self.answer:
            return False
        return self.answer['lesson_done'] if 'lesson_done' in self.answer else False

    def is_answer_send(self):
        if not self.answer:
            return False
        return self.answer['answer_done']

    # надо потом добавить к этому методу чтобы он захдил в базу и смотрел последний урок по базе - номер последнего урока
    def next_lesson(self):
        return 14 if self.lesson['number'] > 13 else self.lesson['number'] + 1
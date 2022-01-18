# -*- coding: utf8 -*-

import telebot
import datetime
from db_manager import DbManager
from settings import token, cron_migrations

bot = telebot.TeleBot(token)


class Cron:
    cron_id = False
    time_stamp = False
    function_name = False
    check_time = False
    db_manager = False

    def __init__(self, **kwargs):
        self.cron_id = kwargs['cron_id'] if 'cron_id' in kwargs else self.cron_id
        self.time_stamp = kwargs['time_stamp'] if 'time_stamp' in kwargs else self.time_stamp
        self.function_name = kwargs['function_name'] if 'function_name' in kwargs else self.function_name
        self.check_time = kwargs['check_time'] if 'check_time' in kwargs else self.check_time
        self.db_manager = kwargs['db_manager'] if 'db_manager' in kwargs else DbManager()
        if str(self.cron_id) in cron_migrations:
            migration = cron_migrations[str(self.cron_id)]['check_time']
            migrations_time = datetime.time(hour=int(migration['hour']),
                                            minute=int(migration['minute']),
                                            second=int(migration['second']))
            set_data = False
            if cron_migrations[str(self.cron_id)]['function_name'] != self.function_name:
                set_data = 'function_name = \'' + cron_migrations[str(self.cron_id)]['function_name'] + '\''
                self.function_name = cron_migrations[str(self.cron_id)]['function_name']

            if migrations_time != self.check_time:
                set_data = ', ' if set_data else ''
                set_data += 'check_time = make_time(' + migration['hour'] + ',' + migration['minute'] + ',' + migration['second'] + ')'
                self.check_time = migrations_time

            if set_data:
                self.db_manager.update(table='cron', where='cron_id =' + str(self.cron_id), set=set_data)

    def check(self, **kwargs):
        if not self.function_name or not self.time_stamp or not self.check_time:
            return False
        now = datetime.datetime.now()
        second = self.get_count_sixteen(self.time_stamp.time().second, self.check_time.second)
        minute = self.get_count_sixteen(self.time_stamp.time().minute, self.check_time.minute)
        hour = self.get_count_sixteen(self.time_stamp.time().hour, self.check_time.hour)
        time = datetime.datetime(year=self.time_stamp.year, month=self.time_stamp.month, day=self.time_stamp.day,
                                 hour=hour['time'] + minute['counter'],
                                 minute=minute['time'],
                                 second=second['time'])

        if now > time:
            self.db_manager.update(table='cron', where='cron_id =' + str(self.cron_id), set='time_stamp = now()')
            return True
        return False

    def get_count_sixteen(self, first_time, second_time):
        result = dict()
        if first_time + second_time > 59:
            result['time'] = first_time + second_time - 60
            result['counter'] = 1
            return result
        result['time'] = first_time + second_time
        result['counter'] = 0
        return result



class Crons:
    items = False
    functions = dict()

    def __init__(self, **kwargs):
        db_manager = kwargs['db_manager'] if 'db_manager' in kwargs else DbManager()
        items = db_manager.get_items(table='cron')
        self.functions['check_transaction'] = check_transaction

        if items:
            self.items = []
            for item in items:
                self.items.append(Cron(cron_id=item['cron_id'], time_stamp=item['time_stamp'],
                                       function_name=item['function_name'], check_time=item['check_time'] ,db_manager=db_manager))
        self.check_crons()

    def check_crons(self):
        if not self.items:
            return False

        for item in self.items:
            if item.check():
                self.functions[item.function_name]()


def check_transaction():
    db_manager = DbManager()
    transactions = db_manager.get_items(table='transactions', where='is_paid = True')
    for transaction in transactions:
        if transaction['type'] == 1:
            date_stamp = transaction['date'] + datetime.timedelta(days=1)
            if date_stamp > datetime.datetime.now():
                role = db_manager.get_item(table='role', where='name = \'learner\'')
                if not role:
                    return False

                db_manager.update(table='transactions', where='trans_id =' + str(transaction['trans_id']),
                                  set='archive = True')

                db_manager.remove(table='user_role_additional',
                                  where='user_id = ' + str(transaction['user_id']) + ' AND role_id =' + str(role['role_id']))
                user = db_manager.get_item(table='account', where='user_id = ' + str(transaction['user_id']))
                if user['role_id'] == role['role_id']:
                    db_manager.update(table='account', where='user_id = ' + str(transaction['user_id']),
                                      set='role_id = NULL')
    # bot.send_message(217974436, 'Крон работает')
    return False
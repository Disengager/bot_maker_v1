# -*- coding: utf8 -*-

import psycopg2
import psycopg2.extras
import urllib.parse as urlparse
import os

class DbManager:
    conn = False
    cursor = False

    def __init__(self):
        url = urlparse.urlparse(os.environ['DATABASE_URL'])
        dbname = url.path[1:]
        user = url.username
        password = url.password
        host = url.hostname
        port = url.port
        conn = psycopg2.connect(dbname=dbname, user=user,
                                password=password, host=host, port=port)
        conn.set_client_encoding('utf-8')
        self.conn = conn
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.cursor = cursor

    def get_item(self, **kwargs):
        if not 'table' in kwargs:
            return False

        if 'where' in kwargs:
            self.cursor.execute('SELECT * FROM "' + kwargs['table']  + '" WHERE ' + kwargs['where'])
        else:
            self.cursor.execute('SELECT * FROM "' + kwargs['table']  + '"')

        result = self.cursor.fetchone()
        return result if result else False

    def get_items(self, **kwargs):
        if not 'table' in kwargs:
            return False

        if 'where' in kwargs:
            self.cursor.execute('SELECT * FROM "' + kwargs['table']  + '" WHERE ' + kwargs['where'])
        else:
            self.cursor.execute('SELECT * FROM "' + kwargs['table']  + '"')

        return self.cursor.fetchall()

    def add_account(self, **kwargs):
        self.cursor.execute('INSERT INTO "account" (login, lesson_id) VALUES (%s, %s)',
                            (kwargs['login'], kwargs['lesson_id']))
        self.conn.commit()

    def add_answer(self, **kwargs):
        self.cursor.execute('INSERT INTO "user_answer" (answer, lesson_done, user_id, answer_done) VALUES (%s, %s, %s, %s)',
                            (kwargs['answer'], kwargs['lesson_done'], kwargs['user_id'], kwargs['answer_done']))
        self.conn.commit()

    def add_lesson(self, **kwargs):
        self.cursor.execute('INSERT INTO "lesson" (name, questions, number) VALUES (%s, %s, %s)',
                            (kwargs['name'], kwargs['questions'], kwargs['number']))
        self.conn.commit()

    def add_survey(self, **kwargs):
        self.cursor.execute('INSERT INTO "survey" (user_id, question, link) VALUES (%s, %s, %s)',
                            (kwargs['user_id'], kwargs['question'], kwargs['link']))
        self.conn.commit()
        return True

    def add_agreement(self, **kwargs):
        self.cursor.execute('INSERT INTO "agreement_lidogenerator" (user_id, answer, register) VALUES (%s, %s, %s)',
                            (kwargs['user_id'], kwargs['answer'], kwargs['register'] ))
        self.conn.commit()

    def add_additional_role(self, **kwargs):
        self.cursor.execute('INSERT INTO "user_role_additional" (user_id, role_id) VALUES (%s, %s)',
                            (kwargs['user_id'], kwargs['role_id']))
        self.conn.commit()

    def add_order(self, **kwargs):
        self.cursor.execute('INSERT INTO "orders" (text, type) VALUES (\'' + kwargs['text'] + '\', ' + str(kwargs['type']) + ')')
        self.conn.commit()

    def add_transaction(self, **kwargs):
        self.cursor.execute('INSERT INTO "transactions" (user_id, description, type, token, price) VALUES (%s, %s, %s, %s, %s)',
                            (kwargs['user_id'], kwargs['description'], kwargs['type'], kwargs['token'], kwargs['out_sum']))
        self.conn.commit()

    def add_user_order(self, **kwargs):
        self.cursor.execute('INSERT INTO "user_order" (user_id, order_id) VALUES (%s, %s)',
                            (kwargs['user_id'], kwargs['order_id']))
        self.conn.commit()

    def add_content(self, **kwargs):
        self.cursor.execute('INSERT INTO "content" (key, text) VALUES (%s, %s)',
                            (kwargs['key'], kwargs['text']))
        self.conn.commit()

    def update(self, **kwargs):
        if not 'set' in kwargs or not 'table' in kwargs:
           return False
        self.cursor.execute('UPDATE "' + kwargs['table'] + '" SET ' + kwargs['set'] + ( ' WHERE ' + kwargs['where'] if 'where' in kwargs else ''))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def query(self, text):
        self.cursor.execute(text)
        return self.cursor.fetchall()

    def remove(self, **kwargs):
        if not 'table' in kwargs and not 'where' in kwargs:
            return False
        self.cursor.execute('DELETE FROM "' + kwargs['table'] + '" WHERE ' + kwargs['where'])
        self.conn.commit()
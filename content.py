# -*- coding: utf8 -*-

from settings import GOOGLE_RESPONSE_TOKEN
from db_manager import DbManager


class Content:
    verify = False
    items = False

    def __init__(self, **kwargs):
        if 'token' in kwargs:
            self.set_verify(kwargs['token'])
        if 'init_items' in kwargs:
            self.items = self.get_translate_items()

    def get_content(self, **kwargs):
        content = self.get_items(kwargs)

        if not content:
            return False

        if 'key' in kwargs:
            content = self.transform_content(content)
            if not kwargs['key'] in content:
                return False
            return content[kwargs['key']]

        return content

    def get_items(self, params):
        if params and 'key' in params:
            return DbManager().get_item(table='content', where='key = \'' + params['key'] + '\'')

        return DbManager().get_items(table='content')

    def load_item(self, key, **kwargs):
        self.get_translate_items()
        return self.get_item(key)

    def get_item(self, key):
        if not key in self.items:
            return 'Панель'
        return self.items[key]

    def get_translate_items(self):
        self.items = self.transform_content(content=self.get_content())
        return self.items

    def set_verify(self, token):
        self.verify = token == GOOGLE_RESPONSE_TOKEN

    def set_content(self, items):
        if not self.verify:
            return False

        if len(items) < 1:
            return False

        content = self.get_items(False)
        db_manager = DbManager()

        if not content:
            for item in items:
                db_manager.add_content(key=item[0], text=item[1])
            return True

        content = self.transform_content(content)
        is_update = False

        for item in items:
            if item[0] in content:
                if item[1] != content[item[0]]:
                    db_manager.update(table='content', where='key = \'' + item[0] + '\'', set='text = \'' + item[1] + '\'')
                    is_update = True
            else:
                db_manager.add_content(key=item[0], text=item[1])
                is_update = True

        db_manager.close()
        return is_update

    def transform_content(self, content):
        result = dict()
        for item in content:
            result[item['key']] = item['text']

        return result

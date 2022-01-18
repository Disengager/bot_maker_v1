# -*- coding: utf8 -*-

import hashlib
from settings import *


class Robokassa:
    LINK_BASE = 'https://auth.robokassa.ru/Merchant/Index.aspx?MerchantLogin=' + merchant_login
    passwords = rk_passwords
    merchant_login = merchant_login
    out_sum = False
    inv_id = False
    signature_value = False  # закодирование в мд5 значение сигнатуры, если робокасса иницализируется для проверки пришедшего кода то синатура идёт из полученных данных
    link = False

    def __init__(self, **kwargs):
        self.out_sum = kwargs['out_sum'] if 'out_sum' in kwargs else self.out_sum

        if 'inv_id' in kwargs:
            self.inv_id = kwargs['inv_id']
            if not 'checksum' in kwargs:
                self.inv_id = user_encode_key + str(self.inv_id)

        self.signature_value = kwargs['signature_value'] if 'signature_value' in kwargs else self.signature_value
        self.link = kwargs['link'] if 'link' in kwargs else self.link

    def generate_link(self, **kwargs):
        if not self.out_sum or not self.inv_id:
            return False

        out_sum = str(self.out_sum)
        inv_id = str(self.inv_id)
        link = '&InvId=' + inv_id + '&Culture=ru&Encoding=utf-8&OutSum=' + out_sum + '&SignatureValue=' \
               + self.encode_signature() + '&IsTest=1'
        self.link = self.LINK_BASE + link
        return self.link

    def verify_response(self, **kwargs):
        if not self.verify_signature(signature=self.signature_value):
            if 'wrong_function' in kwargs:
                kwargs['wrong_function'](
                    self.inv_id)  # функция активируется если проверка не состоялась - на случай если нужно отослать пользователю какое-то сообщение
            return self.get_wrong_status()

        if 'right_function' in kwargs:  # функция активирутся если результат проверки был успешный - на случай если нужно что то добавить в базу
            kwargs['right_function'](self.inv_id)

        return self.get_right_status()

    def get_right_status(self):
        return 'OK' + str(self.inv_id)

    def get_wrong_status(self):
        return False

    def encode_signature(self, **kwargs):
        password = rk_passwords['1']
        merchant = self.merchant_login + rk_separator
        inv_id = str(self.inv_id) if self.inv_id else ''

        if 'checksum' in kwargs and kwargs['checksum']:
            password = rk_passwords['2']
            merchant = ''

        encode_string = merchant + str(self.out_sum) + rk_separator + inv_id + rk_separator + password

        if 'add' in kwargs:
            encode_string += str(kwargs['add'])

        return hashlib.md5(encode_string.encode()).hexdigest()

    def verify_signature(self, **kwargs):
        if not 'signature' in kwargs:
            return False
        return kwargs['signature'].upper() == self.encode_signature(checksum=True).upper()

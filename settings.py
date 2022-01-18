# -*- coding: utf8 -*-

# app settings
static = '/static/'
result_url = '/payment/rk/order/result'
success_url = '/payment/success'
fail_url = '/payment/fail'
tarifs_url = '/tarifs'
test_url = '/test'
google_sheet_column_url = '/google/sheet/column/type'
get_content_url = '/google/sheet/content/get/get_content'
set_content_url = '/google/sheet/content/set/get_content'
bot_url = '/GQY1o7VGknO4hPedCZdp9pXGV7'
site_url = 'link'

# telegram bot settings
token = 'token'


merchant_login = 'login'

links = dict()
links['learner_1'] = ''

# tech suppport
CHATBOT_ORDER_CONTROLLER = 'chatid'
GETUNIQ_CONTROLLER = 'chatid'

# google drive
ANSWER_TYPE_FREE = 'ответ в свободной форме'
ANSWER_TYPE_OK = 'кнопка ок'
GOOGLE_RESPONSE_TOKEN = ''

#cron settings
cron_migrations = dict()
cron_migrations['1'] = dict()
cron_migrations['1']['function_name'] = 'check_transaction'
cron_migrations['1']['check_time'] = dict()
cron_migrations['1']['check_time']['hour'] = '0'
cron_migrations['1']['check_time']['minute'] = '16'
cron_migrations['1']['check_time']['second'] = '0'

#orders
ORDER_LIDGEN_ID = 1
ORDER_LIDGEN_NAME = 'lidogeneration'
ORDER_CHATBOT_ID = 2
ORDER_CHATBOT_NAME = 'chat_bot_develop'
ORDER_TYPE = [
    (ORDER_LIDGEN_ID, ORDER_LIDGEN_NAME),
    (ORDER_CHATBOT_ID, ORDER_CHATBOT_NAME)
]

#parser
#getuniq
GETUNIQ_LOGIN = ''
GETUNIQ_PASSWORD = ''
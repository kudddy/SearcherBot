from random import randint
from json import load
from os import environ


jenkins: bool = True

if jenkins:
    url_fasttext = environ['url_fasttext']
    token_fastext = environ['token_fastext']
    server_memcached = environ['server_memcached']
    bot_token = environ['bot_token']
else:
    with open('Cache/files/cnfg.json') as json_file:
        data: dict = load(json_file)

    url_fasttext: str = data['url_fasttext']
    token_fastext: str = data['token_fastext']
    server_memcached: str = data['server_memcached']
    bot_token: str = data['bot_token']

url_send_message: str = """https://api.telegram.org/bot{}/sendMessage""".format(bot_token)
index_filename: str = 'Cache/files/index_cache.p'
vacs_filename: str = 'Cache/files/struct_actual_vac.pickle'
vacancy_url: str = "https://my.sbertalents.ru/#/job-requisition/{}"

# константы работы движка

time_for_update_index: int = 60*60*6

time_for_sleep_sheduller: int = 60*60*12

timeout_for_chat: int = 300

timeout_for_chat_test: int = 5

unique_quid_app: int = randint(0, 10000)






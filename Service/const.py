from random import randint
from json import load

with open('Cache/files/cnfg.json') as json_file:
    data = load(json_file)

url_fasttext = data['url_fasttext']
token_fastext = data['token_fastext']
server_memcached = data['server_memcached']
bot_token = data['bot_token']

url_send_message = """https://api.telegram.org/bot{}/sendMessage""".format(bot_token)
index_filename = 'Cache/files/index_cache.p'
vacs_filename = 'Cache/files/struct_actual_vac.pickle'
vacancy_url = "https://my.sbertalents.ru/#/job-requisition/{}"

# константы работы движка

time_for_update_index = 60*60*6

time_for_sleep_sheduller = 60*60*12

timeout_for_chat = 300

timeout_for_chat_test = 5

unique_quid_app = randint(0, 10000)






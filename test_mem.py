from pymemcache.client import base

# # Не забудьте запустить memcached перед запуском следующей строки:
# client = base.Client(('localhost', 11211))
#
# # После того как клиент инстанцирован, вы можете получить доступ к кэшу:
# client.set('some_key', 'some value')
#
# # # Получаем установленные ранее данные еще раз:
# client.get('some_key') # 'some value'
# #
# # print(result)

# import memcache
# from time import sleep
#
# mc = memcache.Client(['127.0.0.1:11211'], debug=0)
# mc.set("1", "Some value", time=1)
#
# sleep(2)
# value = mc.get("1")
#
# # print(value)
#
# if value:
#     print(value)
# else:
#     print('нихуя')
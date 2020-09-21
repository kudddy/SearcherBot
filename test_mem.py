from pymemcache.client import base

# # Не забудьте запустить memcached перед запуском следующей строки:
# client = base.Client(("localhost", 11211))
#
# # После того как клиент инстанцирован, вы можете получить доступ к кэшу:
# client.set("some_key", "some value")
#
# # # Получаем установленные ранее данные еще раз:
# client.get("some_key") # "some value"
# #
# # print(result)

# import memcache
# from time import sleep
#
# mc = memcache.Client(["127.0.0.1:11211"], debug=True)
# mc.set("1", ["Some value", "SomeVal", "Val"])
# mc.set("2", ["Some value", "SomeVal", "Val"])
# mc.set("3", {"лол": "лол"})
#
# value = mc.get("1")
#
# value = mc.get("3")
#
# print(value)
#
# print(type(value))
#
# values: dict = mc.get_multi(["0", "2"])
#
# one, two = values.get("0"), values.get("2")
#
# print(one)
# print(two)
#
# # print(values)
#
# # print(value)
#
# if value:
#     print(value)
# else:
#     print("нихуя")
# mc.flush_all()
# values: dict = mc.get_multi(["0", "2"])
# one, two = values.get("0"), values.get("2")
# print(one)
# print(two)


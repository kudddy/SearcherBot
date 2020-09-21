from typing import List

from Service.validform import Updater
from db.schema import mc
from Service.const import timeout_for_chat


class Stages:
    def __init__(self, stages):
        self.stages = stages

    @property
    def k_iter(self):
        return len(self.stages) - 1

    def next(self, m: Updater) -> None:
        """
        Ф-ция занимается маршрутизацией и вызовом коллбэк функций
        :param m: сообщение от Telegram
        :return: None
        """
        if m.message:
            chat_id = str(m.message.chat.id)
        else:
            chat_id = str(m.callback_query.message.chat.id)
        key = mc.get(chat_id)
        if key:
            key = int(key)
        else:
            key = 0

        step = self.stages[key].__call__(m)

        mc.set(chat_id, str(step), time=timeout_for_chat)


class LocalCacheForCallbackFunc:
    def __init__(self):
        self.cache_vacancy_result = {}
        self.cache_iter = {}

    def caching(self, chat_id: int, step: int, arr: List[int]) -> None:
        self.cache_iter[chat_id] = step
        self.cache_vacancy_result[chat_id] = arr

    def give_cache(self, chat_id: int) -> int or False:
        if chat_id in self.cache_iter and chat_id in self.cache_vacancy_result:
            try:
                return self.cache_vacancy_result[chat_id][self.cache_iter[chat_id]]
            except IndexError as e:
                return False
        else:
            return False

    def check(self, chat_id: int) -> bool:
        if chat_id in self.cache_iter:
            return True
        else:
            return False

    def clean(self, chat_id: int) -> None:
        if chat_id in self.cache_iter and chat_id in self.cache_vacancy_result:
            self.cache_iter.pop(chat_id, None)
            self.cache_vacancy_result.pop(chat_id, None)

    def next_step(self, chat_id: int) -> None:
        self.cache_iter[chat_id] += 1

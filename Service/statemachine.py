from datetime import datetime

from typing import List

from Service.validform import Updater


class Stages:
    def __init__(self, stages):
        self.stages = stages
        self.cache = {}
        self.cache_time = {}
        self.last_date = datetime.now()

    @property
    def k_iter(self):
        return len(self.stages) - 1

    def next(self, m: Updater) -> None:
        if m.message.chat.id not in self.cache:
            self.reset_all(m.message.chat.id)
            self.cache_time[m.message.chat.id].append(datetime.now())

        self.cache_time[m.message.chat.id].append(datetime.now())

        elapsed = self.cache_time[m.message.chat.id][-1] - self.cache_time[m.message.chat.id][-2]

        if divmod(elapsed.total_seconds(), 60)[1] > 15:
            self.reset_all(m.message.chat.id)
            self.cache_time[m.message.chat.id].append(datetime.now())

        step = self.stages[self.cache[m.message.chat.id]].__call__(m)
        self.cache[m.message.chat.id] = step

    def reset_cache_key(self, key: str or int) -> None:
        self.cache[key] = 0

    def reset_cache_time(self, key: str or int) -> None:
        self.cache_time[key] = []

    def reset_all(self, key: str or int) -> None:
        self.cache[key] = 0
        self.cache_time[key] = []

    def next_key(self, key: str or int):
        self.cache[key] = self.cache[key] + 1


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

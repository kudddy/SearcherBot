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
            step = int(key['step'])
        else:
            step = 0

        step = self.stages[step].__call__(m)

        key = mc.get(chat_id)

        if key:
            key['step'] = step
        else:
            key = {'step': step}

        mc.set(chat_id, key, time=timeout_for_chat)


class LocalCacheForCallbackFunc:

    @staticmethod
    def caching(chat_id: int, step: int, arr: List[int]) -> None:

        chat_id = str(chat_id)
        val = mc.get(chat_id)

        val['cache_vacancy_result'] = arr
        val['cache_iter'] = step

        mc.set(chat_id, val)

    @staticmethod
    def give_cache(chat_id: int) -> int or False:
        chat_id = str(chat_id)

        val = mc.get(chat_id)

        if val:
            try:
                return val['cache_vacancy_result'][val['cache_iter']]
            except IndexError as e:
                return False
        else:
            return False

    @staticmethod
    def check(chat_id: int) -> bool:
        val = mc.get(str(chat_id))
        if 'cache_iter' in val:
            return True
        else:
            return False

    @staticmethod
    def clean(chat_id: int) -> None:
        val = mc.get(str(chat_id))
        if val:
            mc.delete(str(chat_id))

    @staticmethod
    def next_step(chat_id: int) -> None:
        val = mc.get(str(chat_id))
        val['cache_iter'] += 1
        mc.set(str(chat_id), val)

from Service.const import url_send_message
from Service.helper import send_message
from Service.validform import Updater
from Service.statemachine import LocalCacheForCallbackFunc
from Service.const import vacancy_url
from Service.const import url_fasttext, token_fastext, time_for_update_index, unique_quid_app

from SearchEngine.EasySearchEngine import InversIndexSearch
from ext.helper import GetVac, remove_html_in_dict, pcl
from Cache.cache import vacs_filename, index_filename
from db.schema import mc


# инициализируем класс с вакансиями
vacs = GetVac(vacs_filename=vacs_filename)
# инициализируем поисковой движок
search = InversIndexSearch(url=url_fasttext, token=token_fastext)

# инициализируем класс с кэшем только для коллбэк ф-ций
cache = LocalCacheForCallbackFunc()


def hello_message(m: Updater):
    """
    Приветственное сообщение с просьбой указать навык
    :param m: Входящее сообщение
    :return: ключ колбэк ф-ции, которую нужно вызвать
    """
    if m.message:
        cache.clean(m.message.chat.id)
    else:
        cache.clean(m.callback_query.message.chat.id)

    # процедура для обновления кэша
    key = mc.get("key_for_update_{}".format(str(unique_quid_app)))
    if key is None:
        search.cache_index = pcl.get_pickle_file(index_filename)
        vacs.vacs = pcl.get_pickle_file(vacs_filename)
        mc.set("key_for_update_{}".format(str(unique_quid_app)), "True", time=time_for_update_index)

    text = "💥 Приветствую, я найду для тебя работу. Введите ключевые слова❗"
    send_message(url_send_message, m.message.chat.id, text, remove_keyboard=True)
    return 1


def analyze_text_and_give_vacancy(m: Updater):
    """

    :param m: Входящее сообщение
    :return: ключ колбэк ф-ции, которую нужно вызвать
    """
    if m.message.text != 'Нет':
        if cache.check(m.message.chat.id):
            cache.next_step(m.message.chat.id)
        else:
            result: list = search.search(m.message.text)
            step = 0
            cache.caching(m.message.chat.id, step=step, arr=result)
        vac_id = cache.give_cache(m.message.chat.id)
        vacancy_info: dict = vacs.get_vac_by_id(vac_id)
        if vacancy_info:
            title: str = "💥 Название позиции: " + vacancy_info['content']['title'] + '\n'
            text: str = title + "💥 Описание: " + vacancy_info['content']['header'] + '\n' + vacancy_url.format(str(vac_id))
            text: str = text + '\n' "Показать еще❓"
            send_message(url_send_message, m.message.chat.id,
                         remove_html_in_dict(text)[:4095],
                         buttons=['Да', 'Нет'],
                         one_time_keyboard=False)
            return 1
        else:
            text = '🤓 К сожалению, вакансий больше нет❗️'
            send_message(url_send_message, m.message.chat.id, text, remove_keyboard=True)
            return 0

    else:
        text = '💥 Пока, возвращайся еще❗️'
        send_message(url_send_message, m.message.chat.id, text, remove_keyboard=True)
        return 0


def goodbye_message(m: Updater):
    text = '💥 Пока, возвращайся еще❗️'
    send_message(url_send_message, m.message.chat.id, text, remove_keyboard=True)
    return 0

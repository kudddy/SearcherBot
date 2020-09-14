from Service.const import url_send_message
from Service.helper import send_message
from Service.validform import Updater
from SearchEngine.EasySearchEngine import InversIndexSearch
from Service.statemachine import LocalCacheForCallbackFunc
from ext.helper import GetVac, remove_html_in_dict
from Cache.cache import vacs_filename

from db.query import VACANCY_QUERY
from db.schema import vacancy_info_table
from db.schema import conn

# инициализируем класс с вакансиями

vac = GetVac(vacs_filename)

# инициализируем поисковой движок
search = InversIndexSearch(url="104.154.103.236:8080/FastTextAsServer", token="dkhfklsdhflksdhflksdhf43934")

# инициализируем класс с кэшем только для коллбэк ф-ций
cache = LocalCacheForCallbackFunc()


def hello_message(m: Updater):
    """
    Приветственное сообщение с просьбой указать навык
    :param m: Входящее сообщение
    :return: ключ колбэк ф-ции, которую нужно вызвать
    """
    cache.clean(m.message.chat.id)
    text = "Приветствую, я найду для тебя работу. Введите ключевые слова!"
    send_message(url_send_message, m.message.chat.id, text)
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
            result: list = search.search(m.message.text)[0:10]
            step = 0
            cache.caching(m.message.chat.id, step=step, arr=result)
        # TODO записать в базу vacancy_id в int а не в str
        insert_statement = VACANCY_QUERY.where(vacancy_info_table.c.vacancy_id == str(cache.give_cache(m.message.chat.id)))
        try:
            raw_title, raw_vac_text = list(conn.execute(insert_statement))[0]
            vacancy_info = True
        except Exception as e:
            print(e)
            vacancy_info = False

        if vacancy_info:
            title: str = raw_title + '\n'
            text: str = title + raw_vac_text
            send_message(url_send_message, m.message.chat.id, remove_html_in_dict(text)[:4095], buttons=['Да', 'Нет'])
            return 1
        else:
            text = 'К сожалению, вакансий больше нет!'
            send_message(url_send_message, m.message.chat.id, text, remove_keyboard=True)
            return 0

    else:
        text = 'Пока, возвращайся еще!'
        send_message(url_send_message, m.message.chat.id, text)
        return 0


def goodbye_message(m: Updater):
    text = 'Пока, возвращайся еще!'
    send_message(url_send_message, m.message.chat.id, text)
    return 0

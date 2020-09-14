#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import logging
import os
import re
import sys
from collections import defaultdict, Iterable
from time import sleep

import requests

from ext.pickler import Pickler as pcl


def split_dict_equally(input_dict, chunks=2):
    """
    Разделение словаря на n частей. Возвращает лист из словарей.
    Аrgs:
        type(dict) - input_dict : словарь с любым типом данных
        type(int) - chunks : размер выходного списка
    Returns:
        type(list) - return_list : список с словарями
    """
    # prep with empty dicts
    return_list = [dict() for idx in range(chunks)]
    idx = 0
    for k, v in input_dict.items():
        return_list[idx][k] = v
        if idx < chunks - 1:  # indexes start at 0
            idx += 1
        else:
            idx = 0
    return return_list


def func(*dicts):
    """
    Объединяет словари по ключа. Работает только со строками
    Аrgs:
        type(dict) - input_dict : словари
    Returns:
        type(list) - return_list : список с словарями
    """
    keys = set().union(*dicts)
    return {k: " ".join(dic.get(k, '') for dic in dicts) for k in keys}


def check_updates(recs_new, recs_old):
    """
    В случае если старые и новые рекомендации разные,то возвращаем True, если же одинаковые то
    False
    Аrgs:
        type(list) - recs_new : список с новыми рекомендациями
        type(list) - recs_old : строка c sf_id
    Returns:
        type(list) - jc : список с актуальными jc
    """
    len_intersect = len(set(recs_old).intersection(set(recs_new)))

    len_old_rec = len(recs_old)

    if len_intersect == len_old_rec and recs_old == recs_new:
        return False
    else:
        return True


def get_score(recs_new):
    """
    Ф-ция возвращает искуственно созданных скор для рекомендаций в зависимости от кол-ва новых рекомендаций
    Аrgs:
        type(list) - recs_new : список с новыми рекомендациями
    Returns:
        type(list) - score : список со скором
    """
    len_recs = len(recs_new)
    min_trash = 0.6
    max_trash = 0.95
    score = []
    error = 0
    for i in range(len(recs_new)):
        error += (max_trash - min_trash) / len_recs
        score.append(str(max_trash - error))
    return score


def group_by_value(dct):
    """
    Группируем ключ по значениям
    Аrgs:
        type(dict) - input_dict : словарь с любым типом данных
        type(int) - chunks : размер выходного списка
    Returns:
        type(list) - return_list : список с словарями
    """
    v = {}
    for key, value in sorted(dct.items()):
        v.setdefault(value, []).append(key)
    return v


def group_tuples_by_key(tuples):
    """
    Ф-ция возвращает сгруппированный по ключу словарь
    Аrgs:
        type(list((key,val),(key,val))) - tuples : список с кортежами
    Returns:
        type(dict) - score : сгруппированный по ключу словарь
    """
    d = defaultdict(list)
    for k, *v in tuples:
        d[k].append(v[0])
    b = list(d.items())
    return dict(b)


def add_list(main_list, new_list):
    """
    Ф-ция добавляет в начала списка main_list список new_list
    Аrgs:
        type(list) - main_list : основной список с элементами
        type(list) - bad_list : список элементов, которые нужно удалить из основного списка
    Returns:
        type(list) - new_list : новый список
    """
    return new_list + main_list


def diff_no_mutation(main_list, bad_list):
    """
    Ф-ция возвращает список элементов main_list которых нет в bad_list
    Аrgs:
        type(list) - main_list : основной список с элементами
        type(list) - bad_list : список элементов, которые нужно удалить из основного списка
    Returns:
        type(list) - clean_list : очищенный список
    """
    clean_list = [x for x in main_list if x not in bad_list]
    return clean_list


def drop_dublicates_list(seq):
    """
    Удаляем дубликаты из списка
    Аrgs:
        type(list) - seq : основной список с элементами
    Returns:
        type(list) - clean_list : список без дубликатов
    """
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def chunks(array, chunk_size):
    """
    Ф-ция возвращает сгруппированный по ключу словарь. Ф-цию нужно обернуть в list()
    Аrgs:
        type(list)- array : список
        type(int) - chunk_size : коэф от которого зависит какой размер батча
    Returns:
        n/a
    """
    for i in range(0, len(array), chunk_size):
        yield array[i:i + chunk_size]


class NTLogger:
    def __init__(self, context, verbose):
        self.context = context
        self.verbose = verbose

    def info(self, msg, **kwargs):
        print('I:%s:%s' % (self.context, msg), flush=True)

    def debug(self, msg, **kwargs):
        if self.verbose:
            print('D:%s:%s' % (self.context, msg), flush=True)

    def error(self, msg, **kwargs):
        print('E:%s:%s' % (self.context, msg), flush=True)

    def warning(self, msg, **kwargs):
        print('W:%s:%s' % (self.context, msg), flush=True)


def set_logger(context, verbose=False):
    logger = logging.getLogger(context)
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s:%(levelname)-s:' + context + ':[%(filename)s:%(funcName)s:%(lineno)3d]:%(message)s', datefmt=
        '%Y-%m-%d %H:%M:%S')
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    console_handler.setFormatter(formatter)
    logger.handlers = []

    logger.addHandler(console_handler)

    fh = logging.FileHandler('vac_bot_logs.log')
    fh.setLevel(logging.DEBUG if verbose else logging.INFO)
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    return logger


def create_tunnel_to_hana():
    """
    Акстивация соединения с базой данных
    :return:
        conn_hana (:obj:'object'): Конфигуратор соединения с базой данных
    """
    path = os.path.abspath(os.path.dirname('__file__'))
    path_to_tool = os.path.join(path, 'installers', 'hana_t2', 'tools')
    if os.name == 'nt':
        import subprocess
        p = subprocess.Popen(os.path.join(path_to_tool, 'connect_to_HANA_Prom.cmd'),
                             creationflags=subprocess.CREATE_NEW_CONSOLE, cwd=path_to_tool)
    else:
        from subprocess import call
        comand = ''
        call(comand, shell=True)
    sleep(60)
    con_hana = None
    return con_hana


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


class safesub(dict):
    def __missing__(self, key):
        return '{' + key + '}'


def sub(text):
    return text.format_map(safesub(sys._getframe(1).f_locals))


def flatten(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            yield from (flatten(x))
        else:
            yield x


class TunnelCreator:
    def __init__(self):
        self.incement = 0
        self.max_depth = 10

    def create_tunnel_to_hana(self):
        """
        Акстивация соединения с базой данных
        :return:
            conn_hana (:obj:'object'): Конфигуратор соединения с базой данных
        """
        if self.max_depth > self.incement:
            path = os.path.abspath(os.path.dirname('__file__'))
            path_to_tool = os.path.join(path, 'installers', 'hana_t2', 'tools')
            if os.name == 'nt':
                import subprocess
                p = subprocess.Popen(os.path.join(path_to_tool, 'connect_to_HANA_Prom.cmd'),
                                     creationflags=subprocess.CREATE_NEW_CONSOLE, cwd=path_to_tool)
            else:
                from subprocess import call
                comand = ''
                call(comand, shell=True)
            # ждем пока туннель запустится
            sleep(60)
            try:
                con_hana = None
                return con_hana
            except Exception as e:
                print(str(e))
                # засыпаем перед следующей попыткой
                sleep(30)
                self.incement = self.incement + 1
                return self.create_tunnel_to_hana()

        else:
            self.incement = 0
            return -1


def structure_normalization(d: list) -> dict:
    """
    Нормализация структуры данных, которая приходит из JobApi
    :param d:
    :return:
    """
    local_dict = {}
    for k in d:
        local_dict.update({k['id']: k})
    return local_dict


class GetVac:
    def __init__(self, vacs_filename):
        self.vacs = pcl.get_pickle_file(vacs_filename)

    def get_vac_by_id(self, key: int):
        if key in self.vacs.keys():
            return self.vacs[key]
        else:
            return False

    def update_cache(self, new_cache):
        self.vacs = new_cache


def remove_html_in_dict(text):
    html_pattern = re.compile('<.*?>')
    title_pattern = re.compile(r'([a-zа-я](?=[A-ZА-Я])|[A-ZА-Я](?=[A-ZА-Я][a-zа-я]))')

    val = title_pattern.sub(r'\1 ', html_pattern.sub(r'', text).replace('\xa0', ' '))
    text = re.sub(r'&[\w]*;', ' ', val).strip()
    return text


def get_clean_text_str(text_vacs: dict) -> str:
    """
    Ф-ция необходима для процедуры токенизации. Преобразует данные из словаря в единую строку
    :param text_vacs: словарь с описанием вакансии
    :return: единая строка содержащая в себе поля
    """
    if 'title' in text_vacs.keys():
        title = remove_html_in_dict(text_vacs['title'])
    else:
        title = 'fail'

    # обязанности
    if 'duties' in text_vacs.keys():
        duties_text = remove_html_in_dict(text_vacs['duties'])
    else:
        duties_text = 'fail'

    # условия
    if 'conditions' in text_vacs.keys():
        # conditions_text = remove_html_in_dict(text_vacs['conditions'])
        conditions_text = 'fail'
    else:
        conditions_text = 'fail'

    return title + ' ' + duties_text


def model_result(input_vector: dict, token: str, url: str) -> list:
    url = url + 'get_recs'

    data = {
        'token': token,
        'vector': input_vector
    }
    result = get_response(url, data)
    if result['status'] == 'ok':
        result = result['result']
    else:
        result = []

    return result


def search_result(text: str, token: str, url: str) -> list:
    url = url + 'search'

    data = {
        'token': token,
        'string': text
    }
    result = get_response(url, data)
    if result['status'] == 'ok':
        result = result['result']
    else:
        result = []

    return result


def get_response(url, data):
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    payload = json.dumps(data)
    r = requests.post(url, data=payload, headers=headers)
    result = r.json()
    return result


def get_nearest_vac(url: str, city: str):
    data = {
        "token": "shdfksdhflkdsfh",
        "data": city,
        "get_vac": True
    }
    nearest_vac = get_response(url, data)

    status = nearest_vac['status']

    if status:
        return nearest_vac['data']
    else:
        return -1


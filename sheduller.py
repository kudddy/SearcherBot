from termcolor import colored
from time import sleep

from Cache.cache import vacs_filename, index_filename
from VacancyUploader.parser import Parser
from SearchEngine.EasySearchEngine import InversIndexSearch
from ext.helper import structure_normalization as norm, set_logger
from ext.pickler import Pickler as pcl
from Service.const import token_fastext, url_fasttext
from Service.const import time_for_sleep_sheduller

SearchEngine = InversIndexSearch(url=url_fasttext, token=token_fastext)
get_data = Parser()
logger = set_logger(colored('SearchEngine', 'green'))

while True:
    logger.info("Начало обновления")

    logger.info("Выгрузка данных")
    d_vac = get_data.get_jobs_api(is_parse=False)
    norm_d_vac = norm(d_vac)

    logger.info("Обновление индекса движка")
    SearchEngine.update_index(norm(d_vac))

    pcl.dump_pickle_file(norm_d_vac, vacs_filename)
    pcl.dump_pickle_file(SearchEngine.cache_index, index_filename)

    sleep(time_for_sleep_sheduller)

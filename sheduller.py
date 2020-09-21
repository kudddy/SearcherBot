from termcolor import colored
from time import sleep

from Cache.cache import vacs_filename, index_filename
from VacancyUploader.parser import Parser
from SearchEngine.EasySearchEngine import InversIndexSearch
from ext.helper import structure_normalization as norm, set_logger
from ext.pickler import Pickler as pcl

SearchEngine = InversIndexSearch(url="http://104.154.103.236:8080/FastTextAsServer",
                                 token="dkhfklsdhflksdhflksdhf43934")
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

    sleep(60*60*12)

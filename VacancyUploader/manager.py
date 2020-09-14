from Cache.cache import vacs_filename, index_filename
from VacancyUploader.parser import Parser
from SearchEngine.EasySearchEngine import InversIndexSearch
from ext.helper import structure_normalization as norm
from ext.pickler import Pickler as pcl
from time import sleep

SearchEngine = InversIndexSearch(url="http://104.154.103.236:8080/FastTextAsServer",
                                 token="dkhfklsdhflksdhflksdhf43934")
get_data = Parser()


def worker(q):
    while True:
        d_vac = get_data.get_jobs_api(is_parse=False)

        norm_d_vac = norm(d_vac)
        # данный объект нужно передавать управляющей контрукции и лучше дампить
        # потому что нужно все это синхронизировать с репой

        pcl.dump_pickle_file(norm_d_vac, vacs_filename)

        SearchEngine.update_index(norm(d_vac))
        # данный объект нужно передавать управляющей контрукции
        pcl.dump_pickle_file(SearchEngine.cache_index, index_filename)

        q.put({
            'norm_d_vac': norm_d_vac,
            'cache_index': SearchEngine.cache_index
        }, block=False)

        # на данном этапе нужно сигнализировать остальные процессы подхватить изменения
        # поэтому простой запрос заставит обновиться только один процесс
        # нужно придумать как обновлять все процессы в зависимости от кол-во запущенных воркеров
        # но пока пох, но нужно подумать

        sleep(60*2)



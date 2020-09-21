from termcolor import colored
from collections import Counter
from tqdm import tqdm

from SearchEngine.Tokenizer import QueryBuilder
from ext.pickler import Pickler as pcl
from ext.helper import set_logger, get_clean_text_str
from ext.ClientFasttext import ClientFasttext
from Cache.cache import index

tokenizer = QueryBuilder(out_clean='str', out_token='list')

index_filename = 'Cache/files/index_cache.p'


class InversIndexSearch(ClientFasttext):
    def __init__(self, url: str, token: str, topn=30):
        super(InversIndexSearch, self).__init__(url, token)
        self.__logger = set_logger(colored('SearchEngine', 'green'))
        self.topn = topn
        try:
            self.cache_index = index
        except FileNotFoundError:
            self.cache_index = None
            self.__logger.critical('index not found')

    def update_index(self, vacancy_dict: dict):
        self.cache_index['cache_index'] = {}
        self.cache_index['index_map'] = []
        global_cache = {}
        global_arr = []
        self.__logger.info('cleaning text')
        for k, dirty_string in vacancy_dict.items():
            clean_token = tokenizer.clean_query(get_clean_text_str(dirty_string['content']))
            global_cache.update({k: clean_token})
            global_arr.extend(clean_token)
        self.__logger.info('done')

        self.__logger.info('indexing')
        for token in set(global_arr):
            # cоздание словаря с мэппингом слова к словам, которые близки по контексту
            result = [x[0] for x in self.get_most_similar(token, topn=self.topn)] + [token]
            size = self.topn + 1
            iter_dict = dict(zip(result, [token] * size))
            self.cache_index['index_map'].extend(list(iter_dict.items()))
            local_arr = []
            for k, v in global_cache.items():
                if token in v:
                    local_arr.append(k)
            self.cache_index['cache_index'].update({token: local_arr})
        self.__logger.info('done')

        self.__logger.info('dump structure')
        pcl.dump_pickle_file(self.cache_index, index_filename)

    def search(self, query: str, n=20) -> list:

        query = tokenizer.clean_query(query)
        result_dict = []
        for token in query:
            for tpl in self.cache_index['index_map']:
                if token == tpl[0]:
                    if tpl[1] in self.cache_index['cache_index'].keys():
                        result_dict.extend(self.cache_index['cache_index'][tpl[1]])

        cnt_object = Counter(result_dict)
        return sorted(cnt_object, key=cnt_object.get, reverse=True)[:n]

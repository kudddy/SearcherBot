from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, MetaData, Integer, select
from ext.pickler import Pickler as pcl
from db.schema import vacancy_info_table, db
from tqdm import tqdm


# # создаем таблицу с свежими вакансиями
# d = pcl.get_pickle_file('/Users/kirillhudakov/PycharmProjects/SearcherBot/Cache/files/struct_actual_vac.pickle')
#
# with db.connect() as conn:
#     print('Создаем таблицу')
#     vacancy_info_table.drop()
#     vacancy_info_table.create()
#     data = []
#     for k, v in tqdm(d.items()):
#         key = k
#         if 'title' in v['content']:
#             title = v['content']['title']
#         else:
#             title = 'None'
#         if 'footer' in v['content']:
#             footer = v['content']['footer']
#         else:
#             footer = 'None'
#         if 'header' in v['content']:
#             header = v['content']['header']
#         else:
#             header = 'None'
#         if 'duties' in v['content']:
#             duties = v['content']['duties']
#         else:
#             duties = 'None'
#         if 'conditions' in v['content']:
#             conditions = v['content']['conditions']
#         else:
#             conditions = 'None'
#         data.append({'vacancy_id': key, 'title': title, 'footer': footer, 'header': header, 'duties': duties,
#                     'conditions': conditions})
#         # insert_statement = vacancy_info_table.insert().values(vacancy_id=key, footer=footer, header=header,
#                                                               # duties=duties, conditions=conditions)
#
#     insert_statement = vacancy_info_table.insert().values(data)
#     print('мы тут')
#     conn.execute(insert_statement)

# SAMPLE_QUERY = select([vacancy_info_table.c.footer])
#
#
# insert_statement = SAMPLE_QUERY.where(vacancy_info_table.c.vacancy_id == '1326963')
# with db.connect() as conn:
#     data = conn.execute(insert_statement)
#     print(list(data))


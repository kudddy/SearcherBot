from sqlalchemy import select

from db.schema import vacancy_info_table


VACANCY_QUERY = select([vacancy_info_table.c.title, vacancy_info_table.c.header])
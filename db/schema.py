import memcache
# from enum import Enum, unique
# from sqlalchemy import create_engine
#
# from sqlalchemy import (
#     Column, Date, Enum as PgEnum, ForeignKey, ForeignKeyConstraint, Integer,
#     MetaData, String, Table,
# )
# db_string = "postgresql://BotBase_master:fvjsYUtq@postbot.cgudfwtndfnn.us-east-2.rds.amazonaws.com:5432/TeleBotPstGrs"

# db = create_engine(db_string)
#
# meta = MetaData(db)
#
# vacancy_info_table = Table(
#     'vacancy_info',
#     meta,
#     Column('id', Integer, primary_key=True),
#     Column('vacancy_id', String),
#     Column('title', String),
#     Column('footer', String),
#     Column('header', String),
#     Column('duties', String),
#     Column('conditions', String)
#
# )
#
# conn = db.connect()


mc = memcache.Client(['127.0.0.1:11211'])


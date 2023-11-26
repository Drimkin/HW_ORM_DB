import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, exc
from sqlalchemy.exc import OperationalError

from models import create_tables, Publisher, Book, Shop, Stock, Sale

type_ = input('Введите тип базы данных (postgresql, MSSQL или др.): ')
login = input('Введите имя пользователя базы данных: ')
password = input('Введите пароль: ')
db = input('Введите имя базы данных для подключения: ')

engine = sqlalchemy.create_engine(f'{type_}://{login}:{password}@localhost:5432/{db}')


create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()


session.close()
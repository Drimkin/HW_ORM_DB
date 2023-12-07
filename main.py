import json

import sqlalchemy
import sqlalchemy as sq
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Publisher, Book, Shop, Stock, Sale, create_tables

type_ = input('Введите тип базы данных (postgresql, MSSQL или др.): ')
login = input('Введите имя пользователя базы данных: ')
password = input('Введите пароль: ')
db = input('Введите имя базы данных для подключения: ')

engine = sqlalchemy.create_engine(f'{type_}://{login}:{password}@localhost:5432/{db}')

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'book': Book,
        'shop': Shop,
        'stock': Stock,
        'sale': Sale
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()

publisher_request = input("Введите имя или идентификатор издателя: ")

query = (session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).
         join(Stock, Book.id == Stock.id_book).
         join(Shop, Stock.id_shop == Shop.id).
         join(Sale, Stock.id == Sale.id_stock).
         filter(Book.id_publisher == Publisher.id))

if publisher_request.isdigit():
    query = query.filter(Publisher.id == publisher_request).all()
else:
    query = query.filter(Publisher.name == publisher_request).all()
for title, shop_name, price, date_sale in query:
    print(f"{title} | {shop_name} | {price} | {date_sale.strftime('%d-%m-%Y')}")

session.close()
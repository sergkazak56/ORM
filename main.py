import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale
import json

# Открытие базы данных и создание таблиц из задания 2
db_name = 'bookstock_db'    #Здесь надо подставить имя вашей БД
password = '******'        #Здесь вставляется пароль к postgres
DSN = f'postgresql://postgres:{password}@localhost:5432/{db_name}'
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Импорт данных в таблицы из json файла (задание 3)
with open("tests_data.json") as td:
    json_data = json.load(td)
model = {'publisher': Publisher, 'shop': Shop, 'book': Book, 'stock': Stock, 'sale': Sale}
for item in json_data:
    class_name = model[item.get('model')]
    session.add(class_name(**item.get('fields')))
session.commit()

# Создание запроса из задания 2
name_id_publ = input('Введите имя или id издательства: ')
if name_id_publ.isdigit():
    for q in session.query(Publisher).filter(Publisher.id == int(name_id_publ)):
        print(q)
else:
    for q in session.query(Publisher).filter(Publisher.name == name_id_publ):
        print(q)

# Доп. задание: создание выборки магазинов, где продают книги определенного издательства
# Без подзапроса:
name_publ = input('Введите имя издательства: ')
for q in session.query(Shop).join(Stock.shop).join(Stock.book).join(Book.publisher).filter(Publisher.name == name_publ).all():
    print(q)

# Через подзапрос:
name_publ = input('Введите имя издательства: ')
subq = session.query(Stock).join(Stock.book).join(Book.publisher).filter(Publisher.name == name_publ).subquery()
for q in session.query(Shop).join(subq, Shop.id == subq.c.id_shop).all():
    print(q)
session.close()

# pip install psycopg
import psycopg

from CONFIG import *

"""
Обновил способ создания таблиц
Раньше было написано 5 разных функция, в которых отличался только скрипт создания
=> лишний раз писать строки:
cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()
    
Теперь это лежит в 1 функции, которая принимает разные запросы и выполняет их.
При работе соблюдайте порядок заполнения

*я еще не тестировал этот код, он не должен выдавать ошибку, т.к. сделан по аналогии со старым
но если будет ошибка - пишите!
"""
query_partners_import = '''
    create table partners_import (
    partner_type nchar(3) not null,
    partner_name nchar(100) PRIMARY KEY not null,
    partner_dir nchar(100) not null,
    partner_mail nchar(100) not null,
    partner_phone nchar(13) not null,
    partner_addr nchar(300) not null,
    partner_inn nchar(10) not null,
    partner_rate nchar(2) not null
    )
    '''

query_partner_products_import = '''
    create table partner_products_import (
    product_name_fk nchar(300) not null,
    FOREIGN KEY (product_name_fk) REFERENCES products_import(product_name) ON UPDATE CASCADE,
    
    partner_name_fk nchar(100) not null,
    FOREIGN KEY (partner_name_fk) REFERENCES partners_import(partner_name) ON UPDATE CASCADE,
    
    product_count int not null,
    sale_date date not null
    )
    '''

query_material_type_import = '''
    create table material_type_import (
    material_type nchar(50) PRIMARY KEY not null,
    material_broke_percent nchar(5) not null
    )
    '''

query_products_import = '''
    create table products_import (
    product_type_fk nchar(50) not null,
    FOREIGN KEY (product_type_fk) REFERENCES product_type_import(product_type) ON UPDATE CASCADE,
    product_name nchar(300) PRIMARY KEY not null,
    product_article bigint not null,
    product_min_cost real not null
    )
    '''

query_product_type_import = '''
    create table product_type_import (
    product_type nchar(50) PRIMARY KEY not null,
    product_coefficient_type real not null
    )
    '''


def create_table(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()


# Создание строки подключения к серверу
connection_uri = psycopg.connect(
    user=USER,
    host=HOST,
    password=PASS,
    dbname=DBNAME
)
create_table(connection_uri, query_partners_import)
create_table(connection_uri, query_product_type_import)
create_table(connection_uri, query_material_type_import)
create_table(connection_uri, query_products_import)
create_table(connection_uri, query_partner_products_import)

# pip install psycopg
import psycopg

from CONFIG import *


def create_partners_import(connection):
    # Создание запроса к бд
    query = '''
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
    # Создание курсора для запуска запроса
    cursor = connection.cursor()
    # Исполнение запроса
    cursor.execute(query)
    # Сохранение изменений
    connection.commit()
    # Закрытие курсора
    cursor.close()


def create_partner_products_import(connection):
    query = '''
    create table partner_products_import (
    product_name_fk nchar(300) not null,
    FOREIGN KEY (product_name_fk) REFERENCES products_import(product_name) ON UPDATE CASCADE,
    
    partner_name_fk nchar(100) not null,
    FOREIGN KEY (partner_name_fk) REFERENCES partners_import(partner_name) ON UPDATE CASCADE,
    
    product_count int not null,
    sale_date date not null
    )
    '''
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()


def create_material_type_import(connection):
    query = '''
    create table material_type_import (
    material_type nchar(50) PRIMARY KEY not null,
    material_broke_percent nchar(5) not null
    )
    '''
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()


def create_products_import(connection):
    query = '''
    create table products_import (
    product_type_fk nchar(50) not null,
    FOREIGN KEY (product_type_fk) REFERENCES product_type_import(product_type) ON UPDATE CASCADE,
    product_name nchar(300) PRIMARY KEY not null,
    product_article bigint not null,
    product_min_cost real not null
    )
    '''
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()


def create_product_type_import(connection):
    query = '''
    create table product_type_import (
    product_type nchar(50) PRIMARY KEY not null,
    product_coefficient_type real not null
    )
    '''
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()


def main():
    # Создание строки подключения к серверу
    connection_uri = psycopg.connect(
        user=USER,
        host=HOST,
        password=PASS,
        dbname=DBNAME
    )
    # Вызов скриптов на создание таблиц (Важен порядок создания)
    create_partners_import(connection_uri)
    create_product_type_import(connection_uri)
    create_material_type_import(connection_uri)
    create_products_import(connection_uri)
    create_partner_products_import(connection_uri)

main()

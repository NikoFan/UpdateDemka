import psycopg

from DATABASE import CONFIG

from CheckInputData import start_check


class Database():
    def __init__(self):
        # Инициализация классовой переменной для строки подключения
        self.connection_uri = self.connect_to_db()

    def connect_to_db(self):
        """
        Функция подключения к БД на сервере
        :return: Возвращает строку подключения, с которой потом ведется работа
        """
        # Все действия с БД должны производиться с проверкой try: except, чтобы предотвратить поломку приложения
        try:
            print('База данных -> Подключение')
            # Создание строки подключения
            connection = psycopg.connect(
                user=CONFIG.USER,
                host=CONFIG.HOST,
                password=CONFIG.PASS,
                dbname=CONFIG.DBNAME
            )
            print('База данных -> Подключена')
            # Возвращение в переменную self.connection_uri значения переменной connection
            return connection
        except Exception as error:  # Обработка любой ошибки при работе с БД
            print(f':: {error}')
            # При ошибке в переменную self.connection_uri возвращается значение None.
            return None

    def take_all_partners_info(self):
        """
        Функция получения всей информации о Партнерах, для создания карточек
        :return:
        """
        try:
            query = '''
            SELECT *
            FROM partners_import;
            '''
            # Создание курсора для взаимодействия с БД
            cursor = self.connection_uri.cursor()
            # Исполнение запроса
            cursor.execute(query)

            # Создание массива для хранения результатов
            partners_data = []
            # Перебор ответа из Базы данных
            for return_row in cursor.fetchall():
                # Добавление данных в массив
                partners_data.append(
                    {  # При добавлении используются словари {}
                        'type': return_row[0].strip(),  # .strip() - Обрезание лишних пробелов. Только для nchar()
                        'name': return_row[1].strip(),
                        'dir': return_row[2].strip(),
                        'mail': return_row[3].strip(),
                        'phone': return_row[4].strip(),
                        'addr': return_row[5].strip(),
                        'inn': return_row[6].strip(),
                        'rate': return_row[7].strip()
                    }
                )
            # Возврат данных
            return partners_data
        except Exception as error:
            print(f':: {error}')
            # При ошибке возвращается пустой список
            return []

    def take_count_of_sales(self, partner_name: str):
        """
        Функция получения числа продаж для конкретного партнера
        :param partner_name: Имя интересующего партнера
        :return: Число продаж из истории
        """
        try:
            query = f'''
            SELECT SUM(product_count)
            FROM partner_products_import
            WHERE partner_name_fk = '{partner_name}';
            '''
            # Создание курсора для взаимодействия с БД
            cursor = self.connection_uri.cursor()
            # Исполнение запроса
            cursor.execute(query)
            # Запись значения в переменную
            count = cursor.fetchone()
            # Закрытие курсора
            cursor.close()
            # Проверка наличия ответа на запрос
            if count:
                return count[0]
            # Возврат пустоты
            return None
        except Exception as error:
            print(f'::^ {error}')
            # При ошибке возвращается пустоту
            return None

    def add_new_partner(self, partner_data: dict):
        """
        Функция добавление нового партнера в БД
        :param partner_data: Словарь с введенными пользователем данными
        :return: Результат операции True | False
        """
        try:
            # Вызов проверки для данных
            if not start_check(partner_data):
                # если проверка не пройдена - Вернуть False
                return False

            query = f'''
            INSERT INTO partners_import
            VALUES (
            '{partner_data['type']}', 
            '{partner_data['name']}', 
            '{partner_data['dir']}', 
            '{partner_data['mail']}', 
            '{partner_data['phone']}', 
            '{partner_data['addr']}', 
            '{partner_data['inn']}', 
            '{partner_data['rate']}');
            '''

            # Создание курсора для взаимодействия с БД
            cursor = self.connection_uri.cursor()
            # Исполнение запроса
            cursor.execute(query)
            # Сохранение изменений в БД
            self.connection_uri.commit()
            cursor.close()
            # Возврат пустоты
            return True
        except Exception as error:
            print(f'::^ {error}')
            # При ошибке возвращается пустоту
            return False

    def take_partner_info(self, partner_name: str):
        """
        Функция получения всей информации о Конкретном партнере, для выгрузки в окно информации
        :param partner_name - Имя конкретного партнера
        :return:
        """
        try:
            query = f'''
            SELECT *
            FROM partners_import
            WHERE partner_name = '{partner_name}';
            '''
            # Создание курсора для взаимодействия с БД
            cursor = self.connection_uri.cursor()
            # Исполнение запроса
            cursor.execute(query)
            # Создание словаря для хранения результатов
            partners_data = dict()
            for data in cursor.fetchall():
                # Заполнение словаря, который будет возвращен
                partners_data = {  # При добавлении используются словари {}
                    'type': data[0].strip(),  # .strip() - Обрезание лишних пробелов. Только для nchar()
                    'name': data[1].strip(),
                    'dir': data[2].strip(),
                    'mail': data[3].strip(),
                    'phone': data[4].strip(),
                    'addr': data[5].strip(),
                    'inn': data[6].strip(),
                    'rate': data[7].strip()
                }
            # Закрытие курсора
            cursor.close()
            # Возврат данных
            return partners_data
        except Exception as error:
            print(f':: {error}')
            # При ошибке возвращается пустой словарь
            return dict()

    def update_partner(self, partner_data: dict, partner_name: str):
        """
        Функция добавление нового партнера в БД
        :param partner_data: Словарь с введенными пользователем данными
        :param partner_name: Старое имя партнера, которе используется (на случай если его изменят - надо определить в БД)
        :return: Результат операции True | False
        """
        try:
            # Вызов проверки для данных
            if not start_check(partner_data):
                # если проверка не пройдена - Вернуть False
                return False

            query = f'''
            UPDATE partners_import
            SET 
            partner_type = '{partner_data['type']}', 
            partner_name = '{partner_data['name']}', 
            partner_dir = '{partner_data['dir']}', 
            partner_mail = '{partner_data['mail']}', 
            partner_phone = '{partner_data['phone']}', 
            partner_addr = '{partner_data['addr']}', 
            partner_inn = '{partner_data['inn']}', 
            partner_rate = '{partner_data['rate']}'
            
            WHERE partner_name = '{partner_name}';
            '''

            # Создание курсора для взаимодействия с БД
            cursor = self.connection_uri.cursor()
            # Исполнение запроса
            cursor.execute(query)
            # Сохранение изменений в БД
            self.connection_uri.commit()
            cursor.close()
            # Возврат пустоты
            return True
        except Exception as error:
            print(f'::^ {error}')
            # При ошибке возвращается пустоту
            return False


    def take_partner_history_info(self, partner_name: str):
        """
        Функция получения всей информации о Конкретном партнере, для выгрузки в таблицу
        :param partner_name Имя партнера
        :return: Список со словарем
        """
        try:
            query = f'''
                    SELECT *
                    FROM partner_products_import
                    WHERE partner_name_fk = '{partner_name}';
                    '''
            # Создание курсора для взаимодействия с БД
            cursor = self.connection_uri.cursor()
            # Исполнение запроса
            cursor.execute(query)
            # Создание массива для хранения результатов
            partners_data = []
            for data in cursor.fetchall():
                # Заполнение массива, который будет возвращен
                partners_data.append(
                    {  # При добавлении используются словари {}
                        'product': data[0].strip(),  # .strip() - Обрезание лишних пробелов. Только для nchar()
                        'partner': data[1].strip(),
                        'count': data[2],  # Эти параметры int и date - не применяют strip()
                        'date': data[3],
                    }
                )

            # Закрытие курсора
            cursor.close()
            # Возврат данных
            return partners_data
        except Exception as error:
            print(f':: {error}')
            # При ошибке возвращается пустой массива
            return []
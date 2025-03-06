import psycopg

from CheckInputData import start_check


class DatabaseMainClass():
    def __init__(self):
        self.connection_uri = self.connect_db()

    def connect_db(self):
        """
        Функция для подключения к базе данных
        :return: Строка подключения
        """
        try:
            USER = "administrator"
            HOST = "localhost"
            PASS = "123456"
            PORT = 5432
            DBNAME = "update_demoexam"
            connection = psycopg.connect(
                user=USER,
                host=HOST,
                password=PASS,
                dbname=DBNAME
            )
            print("Подключение Удачно")
            return connection
        except Exception as error:
            print("Подключение Ошибка")
            print(error)
            return None

    def take_all_partners(self):
        """
        Функция получения всех партеров
        :return: Список со словарями партеров
        """
        try:
            query = """
            select *
            from partners_import
            """
            cursor = self.connection_uri.cursor()
            cursor.execute(query)

            # [
            #   {"type":"123", "name":"NAME", "dir":"123"},
            #   {"type":"123", "name":"NAME$", "dir":"123"}
            # ]
            partners = []
            for row in cursor.fetchall():
                partners.append(
                    {
                        "type": row[0].strip(),
                        "name": row[1].strip(),
                        "dir": row[2].strip(),
                        "mail": row[3].strip(),
                        "phone": row[4].strip(),
                        "addr": row[5].strip(),
                        "inn": row[6].strip(),
                        "rate": row[7].strip()
                    }
                )
            return partners

        except Exception as error:
            print(error)
            return []

    def take_sales_sum(self, partner_name: str):
        """
        Функция получения количества продаж
        :param partner_name: Имя партнера
        :return: Число продаж партнера
        """

        try:
            query = f"""
            select SUM(product_count)
            from partner_products_import
            where partner_name_fk = '{partner_name}'
            """
            cursor = self.connection_uri.cursor()
            cursor.execute(query)

            answer = cursor.fetchone()

            cursor.close()
            return answer[0]

        except Exception as error:
            print(error)
            return None

    def take_partner(self, partner_name: str):
        """
        Функция получения всех партеров
        :return: Список со словарями партеров
        """
        try:
            query = f"""
                       select *
                       from partners_import
                       where partner_name = '{partner_name}'
                       """
            cursor = self.connection_uri.cursor()
            cursor.execute(query)

            partners = []
            for row in cursor.fetchall():
                partners.append(
                    {
                        "type": row[0].strip(),
                        "name": row[1].strip(),
                        "dir": row[2].strip(),
                        "mail": row[3].strip(),
                        "phone": row[4].strip(),
                        "addr": row[5].strip(),
                        "inn": row[6].strip(),
                        "rate": row[7].strip()
                    }
                )
            return partners

        except Exception as error:
            print(error)
            return []


    def update_partner_data(self, new_partner_data: dict, partner_name: str):
        """
        Функция обновления данных партнера
        :param new_partner_data: Словарь с данными
        :param partner_name: Старое имя партнера
        :return: bool
        """

        try:
            query = f"""
            UPDATE partners_import
            SET
            partner_type = '{new_partner_data["type"]}',
            partner_name = '{new_partner_data["name"]}',
            partner_dir = '{new_partner_data["dir"]}',
            partner_mail = '{new_partner_data["mail"]}',
            partner_phone = '{new_partner_data["phone"]}',
            partner_addr = '{new_partner_data["addr"]}',
            partner_inn = '{new_partner_data["inn"]}',
            partner_rate = '{new_partner_data["rate"]}'
            
            where partner_name = '{partner_name}'
            """

            if start_check(new_partner_data) == False:
                return False
            cursor = self.connection_uri.cursor()
            cursor.execute(query)

            self.connection_uri.commit()
            return True


        except Exception as error:
            print(error)
            return False

    def create_partner_data(self, new_partner_data: dict):
        """
        Функция обновления данных партнера
        :param new_partner_data: Словарь с данными
        :param partner_name: Старое имя партнера
        :return: bool
        """

        try:
            query = f"""
            insert into partners_import
            values ('{new_partner_data["type"]}',
            '{new_partner_data["name"]}',
            '{new_partner_data["dir"]}',
            '{new_partner_data["mail"]}',
            '{new_partner_data["phone"]}',
            '{new_partner_data["addr"]}',
            '{new_partner_data["inn"]}',
            '{new_partner_data["rate"]}')
            """

            if start_check(new_partner_data) == False:
                return False
            cursor = self.connection_uri.cursor()
            cursor.execute(query)

            self.connection_uri.commit()
            return True


        except Exception as error:
            print(error)
            return False

    def take_history(self, partner_name: str):
        """
        Функция получения истории определенного партнера
        :param partner_name: Имя интересующего партнера
        :return: Список со словарями
        """

        try:
            query = f"""
            select *
            from partner_products_import
            where partner_name_fk = '{partner_name}'
            """
            cursor = self.connection_uri.cursor()
            cursor.execute(query)

            partner_history = []

            for row in cursor.fetchall():
                partner_history.append(
                    {
                        "Продукт":row[0].strip(),
                        "Партнер":row[1].strip(),
                        "Количество":row[2],
                        "Дата":row[3],
                    }
                )

            return partner_history

        except Exception as error:
            print(error)
            return []

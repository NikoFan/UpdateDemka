from PySide6.QtWidgets import (
    QWidget,  # Нужен для создания виджетов
    QVBoxLayout,  # Разметка, которая размещает объекты вертикально
    QScrollArea,  # Область прокрутки для объектов
    QLabel,  # Текстовое поле для объектов
    QPushButton,  # Кнопка для пользователя
    QComboBox,  # Создание выпадающего списка
    QLineEdit,  # Поле для текстового ввода
    QFrame  # Нужно для сборки фрейма
)

import PartnerStatic

from DATABASE import Database

from SendMessageBox import *

from FRAMES import PartnerInfoFrame



class UpdatePartnerClass(QFrame):
    def __init__(self, main_class_controller):  # Конструктор класса UpdatePartnerClass
        # main_class_controller - Переменная для взаимодействия с Функциями и Переменными из класса MainApplicationClass
        QFrame.__init__(self)  # Вызов родительского класса
        # Создание переменной, для взаимодействия с main_class_controller во всем классе
        self.controller = main_class_controller
        # Приписка ': DATABASE.Database.Database', позволяет IDE понять с каким классом ведется работа в момент написания кода
        self.db: Database.Database = main_class_controller.db

        self.main_frame_layout = QVBoxLayout(self)  # Разметка фрейма (хранит в себе все объекты)
        self.setup_ui()

    def setup_ui(self):
        # Создание текстового поля
        title_label = QLabel("Добавление партнера")
        # Назначение объектного имени для стилизации объекта
        title_label.setObjectName("Title")
        # ДОБАВЛЕНИЕ текстового поля на фрейм
        self.main_frame_layout.addWidget(title_label)

        # Получение данных из бд по партнеру, старые данные
        partners_data = self.db.take_partner_info(PartnerStatic.Partner.get_name())

        # Создание полей для ввода и подсказок
        self.create_hint_label("Обновите Имя партнера")
        self.partner_name = self.create_edit_line(partners_data['name'], 100)

        self.create_hint_label("Обновите Телефон партнера")
        self.partner_phone = self.create_edit_line(partners_data['phone'], 13)
        self.partner_phone.setInputMask('+7 000 000 00 00') # Добавление маски для ввода

        self.create_hint_label("Обновите ИНН партнера")
        self.partner_inn = self.create_edit_line(partners_data['inn'], 10)

        self.create_hint_label("Обновите Юридический адрес партнера")
        self.partner_ur_addr = self.create_edit_line(partners_data['addr'], 300)

        self.create_hint_label("Обновите ФИО директора партнера")
        self.partner_dir = self.create_edit_line(partners_data['dir'], 100)

        self.create_hint_label("Обновите Рейтинг (от 1 до 10) партнера")
        self.partner_rate = self.create_edit_line(partners_data['rate'], 2)

        self.create_hint_label("Обновите Электронную почту партнера")
        self.partner_mail = self.create_edit_line(partners_data['mail'], 100)

        self.create_hint_label("Укажите тип партнера")
        # Создание выпадающего списка
        self.partner_type = QComboBox()
        # Добавление элементов в выпадающий список
        self.partner_type.addItems(["ООО", "ОАО", "ПАО", "ЗАО"])
        self.main_frame_layout.addWidget(self.partner_type)

        # Создание кнопки для добавления партнера в БД
        add_btn = QPushButton("Обновить партнера")
        # Добавление действия при нажатии на кнопку
        add_btn.clicked.connect(self.add_partner) # Если действие без lambda - Скобки не ставятся
        # Добавление кнопки в разметку фрейма
        self.main_frame_layout.addWidget(add_btn)


        back_btn = QPushButton("Назад")
        # Добавление действия при нажатии на кнопку
        back_btn.clicked.connect(
            lambda : self.controller.switch_frames(PartnerInfoFrame.PartnerInfoClass)
        )  # Если действие без lambda - Скобки не ставятся
        # Добавление кнопки в разметку фрейма
        self.main_frame_layout.addWidget(back_btn)

    def add_partner(self):
        """
        Функция отправки данных на добавление в БД
        :return: Ничего не возвращается
        """

        # Создание словаря для хранения введенных данных
        partner_input_data: dict = {
            # Считывание элемента из self.partner_type используя функцию .currentText()
            "type": self.partner_type.currentText(),
            "name": self.partner_name.text(),  # Считывание текста из self.partner_name используя функцию .text()
            "dir": self.partner_dir.text(),
            "mail": self.partner_mail.text(),
            "phone": self.partner_phone.text()[3:], # В словарь добавляем только '999 999 99 99', без '+7 '
            "addr": self.partner_ur_addr.text(),
            "inn": self.partner_inn.text(),
            "rate": self.partner_rate.text()
        }

        if self.db.update_partner(partner_input_data, PartnerStatic.Partner.get_name()):
            # Если процесс добавления партнера - успешен
            send_I_message("Партнер Обновлен!")
            # Обновление имени партнера, если оно обновилось 0 это не крашнет прогу
            PartnerStatic.Partner.set_name(self.partner_name.text())
            return # Пустой return, чтобы завершить работу функции
        send_C_message("Ошибка Обновления!")
        return


    def create_hint_label(self, text: str):
        """
        Функция создания текстового поля-подсказки
        :param text: Текст, устанавливающийся в текстовое поле
        :return: Ничего не возвращается, нам не надо считывать данные из QLabel
        """
        # Создание текстового поля И установка текста в него
        label = QLabel(text)
        # Назначение объектного имени для дизайна
        label.setObjectName("Hint_label")

        # Добавление текстового поля в разметку фрейма
        self.main_frame_layout.addWidget(label)

    def create_edit_line(self, text: str, max_length: int):
        """
        Функция создания текстового ввода по паттерну
        :param text: Исчезающий текст
        :param max_length: Максимальная длина допустимая для ввода
        :return: Объект для присвоения к переменной
        """

        # Создание текстового ввода
        edit = QLineEdit()
        # Установка текста
        edit.setText(text)
        edit.setMaxLength(max_length)

        # Добавление текстового поля в разметку фрейма
        self.main_frame_layout.addWidget(edit)

        return edit

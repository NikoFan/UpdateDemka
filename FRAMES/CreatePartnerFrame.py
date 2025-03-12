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

from DATABASE import Database

from SendMessageBox import *

from FRAMES import PartnersCardFrame



class CreatePartnerClass(QFrame):
    def __init__(self, main_class_controller):  # Конструктор класса CreatePartnerClass
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

        # Создание полей для ввода и подсказок
        self.create_hint_label("Введите Имя партнера")
        self.partner_name = self.create_edit_line("Введите имя", 100)

        self.create_hint_label("Введите Телефон партнера")
        self.partner_phone = self.create_edit_line("Введите Телефон", 13)
        self.partner_phone.setInputMask('+7 000 000 00 00') # Добавление маски для ввода

        self.create_hint_label("Введите ИНН партнера")
        self.partner_inn = self.create_edit_line("Введите инн", 10)

        self.create_hint_label("Введите Юридический адрес партнера")
        self.partner_ur_addr = self.create_edit_line("Введите Юр. адрес", 300)

        self.create_hint_label("Введите ФИО директора партнера")
        self.partner_dir = self.create_edit_line("Введите ФИО директора", 100)

        self.create_hint_label("Введите Рейтинг (от 1 до 10) партнера")
        self.partner_rate = self.create_edit_line("Введите рейтинг", 2)

        self.create_hint_label("Введите Электронную почту партнера")
        self.partner_mail = self.create_edit_line("Введите почту", 100)

        self.create_hint_label("Укажите тип партнера")
        # Создание выпадающего списка
        self.partner_type = QComboBox()
        # Добавление элементов в выпадающий список
        self.partner_type.addItems(["ООО", "ОАО", "ПАО", "ЗАО"])
        self.main_frame_layout.addWidget(self.partner_type)

        # Создание кнопки для добавления партнера в БД
        add_btn = QPushButton("Добавить партнера")
        # Добавление действия при нажатии на кнопку
        add_btn.clicked.connect(self.add_partner) # Если действие без lambda - Скобки не ставятся
        # Добавление кнопки в разметку фрейма
        self.main_frame_layout.addWidget(add_btn)

        # Создание кнопки для возврата на главное окно
        back_btn = QPushButton("Назад")
        # Добавление действия при нажатии на кнопку
        back_btn.clicked.connect(
            lambda : self.controller.switch_frames(PartnersCardFrame.PartnerCardsClass)
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

        if self.db.add_new_partner(partner_input_data):
            # Если процесс добавления партнера - успешен
            send_I_message("Партнер добавлен!")
            return # Пустой return, чтобы завершить работу функции
        send_C_message("Ошибка добавления!")
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

    def create_edit_line(self, placeholder_text: str, max_length: int):
        """
        Функция создания текстового ввода по паттерну
        :param placeholder_text: Исчезающий текст
        :param max_length: Максимальная длина допустимая для ввода
        :return: Объект для присвоения к переменной
        """

        # Создание текстового ввода
        edit = QLineEdit()
        # Установка исчезающего текста
        edit.setPlaceholderText(placeholder_text)
        edit.setMaxLength(max_length)

        # Добавление текстового поля в разметку фрейма
        self.main_frame_layout.addWidget(edit)

        return edit

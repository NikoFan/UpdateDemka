from PySide6.QtWidgets import (
    QWidget,  # Нужен для создания виджетов
    QVBoxLayout,  # Разметка, которая размещает объекты вертикально
    QLabel,  # Текстовое поле для объектов
    QPushButton,  # Кнопка для пользователя
    QTreeWidget,  # Создание Таблицы
    QTreeWidgetItem, # Создание элемента таблицы
    QLineEdit,  # Поле для текстового ввода
    QFrame  # Нужно для сборки фрейма
)

import PartnerStatic
from DATABASE import Database

from SendMessageBox import *

from FRAMES import PartnersCardFrame



class HistoryClass(QFrame):
    def __init__(self, main_class_controller):  # Конструктор класса HistoryClass
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

        # Создание таблицы
        table = QTreeWidget()
        # Создание заголовков для колонок
        table.setHeaderLabels(['Продукция', 'Партнер', 'Количество продукции', 'Дата'])
        # Добавление таблицы в окно
        self.main_frame_layout.addWidget(table)

        # Цикл заполнения таблицы данными из БД
        for data in self.db.take_partner_history_info(PartnerStatic.Partner.get_name()):
            # Создание элемента талицы и присвоение его к таблице (через скобки прибили его на ГВОЗДЬ)
            item = QTreeWidgetItem(table)
            item.setText(0, data['product'])
            item.setText(1, data['partner'])
            item.setText(2, str(data['count'])) # Перевод из int в str
            item.setText(3, str(data['date'])) # Перевод из date в str


        # Создание кнопки для возврата назад
        back_btn = QPushButton("Назад")
        # Добавление действия при нажатии на кнопку
        back_btn.clicked.connect(
            lambda : self.controller.switch_frames(PartnersCardFrame.PartnerCardsClass)
        )  # Если действие без lambda - Скобки не ставятся
        # Добавление кнопки в разметку фрейма
        self.main_frame_layout.addWidget(back_btn)




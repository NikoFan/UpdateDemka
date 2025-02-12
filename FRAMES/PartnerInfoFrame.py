from PySide6.QtWidgets import (
    QVBoxLayout,  # Разметка, которая размещает объекты вертикально
    QLabel,  # Текстовое поле для объектов
    QPushButton,  # Кнопка для пользователя
    QLineEdit,  # Поле для текстового ввода
    QFrame  # Нужно для сборки фрейма
)

from DATABASE import Database

from PartnerStatic import Partner

from FRAMES import PartnersCardFrame, UpdatePartnerFrame, HistoryFrame


class PartnerInfoClass(QFrame):
    def __init__(self, main_class_controller):  # Конструктор класса PartnerInfoClass
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
        title_label = QLabel("Информация о партнере")
        # Назначение объектного имени для стилизации объекта
        title_label.setObjectName("Title")
        # ДОБАВЛЕНИЕ текстового поля на фрейм
        self.main_frame_layout.addWidget(title_label)
        # Создание массива с заголовками
        labels_hints = [
            "Тип партнера",
            "Имя партнера",
            "Директор партнера",
            "Почта партнера",
            "Телефон партнера",
            "Юридический адрес партнера",
            "ИНН партнера",
            "Рейтинг партнера",
        ]
        # Создание индекс для перебора массива
        hints_index = 0
        # Цикл для перебора возвращенного из БД словаря
        for key, value in self.db.take_partner_info(Partner.get_name()).items():
            # Создание подсказки для текста
            self.create_hint_label(labels_hints[hints_index])
            # Увеличение индекса на 1
            hints_index += 1
            # Создание Основного текста
            self.create_main_label(value)

        history_btn = QPushButton("История продаж партнера")
        # Добавление действия при нажатии на кнопку
        history_btn.clicked.connect(
            lambda: self.controller.switch_frames(HistoryFrame.HistoryClass)
        )  # Если действие без lambda - Скобки не ставятся

        # Создание кнопки для возврата на главное окно
        back_btn = QPushButton("На главную")
        # Добавление действия при нажатии на кнопку
        back_btn.clicked.connect(
            lambda: self.controller.switch_frames(PartnersCardFrame.PartnerCardsClass)
        )  # Если действие без lambda - Скобки не ставятся
        # Добавление кнопки в разметку фрейма
        self.main_frame_layout.addWidget(history_btn)
        self.main_frame_layout.addWidget(back_btn)

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

    def create_main_label(self, text: str):
        """
        Функция создания текстового ввода по паттерну
        :param placeholder_text: Исчезающий текст
        :param max_length: Максимальная длина допустимая для ввода
        :return: Объект для присвоения к переменной
        """
        # Создание текстового поля И установка текста в него
        label = QLabel(text)
        # Назначение объектного имени для дизайна
        label.setObjectName("Main_label")
        # Добавление текстового поля в разметку фрейма
        self.main_frame_layout.addWidget(label)

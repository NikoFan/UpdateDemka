from PySide6.QtWidgets import (
    QWidget,  # Нужен для создания виджетов
    QVBoxLayout,  # Разметка, которая размещает объекты вертикально
    QScrollArea,  # Область прокрутки для объектов
    QLabel,  # Текстовое поле для объектов
    QPushButton,  # Кнопка для пользователя
    QHBoxLayout,  # Позволяет разместить объекты горизонтально
    QFrame  # Нужно для сборки фрейма

)

from PySide6.QtGui import (
    QPixmap  # Нужна для чтения фотографий
)

from DATABASE import Database

# Добавление файлов с другими фреймами
from FRAMES import  HistoryFrame, UpdatePartnerFrame, CreatePartnerFrame


class PartnerCardsClass(QFrame):
    def __init__(self, main_class_controller):  # Конструктор класса PartnerCardsClass
        # main_class_controller - Переменная для взаимодействия с Функциями и Переменными из класса MainApplicationClass
        QFrame.__init__(self)  # Вызов родительского класса
        # Создание переменной, для взаимодействия с main_class_controller во всем классе
        self.controller = main_class_controller
        # Приписка ': DATABASE.Database.Database', позволяет IDE понять с каким классом ведется работа в момент написания кода
        self.db: Database.Database = main_class_controller.db

        self.main_frame_layout = QVBoxLayout(self)  # Разметка фрейма (хранит в себе все объекты)
        self.setup_ui()

    def setup_ui(self):
        """
        Функция для создания всего интерфейса
        :return: Функция ничего не возвращает
        """

        # Создание текстового поля
        title_label = QLabel("Карточки партнеров")
        # Назначение объектного имени для стилизации объекта
        title_label.setObjectName("Title")
        # ДОБАВЛЕНИЕ текстового поля на фрейм
        self.main_frame_layout.addWidget(title_label)

        # Добавление фотографии на экран
        self.add_picture()

        # Создание области прокрутки
        scroll_area = QScrollArea()
        # Объекты внутри области прокрутки будут подстраивать свой размер под размер области
        scroll_area.setWidgetResizable(True)
        # Установка контейнера с карточками в область прокрутки scroll_area
        scroll_area.setWidget(
            self.create_partners_cards())  # В self.create_partners_cards() возвращается контейнер => он помещается в scroll_area

        # Добавление области прокрутки в разметку фрейма
        self.main_frame_layout.addWidget(scroll_area)

        # Создание кнопки перехода в окно добавления партнера
        add_partner_btn = QPushButton("Добавить нового партнера")
        # Назначение действия при нажатии на кнопку
        add_partner_btn.clicked.connect(
            # Вызов функции switch_frames() из Главного класса. Имя партнера не передается, Нам оно не требуется
            # Передается только имя Класса, который хотим открыть. БЕЗ СКОБОК!!! Скобки будут добавлены в switch_frames
            lambda: self.controller.switch_frames(CreatePartnerFrame.CreatePartnerClass)
        )

        self.main_frame_layout.addWidget(add_partner_btn)


    def add_picture(self):
        """
        Функция добавления фотографии
        :return: ничего не возвращается, фото будет помещено на экран внутри функции
        """

        # Создание области, которая будет хранить фото
        picture_place = QLabel()
        # Создание инструмента для считывания фото из файловой системы
        picture_read = QPixmap('/home/spirit2/Desktop/UpdateDemoexam/ICONS/icon.png')

        # Объекты внутри QLabel будут размером как сам QLabel
        picture_place.setScaledContents(True)
        # Установка размеров для QLabel
        picture_place.setFixedSize(52, 52)
        # Добавление фото в QLabel
        picture_place.setPixmap(picture_read)

        # Создание горизонтальной разметки для центровки фотки
        hbox = QHBoxLayout()
        hbox.addWidget(QWidget())
        hbox.addWidget(picture_place)
        hbox.addWidget(QWidget())

        # Добавление фото на экран
        self.main_frame_layout.addLayout(hbox)

    def calculate_discount(self, partner_name: str):
        """
        Функция для расчета скидки по заданию
        :param partner_name: Имя партнера, для которого рассчитывается скида
        :return: Число скидки
        """
        # Получение суммы продаж
        count = self.db.take_count_of_sales(partner_name)
        # Проверка по зданию
        if count == None:
            return 0
        elif count > 300_000:
            return 15
        elif count > 50_000:
            return 10
        elif count > 10000:
            return 5
        return 0

    def create_partners_cards(self):
        """
        Функция генерации карточек партнеров
        :return: возвращает контейнер QWidget(), который хранит в себе карточки QWidget()
        """

        # Создание контейнера для карточек
        cards_container = QWidget()
        # Назначение разметки для контейнера, чтобы карточки были вертикально расположены
        self.cards_container_layout = QVBoxLayout(cards_container)

        # Генерация карточек
        for partner_information in self.db.take_all_partners_info():
            # Создание карточки
            card = QWidget()
            # Назначение объектного имени для дизайна
            card.setObjectName(f"Card")

            # Создание разметки для карточки, чтобы текст размещался вертикально
            card_layout = QVBoxLayout()
            card.setLayout(card_layout)

            # Создание горизонтальной разметки для строки 'Тип | Наименование партнера          10%'
            card_top_level_hbox = QHBoxLayout()

            # Создание кнопки с типом партнера
            partner_type_btn = QPushButton(f"{partner_information['type']}")
            partner_type_btn.setObjectName("CardInfoButtonsTitle")
            partner_type_btn.clicked.connect(
                self.open_update_partner_frame
            )
            # Установка имени, по которому будет определяться партнер для редактирования
            partner_type_btn.setAccessibleName(partner_information['name'])

            # Разделительный знак
            partner_edge = QLabel(f"|")
            partner_edge.setObjectName("CardInfoButtonsTitle")

            # Кнопка с Наименованием партнера
            partner_name_btn = QPushButton(f"{partner_information['name']}")
            partner_name_btn.clicked.connect(
                self.open_update_partner_frame
            )
            partner_name_btn.setObjectName("CardInfoButtonsTitle")
            partner_name_btn.setAccessibleName(partner_information['name'])

            # Установка скидки (Кнопкой, чтобы была в один ряд с остальными)
            partner_discount = QPushButton(f"{self.calculate_discount(partner_information['name'])}%")
            partner_discount.setObjectName("CardInfoButtonsTitle")

            # Добавление элементов внутрь верхней планки
            card_top_level_hbox.addWidget(partner_type_btn)
            card_top_level_hbox.addWidget(partner_edge)
            card_top_level_hbox.addWidget(partner_name_btn)
            card_top_level_hbox.addStretch() # Добавляет разделение между объектами лейаута
            card_top_level_hbox.addWidget(partner_discount)

            partner_dir_btn = QPushButton(f"{partner_information['dir']}")
            partner_dir_btn.clicked.connect(
                self.open_update_partner_frame
            )
            # Создание горизонтальной разметки, чтобы сместить кнопку с директором в левый край
            dir_hbox = QHBoxLayout()
            dir_hbox.addWidget(partner_dir_btn)
            dir_hbox.addStretch()

            # Установка обджект имени со стилем
            partner_dir_btn.setObjectName("CardInfoButtons")
            partner_dir_btn.setAccessibleName(partner_information['name'])

            partner_phone_btn = QPushButton(f"+7 {partner_information['phone']}")
            partner_phone_btn.clicked.connect(
                self.open_update_partner_frame
            )
            # Аналогичное действие как и с кнопкой директора
            phone_hbox = QHBoxLayout()
            phone_hbox.addWidget(partner_phone_btn)
            phone_hbox.addStretch()

            partner_phone_btn.setObjectName("CardInfoButtons")
            partner_phone_btn.setAccessibleName(partner_information['name'])

            partner_rate_btn = QPushButton(f"Рейтинг: {partner_information['rate']}")
            partner_rate_btn.clicked.connect(
                self.open_update_partner_frame
            )
            # Аналогично с кнопкой директора
            rate_hbox = QHBoxLayout()
            rate_hbox.addWidget(partner_rate_btn)
            rate_hbox.addStretch()

            partner_rate_btn.setObjectName("CardInfoButtons")
            partner_rate_btn.setAccessibleName(partner_information['name'])

            # Кнопка истории партнера
            partner_history_btn = QPushButton("История партнера")
            partner_history_btn.setAccessibleName(partner_information["name"])
            partner_history_btn.clicked.connect(
                self.open_partner_history_frame
            )


            card_layout.addLayout(card_top_level_hbox)
            card_layout.addLayout(dir_hbox)
            card_layout.addLayout(phone_hbox)
            card_layout.addLayout(rate_hbox)
            card_layout.addWidget(partner_history_btn)

            # Добавление карточки в разметку КОНТЕЙНЕРА
            self.cards_container_layout.addWidget(card)

        # Возвращение контейнера в то место, где вызывают функцию
        return cards_container

    def open_partner_history_frame(self):
        """
        Функция для вызова метода перехода между окнами, и передачи в него имени партнера
        :return: Ничего не возвращается
        """
        # Определение кнопки, с которой вызвалась функция
        sender = self.sender()
        # Определение Имени этой кнопки, в котором записано имя Партнера
        partner_name = sender.accessibleName()
        # Вызов функции switch_frames
        self.controller.switch_frames(HistoryFrame.PartnerHistoryClass, partner_name)


    def open_update_partner_frame(self):
        """
        Обработчик нажатий на кнопки
        :return:
        """
        sender = self.sender()
        sender_name = sender.accessibleName()
        print("SENDER ACCS NAMe:", sender_name)
        self.controller.switch_frames(UpdatePartnerFrame.UpdatePartnerClass, sender_name)


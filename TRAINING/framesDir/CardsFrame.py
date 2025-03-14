from PySide6.QtWidgets import (QFrame,
                               QWidget, QScrollArea, QPushButton, QVBoxLayout, QLabel, QHBoxLayout)
from PySide6.QtGui import QPixmap

# from TRAINING.framesDir import UpdatePartnerInfo, CreatePartner, HistoryFrame
from TRAINING.framesDir import CreateAndUpdatePartnerFrame, HistoryFrame


class PartnersCardsFrameClass(QFrame):
    def __init__(self, controller):
        QFrame.__init__(self)
        self.controller = controller
        self.database = controller.database_var
        print("DB from Frame:", self.database)


        self.main_layout = QVBoxLayout(self)
        self.setup_ui()

    def setup_ui(self):
        """
        Функция для генерации интерфейса
        :return: Ничего
        """
        title = QLabel("Заголовок")
        title.setObjectName("Title")
        self.main_layout.addWidget(title)
        self.create_icon()

        # Добавление области с карточками
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.create_cards())
        self.main_layout.addWidget(scroll_area)

        # create_partner_btn = QPushButton("Добавить партнера")
        # create_partner_btn.clicked.connect(
        #     lambda : self.controller.switch_frames(CreatePartner.CreatePartnerClass)
        # )
        #
        #
        # self.main_layout.addWidget(create_partner_btn)


    def create_icon(self):
        """
        Функция создания иконки
        :return: Ничего
        """
        icon_socket = QLabel()
        icon_socket.setScaledContents(True)
        icon_socket.setFixedSize(64, 64)
        icon = QPixmap("/home/spirit2/Desktop/UpdateDemoexam/ICONS/icon.png")

        hbox = QHBoxLayout()
        hbox.addWidget(QWidget())
        hbox.addWidget(icon_socket)
        hbox.addWidget(QWidget())

        icon_socket.setPixmap(icon)
        self.main_layout.addLayout(hbox)

    def take_discount(self, partner_name: str):
        """
        Функция расчета скидки
        :param partner_name: Имя конкретного партнера
        :return: Ничего
        """
        count = self.database.take_sales_sum(partner_name)
        if count == None:
            return 0
        elif count >= 300000:
            return 15
        elif count >= 50000:
            return 10
        elif count >= 10000:
            return 5
        return 0


    def create_cards(self):
        """
        Функция для создания карточек партнера
        :return: Большой Widget с карточками
        """
        big_widget = QWidget()
        big_widget_layout = QVBoxLayout(big_widget)


        for element in self.database.take_all_partners():
            card = QWidget()
            card.setObjectName("card")
            card_layout = QVBoxLayout(card)

            hbox = QHBoxLayout()

            type_name = QLabel(f"{element['type']} | {element['name']}")
            type_name.setStyleSheet("QLabel {font-size: 25px; padding-left: 20px;}")
            hbox.addWidget(type_name)

            discount = QLabel(f"{self.take_discount(element['name'])}%")
            discount.setStyleSheet("QLabel {font-size: 25px; qproperty-alignment: AlignRight; padding-right: 20px;}")
            hbox.addWidget(discount)

            card_layout.addLayout(hbox)
            card_layout.addWidget(QLabel(f"{element['dir']}", objectName="DIRRECTOR"))
            card_layout.addWidget(QLabel(f"+7 {element['phone']}"))
            card_layout.addWidget(QLabel(f"Рейтинг: {element['rate']}"))

            open_update_window_button = QPushButton("Редактировать")
            open_update_window_button.setObjectName(element['name'])
            open_update_window_button.clicked.connect(
                self.open_frame_to_update
            )
            card_layout.addWidget(open_update_window_button)

            open_history_window_button = QPushButton("История")
            open_history_window_button.setObjectName(element['name'])
            open_history_window_button.clicked.connect(
                self.open_history_frame
            )
            card_layout.addWidget(open_history_window_button)

            big_widget_layout.addWidget(card)

        return big_widget

    def open_frame_to_update(self):
        """
        Обработчик нажатия на кнопку
        :return: Ничего
        """

        sender = self.sender()

        print("SENDER:", sender)
        sender_name = sender.objectName()
        print("SENDER NAME:", sender_name)
        self.controller.switch_frames(CreateAndUpdatePartnerFrame.CreateUpdatePartnerClass, sender_name)

    def open_history_frame(self):
        """
        Обработчик нажатия на кнопку
        :return: Ничего
        """

        sender = self.sender()
        print("SENDER:", sender)
        sender_name = sender.objectName()
        print("SENDER NAME:", sender_name)
        self.controller.switch_frames(HistoryFrame.HistoryFrameClass, sender_name)









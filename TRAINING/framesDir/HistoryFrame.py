from PySide6.QtWidgets import (QFrame, QTreeWidget, QTreeWidgetItem,
                               QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout)
from PySide6.QtGui import QPixmap

from TRAINING.framesDir import CardsFrame

from PartnerStatic import Partner


class HistoryFrameClass(QFrame):
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
        title = QLabel("История продаж партнера")
        title.setObjectName("Title")
        self.main_layout.addWidget(title)

        table = QTreeWidget()
        table.setHeaderLabels(["Продукция", "Партнер", "Количество", "Дата"])

        for data in self.database.take_history(Partner.get_name()):
            item = QTreeWidgetItem(table)
            item.setText(0, f"{data['Продукт']}")
            item.setText(1, f"{data['Партнер']}")
            item.setText(2, f"{data['Количество']}")
            item.setText(3, f"{data['Дата']}")

        self.main_layout.addWidget(table)


        back_btn = QPushButton("Назад")
        back_btn.clicked.connect(
            lambda : self.controller.switch_frames(CardsFrame.PartnersCardsFrameClass)
        )
        self.main_layout.addWidget(back_btn)



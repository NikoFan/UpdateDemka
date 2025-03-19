from PySide6.QtWidgets import (
QFrame, QPushButton, QLabel, QTreeWidget, QTreeWidgetItem, QVBoxLayout
)

from PartnerStatic import Partner
from FRAMES import PartnersCardFrame

class PartnerHistoryClass(QFrame):
    def __init__(self, controller):
        QFrame.__init__(self)
        self.controller = controller
        self.database = controller.db

        self.frame_layout = QVBoxLayout(self)
        self.setup_ui()

    def setup_ui(self):
        """
        Генерация интерфейса
        :return:
        """
        title = QLabel(f"История {Partner.get_name()}")
        title.setObjectName("Title")
        self.frame_layout.addWidget(title)


        table = QTreeWidget()
        table.setHeaderLabels(["Продукция", "Количество", "Дата продажи"])

        for data in self.database.take_partner_history_info(Partner.get_name()):
            item = QTreeWidgetItem(table)
            item.setText(0, data['product'])
            item.setText(1, str(data['count']))
            item.setText(2, str(data['data']))

        self.frame_layout.addWidget(table)

        back_btn = QPushButton("Назад")
        back_btn.clicked.connect(
            lambda: self.controller.switch_frames(PartnersCardFrame.PartnerCardsClass)
        )
        self.frame_layout.addWidget(back_btn)
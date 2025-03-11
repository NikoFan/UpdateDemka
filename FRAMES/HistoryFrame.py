from PySide6.QtWidgets import QVBoxLayout, QLabel,  QPushButton, QTreeWidget,  QTreeWidgetItem, QFrame
import PartnerStatic
from DATABASE import Database
from FRAMES import PartnerInfoFrame

class HistoryClass(QFrame):
    # конструктор класса
    def __init__(self, main_class_controller):
        super().__init__()
        # создание переменной, для взаимодействия с main_class_controller во всем классе
        self.controller = main_class_controller
        self.db: Database.Database = main_class_controller.db

        # создание разметки фрейма
        self.main_frame_layout = QVBoxLayout(self)
        self.setup_ui()

    # метод установки полей
    def setup_ui(self):
        # создание текстового поля
        title_label = QLabel("История продаж партнера")
        # назначение объектного имени для стилизации объекта
        title_label.setObjectName("Title")
        # добавление текстового поля на фрейм
        self.main_frame_layout.addWidget(title_label)

        # создание таблицы
        table = QTreeWidget()
        # создание заголовков для колонок
        table.setHeaderLabels(['Продукция', 'Партнер', 'Количество продукции', 'Дата'])
        # добавление таблицы на фрейм
        self.main_frame_layout.addWidget(table)

        # цикл заполнения таблицы данными из БД
        for data in self.db.take_sales_info(PartnerStatic.Partner.get_name()):
            item = QTreeWidgetItem(table)
            item.setText(0, data['product'])
            item.setText(1, data['partner'])
            item.setText(2, str(data['count']))
            item.setText(3, str(data['date']))


        # создание кнопки для возврата назад
        back_btn = QPushButton("Назад")
        # добавление действия при нажатии на кнопку
        back_btn.clicked.connect(
            lambda : self.controller.switch_frames(PartnerInfoFrame.PartnerInfoClass)
        )
        # Добавление кнопки в разметку фрейма
        self.main_frame_layout.addWidget(back_btn)
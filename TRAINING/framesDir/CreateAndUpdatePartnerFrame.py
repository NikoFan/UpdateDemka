from PySide6.QtWidgets import (QFrame, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit,
                               QComboBox, QPushButton)

from SendMessageBox import *
from PartnerStatic import Partner
from TRAINING.framesDir import CardsFrame
class CreateUpdatePartnerClass(QFrame):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.database = controller.database_var
        self.frame_layout = QVBoxLayout(self)
        self.setup_ui()

    def setup_ui(self):
        """
        Генерация интерфейса окна
        :return: Ничего
        """
        split_widget = QWidget()
        split_hbox = QHBoxLayout(split_widget)

        create_side = QWidget()
        self.create_side_layout = QVBoxLayout(create_side)
        self.fill_create_side()
        split_hbox.addWidget(create_side)


        update_side = QWidget()
        self.update_side_layout = QVBoxLayout(update_side)
        self.fill_update_side()
        split_hbox.addWidget(update_side)

        back_btn = QPushButton("Назад")
        back_btn.clicked.connect(
            lambda : self.controller.switch_frames(CardsFrame.PartnersCardsFrameClass)
        )

        self.frame_layout.addWidget(split_widget)
        self.frame_layout.addWidget(back_btn)

    def fill_update_side(self):
        """
        Заполнение области обновления
        :return: ничего
        """
        title = QLabel("Обновление партнера")
        title.setObjectName("Title")
        self.update_side_layout.addWidget(title)
        self.partner_late_data = self.controller.database_var.take_partner(Partner.get_name())[0]

        def create_edit_line_pattern(text: str, max_len: int):
            """
            Функция создания поля для ввода
            :param placeholder_text: Исчезающий текст
            :param max_len: Длина ввода
            :return: QLineEdit
            """
            edit = QLineEdit()
            edit.setMaxLength(max_len)
            edit.setText(text)
            self.update_side_layout.addWidget(edit)
            return edit

        def create_label_pattern(text: str):
            label = QLabel(text)
            self.update_side_layout.addWidget(label)

        create_label_pattern("Введите имя партнера")
        self.partner_name_update = create_edit_line_pattern(self.partner_late_data["name"], 100)

        create_label_pattern("Введите тип партнера")
        self.partner_type_update = QComboBox()
        self.partner_type_update.addItems(["ООО", "ОАО", "ПАО", "ЗАО"])
        self.update_side_layout.addWidget(self.partner_type_update)

        create_label_pattern("Введите фио директора")
        self.partner_dir_update = create_edit_line_pattern(self.partner_late_data["dir"], 100)

        create_label_pattern("Введите почту партнера")
        self.partner_mail_update = create_edit_line_pattern(self.partner_late_data["mail"], 100)

        create_label_pattern("Введите телефон партнера")
        self.partner_phone_update = create_edit_line_pattern(self.partner_late_data["phone"], 13)
        self.partner_phone_update.setInputMask("+7 000 000 00 00")

        create_label_pattern("Введите адрес партнера")
        self.partner_addr_update = create_edit_line_pattern(self.partner_late_data["addr"], 300)

        create_label_pattern("Введите рейтинг партнера")
        self.partner_rate_update = create_edit_line_pattern(self.partner_late_data["rate"], 2)

        update_btn = QPushButton("Редактировать")
        update_btn.clicked.connect(
            self.update_partner
        )
        self.update_side_layout.addWidget(update_btn)

    def fill_create_side(self):
        """
        Заполнение области добавления
        :return: ничего
        """
        title = QLabel("Добавление партнера")
        title.setObjectName("Title")
        self.create_side_layout.addWidget(title)

        def create_edit_line_pattern(placeholder_text: str, max_len: int):
            """
            Функция создания поля для ввода
            :param placeholder_text: Исчезающий текст
            :param max_len: Длина ввода
            :return: QLineEdit
            """
            edit = QLineEdit()
            edit.setMaxLength(max_len)
            edit.setPlaceholderText(placeholder_text)
            self.create_side_layout.addWidget(edit)
            return edit

        def create_label_pattern(text: str):
            label = QLabel(text)
            self.create_side_layout.addWidget(label)

        create_label_pattern("Введите имя партнера")
        self.partner_name_create = create_edit_line_pattern("Введите имя партнера", 100)

        create_label_pattern("Введите тип партнера")
        self.partner_type_create = QComboBox()
        self.partner_type_create.addItems(["ООО", "ОАО", "ПАО", "ЗАО"])
        self.create_side_layout.addWidget(self.partner_type_create)

        create_label_pattern("Введите фио директора")
        self.partner_dir_create = create_edit_line_pattern("Введите фио директора", 100)

        create_label_pattern("Введите почту партнера")
        self.partner_mail_create = create_edit_line_pattern("Введите почту партнера", 100)

        create_label_pattern("Введите телефон партнера")
        self.partner_phone_create = create_edit_line_pattern("Введите телефон партнера", 13)
        self.partner_phone_create.setInputMask("+7 000 000 00 00")

        create_label_pattern("Введите адрес партнера")
        self.partner_addr_create = create_edit_line_pattern("Введите адрес партнера", 300)

        create_label_pattern("Введите ИНН партнера")
        self.partner_inn_create = create_edit_line_pattern("Введите ИНН партнера", 10)

        create_label_pattern("Введите рейтинг партнера")
        self.partner_rate_create = create_edit_line_pattern("Введите рейтинг партнера", 2)

        create_btn = QPushButton("Добавить")
        create_btn.clicked.connect(
            self.add_partner
        )
        self.create_side_layout.addWidget(create_btn)

    def update_partner(self):
        partners_data = {
            "type": self.partner_type_update.currentText(),
            "name": self.partner_name_update.text(),
            "dir": self.partner_dir_update.text(),
            "mail": self.partner_mail_update.text(),
            "phone": self.partner_phone_update.text()[3:],
            "addr": self.partner_addr_update.text(),
            "inn": self.partner_late_data["inn"],
            "rate": self.partner_rate_update.text(),
        }

        if send_W_message("Проверьте данные! Вы точно хотите обновить партнера?") < 20_000:

            if self.controller.database_var.update_partner_data(partners_data, Partner.get_name()):
                send_I_message("Партнер обновлен")
                return
            send_C_message("Ошибка при обработке данных! Проверьте ввод!")
            return

    def add_partner(self):
        partners_data = {
            "type":self.partner_type_create.currentText(),
            "name":self.partner_name_create.text(),
            "dir":self.partner_dir_create.text(),
            "mail":self.partner_mail_create.text(),
            "phone":self.partner_phone_create.text()[3:],
            "addr":self.partner_addr_create.text(),
            "inn":self.partner_inn_create.text(),
            "rate":self.partner_rate_create.text(),
        }

        if send_W_message("Проверьте данные! Вы точно хотите создать партнера?") < 20_000:

            if self.controller.database_var.create_partner_data(partners_data):
                send_I_message("Партнер добавлен")
                return
            send_C_message("Ошибка при обработке данных! проверьте ввод!")
            return


from PySide6.QtWidgets import (QFrame, QLineEdit, QWidget, QLabel, QVBoxLayout, QPushButton, QComboBox)

from PartnerStatic import Partner
from SendMessageBox import *

from FRAMES import PartnersCardFrame

class CreatePartnerClass(QFrame):
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

        title = QLabel("Добавление партнера")
        title.setObjectName("Title")
        self.frame_layout.addWidget(title)
        self.create_label_pattern("Введите наименование")
        self.partner_name = self.create_edit_pattern("Введите...", 100)

        self.create_label_pattern("Укажите тип")
        self.partner_type = QComboBox()
        self.partner_type.addItems(["ООО", "ЗАО", "ПАО", "ОАО"])
        self.frame_layout.addWidget(self.partner_type)

        self.create_label_pattern("Введите рейтинг")
        self.partner_rate = self.create_edit_pattern("Введите...", 2)

        self.create_label_pattern("Введите адрес")
        self.partner_addr = self.create_edit_pattern("Введите...", 300)

        self.create_label_pattern("Введите ФИО директора")
        self.partner_dir = self.create_edit_pattern("Введите...", 100)

        self.create_label_pattern("Введите телефон")
        self.partner_phone = self.create_edit_pattern("Введите...", 13)
        self.partner_phone.setInputMask("+7 000 000 00 00")

        self.create_label_pattern("Введите почта")
        self.partner_mail = self.create_edit_pattern("Введите...", 100)

        self.create_label_pattern("Введите ИНН")
        self.partner_inn = self.create_edit_pattern("Введите...", 10)

        create_btn = QPushButton("Добавить")
        create_btn.clicked.connect(
            self.create_partner
        )
        self.frame_layout.addWidget(create_btn)

        back_btn = QPushButton("Назад")
        back_btn.clicked.connect(
            lambda : self.controller.switch_frames(PartnersCardFrame.PartnerCardsClass)
        )
        self.frame_layout.addWidget(back_btn)

    def create_partner(self):
        """
        Создание партнера
        :return:
        """

        # Создание словаря, который отправится на редактирование.
        partner_input_data = {
            'type': self.partner_type.currentText(),
            'name': self.partner_name.text(),
            'dir': self.partner_dir.text(),
            'mail': self.partner_mail.text(),
            'phone': self.partner_phone.text()[3:],
            'addr': self.partner_addr.text(),
            'inn': self.partner_inn.text(),
            'rate': self.partner_rate.text(),
        }

        if send_W_message("Вы точно хотите добавить партнера? Проверьте данные перед созданием!") < 20000:
            if self.database.add_new_partner(partner_input_data):
                Partner.set_name(self.partner_name.text())
                send_I_message("Партнер добавлен!")
                return
            send_C_message("Ошибка Добавления! Проверьте данные!")
            return

    def create_label_pattern(self, text: str):
        """
        Шаблон создания текстового поля
        :param text: текст
        :return:
        """

        label = QLabel(text)
        label.setObjectName("Hint_label")
        self.frame_layout.addWidget(label)

    def create_edit_pattern(self, text, max_len):
        """
        Шаблон создания ввода пользователя
        :param text: Исчезающий текст
        :param max_len: Максимальная длина
        :return: edit
        """

        edit = QLineEdit()
        edit.setPlaceholderText(text)
        edit.setMaxLength(max_len)
        edit.setObjectName("EditLine")
        self.frame_layout.addWidget(edit)

        return edit

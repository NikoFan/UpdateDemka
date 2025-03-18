from PySide6.QtWidgets import (QFrame, QLineEdit, QWidget, QLabel, QVBoxLayout, QPushButton, QComboBox)

from PartnerStatic import Partner
from SendMessageBox import *

from FRAMES import PartnersCardFrame

class UpdatePartnerClass(QFrame):
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

        # Создается self. чтобы в дальнейшем использовать в функции обновления
        self.partner_data = self.database.take_partner_info(Partner.get_name())

        title = QLabel("Редактирование партнера")
        title.setObjectName("Title")
        self.frame_layout.addWidget(title)
        self.create_label_pattern("Обновите наименование")
        self.partner_name = self.create_edit_pattern(self.partner_data['name'], 100)

        self.create_label_pattern("Обновите тип")
        self.partner_type = QComboBox()

        # Готовый список с типами партнера
        types_part = ["ООО", "ЗАО", "ПАО", "ОАО"]
        # Удаление дубликата (того типа, который у партнера)
        types_part.remove(self.partner_data['type'])

        # Сложение списков, происходит поочередно. Результат: ["ТИП ПАРТНЕРА"] + ["Остальные типы 1", "Остальные типы 2"]
        self.partner_type.addItems([self.partner_data['type']] + types_part)
        self.frame_layout.addWidget(self.partner_type)

        self.create_label_pattern("Обновите рейтинг")
        self.partner_rate = self.create_edit_pattern(self.partner_data['rate'], 2)

        self.create_label_pattern("Обновите адрес")
        self.partner_addr = self.create_edit_pattern(self.partner_data['addr'], 300)

        self.create_label_pattern("Обновите ФИО директора")
        self.partner_dir = self.create_edit_pattern(self.partner_data['dir'], 100)

        self.create_label_pattern("Обновите телефон")
        self.partner_phone = self.create_edit_pattern(self.partner_data['phone'], 13)
        self.partner_phone.setInputMask("+7 000 000 00 00")

        self.create_label_pattern("Обновите почта")
        self.partner_mail = self.create_edit_pattern(self.partner_data['mail'], 100)

        update_btn = QPushButton("Редактировать")
        update_btn.clicked.connect(
            self.update_partner
        )
        self.frame_layout.addWidget(update_btn)

        back_btn = QPushButton("Назад")
        back_btn.clicked.connect(
            lambda : self.controller.switch_frames(PartnersCardFrame.PartnerCardsClass)
        )
        self.frame_layout.addWidget(back_btn)

    def update_partner(self):
        """
        Обновление партнера
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
            'inn': self.partner_data['inn'],
            'rate': self.partner_rate.text(),
        }

        if send_W_message("Вы точно хотите обновить партнера? Проверьте данные перед обновлением!") < 20000:
            if self.database.update_partner(partner_input_data, Partner.get_name()):
                Partner.set_name(self.partner_name.text())
                send_I_message("Партнер обновлен!")
                return
            send_C_message("Ошибка обновления! Проверьте данные!")
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
        :param text: Стартовый текст
        :param max_len: Максимальная длина
        :return: edit
        """

        edit = QLineEdit()
        edit.setText(text)
        edit.setMaxLength(max_len)
        edit.setObjectName("EditLine")
        self.frame_layout.addWidget(edit)

        return edit

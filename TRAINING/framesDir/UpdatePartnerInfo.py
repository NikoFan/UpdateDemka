from PySide6.QtWidgets import (QFrame, QLineEdit, QComboBox,
                               QWidget, QScrollArea, QPushButton, QVBoxLayout, QLabel, QHBoxLayout)

from PartnerStatic import Partner
from TRAINING.framesDir import CardsFrame
from SendMessageBox import *


class UpdatePartnerCardClass(QFrame):
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
        title = QLabel("Редактирование партнера")
        title.setObjectName("Title")

        partner_data = self.database.take_partner(Partner.get_name())[0]

        self.main_layout.addWidget(title)


        self.create_label_pattern("Введите наименование партнера")
        self.partner_name = self.create_qline_edit_pattern(partner_data["name"], 100)

        self.create_label_pattern("Введите Тип партнера")
        self.partner_type = QComboBox()
        self.partner_type.addItems(["ООО", "ПАО", "ЗАО", "ОАО"])
        self.main_layout.addWidget(self.partner_type)

        self.create_label_pattern("Введите рейтинг партнера")
        self.partner_rate = self.create_qline_edit_pattern(partner_data["rate"], 2)

        self.create_label_pattern("Введите юридический адресс партнера")
        self.partner_addr = self.create_qline_edit_pattern(partner_data["addr"], 300)

        self.create_label_pattern("Введите ФИО Директора партнера")
        self.partner_dir = self.create_qline_edit_pattern(partner_data["dir"], 100)

        self.create_label_pattern("Введите Телефон партнера")
        self.partner_phone = self.create_qline_edit_pattern(partner_data["phone"], 13)
        self.partner_phone.setInputMask("+7 000 000 00 00")


        self.create_label_pattern("Введите Почту электронную партнера")
        self.partner_email = self.create_qline_edit_pattern(partner_data["mail"], 100)

        self.create_label_pattern("Введите ИНН партнера")
        self.partner_inn = self.create_qline_edit_pattern(partner_data["inn"], 10)

        update_btn = QPushButton("Редактировать")
        update_btn.clicked.connect(
            self.update_partner_info
        )
        self.main_layout.addWidget(update_btn)

        back_btn = QPushButton("Назад")
        back_btn.clicked.connect(
            lambda : self.controller.switch_frames(CardsFrame.PartnersCardsFrameClass)
        )
        self.main_layout.addWidget(back_btn)

    def update_partner_info(self):
        """
        Функция отправки данных на редактирование
        :return: Ничего
        """
        partner_input_data = {
            "name": self.partner_name.text(),
            "type": self.partner_type.currentText(),
            "dir": self.partner_dir.text(),
            "mail": self.partner_email.text(),
            "inn": self.partner_inn.text(),
            "rate": self.partner_rate.text(),
            "addr": self.partner_addr.text(),
            "phone": self.partner_phone.text()[3:]
        }
        if send_W_message("Проверьте введенные данные. Тип партнера мог поменять значение!") < 20_000:
            # Редактирование
            if self.database.update_partner_data(partner_input_data, Partner.get_name()):
                send_I_message("Обновление прошло успешно!")
                return
            send_C_message("Ошибка редактирования! Проверьте данные!")
            return
        else:
            return




    def create_label_pattern(self, message):
        """
        Лейблы для подсказки
        :param message: Текст подсказки
        :return: Ничего
        """
        text_hint = QLabel(message)
        text_hint.setObjectName("hint_text")
        self.main_layout.addWidget(text_hint)


    def create_qline_edit_pattern(self, start_text, max_len):
        """
        Функция создания ввода для пользователя
        :param start_text: Стартовый текст
        :param max_len: Максимальная длина текста
        :return: Поле для ввода
        """

        line_edit = QLineEdit(start_text)
        line_edit.setObjectName("line_edit")
        line_edit.setMaxLength(max_len)
        self.main_layout.addWidget(line_edit)

        return line_edit
















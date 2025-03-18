# pip install PySide6
from PySide6.QtWidgets import (
    QWidget,  # На основе QWidget создается макет приложения
    QStackedWidget,  # Хранит в себе фреймы, нужен для переходов между ними
    QVBoxLayout,  # В данном классе размещает в окне фреймы из QStackedWidget
    QApplication  # Создает объект 'Приложение' в системе
)

import sys  # Библиотека для работы с системой

from FRAMES import PartnersCardFrame

from DATABASE import Database

from PartnerStatic import Partner  # Добавление статического класса

from SendMessageBox import *


class MainApplicationClass(QWidget):
    def __init__(self):  # Конструктор класса MainApplication
        # Возможны 3 варианта подключения Родительского класса (QWidget)

        # super().__init__() # super() - Класс, указанный как родительский (В данном случае - QWidget)
        # QWidget().__init__() # Если при вызове Родительского класса добавить скобки - Не надо добавлять self в __init__()
        QWidget.__init__(self)  # Вызов Родительского класса прямым указанием его имени (не super())

        # Установка заголовка приложения
        self.setWindowTitle("Мастер Пол")
        # Установка стартовых размеров приложения
        self.resize(800, 600)

        # Вызов класса Database()
        self.db = Database.Database()

        # Создание контейнера для фреймов
        self.frames_container = QStackedWidget()

        # Вызов класса первого фрейма
        partner_cards_frame = PartnersCardFrame.PartnerCardsClass(self) # self - параметр аргумента main_class_controller
        # Добавление класса фрейма в контейнер фреймов
        self.frames_container.addWidget(partner_cards_frame)

        # Создание разметки для класса MainApplicationClass, которая будет размещать фреймы из self.frame_container
        layout = QVBoxLayout(self)  # Разметка присваивается к классу, путем указания self в скобках
        # self.setLayout(layout) # 2й вариант присвоения разметки к объекту класса MainApplicationClass
        layout.addWidget(
            self.frames_container)  # Добавление контейнера с фреймами в разметку (выбранный фрейм автоматически разместится в ней)

    def switch_frames(self, need_frame_name, partner_name=None):
        """
        Функция переключения Фреймов
        :param need_frame_name: Имя целевого класса, который хранит целевой фрейм. Класс передается без скобок
        :param partner_name: Имя партнера, которого хотим просмотреть (Для открытия карточки партнера) по умолчанию - пустое
        :return: Ничего не возращается
        """
        # Проверка имени партнера
        if partner_name:
            # Если имя партнера не None - передали имя партнера, и его надо записать в статический класс
            Partner.set_name(partner_name)  # Запись имени партнера в статический класс

        # Вызов класса целевого фрейма
        goal_frame = need_frame_name(self)



        # Удаление старых дубликатов целевого фрейма из контейнера
        self.frames_container.removeWidget(goal_frame)
        # Добавление целевого фрейма в контейнер
        self.frames_container.addWidget(goal_frame)
        # Установка целевого фрейма Текущим, чтобы он демонстрировался на экране
        self.frames_container.setCurrentWidget(goal_frame)

    def closeEvent(self, event):
        """
        Функция контролирует выход из приложения, и задает вопрос пользователю
        :param event: Действие - выход
        :return: Ничего не возвращается
        """
        # Если пользователь ответил Да (UID ДА - 16000)
        if send_W_message("Вы точно хотите выйти?") < 20000:
            event.accept()
        # Если пользователь ответил Нет (UID НЕТ - 60000)
        else:
            event.ignore()


# #67BA80 - Акцентирование внимания
# #F4E8D3 - Дополнительный фон
# #FFFFFF - Основной фон
# Segoe UI - Шрифт
# Стили для приложения
styles_sheet = '''
QPushButton {
background: #67BA80;
color: #000000;
}

QLineEdit {
font-size: 15px;
}


#CardInfoButtonsTitle {
background: none;
color: black;
border: none;
font-size: 20px;
}

#CardInfoButtons {
background: none;
color: black;
border: none;
}

#Title {
font-size: 20px;
qproperty-alignment: AlignCenter;
}

#Hint_label {
font-size: 18px;
padding: 10px, 0px, 0px, 0px;
font-weight: bold;
}

#EditLine {
font-size: 18px;
font-weight: bold;
}

#Main_label {
font-size: 15px;
}

#Card_label {
font-size: 15px;
}

#Card {
border: 2px solid black;
}

#Top_lvl_label {
font-size: 30px;
}

'''

# Создание "Приложения" в системе
application = QApplication(sys.argv)
# Подключение стилий
application.setStyleSheet(styles_sheet)
# Установка шрифта из Задания
application.setFont('Segoe UI')
# Вызов класса MainApplicationClass, помещая объект класса в переменную main_class_object
main_class_object = MainApplicationClass()
# Визуализация класса
main_class_object.show()
# Запуск приложения в системе, чтобы оно работало и не сворачивалось
application.exec()

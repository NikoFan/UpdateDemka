from PySide6.QtWidgets import QApplication, QWidget, QStackedWidget, QVBoxLayout
import sys

from framesDir import CardsFrame
from DatabaseDir import DatabaseFile
from PartnerStatic import Partner

class Application(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Мастер пол")
        self.resize(800, 600)
        self.database_var = DatabaseFile.DatabaseMainClass()
        print("DB from App:", self.database_var)

        first_frame = CardsFrame.PartnersCardsFrameClass(controller=self)

        self.frames_container = QStackedWidget()
        self.frames_container.addWidget(first_frame)

        vbox = QVBoxLayout(self)

        vbox.addWidget(self.frames_container)


    def switch_frames(self, frame, partner_name: str = None):
        """
        Функция перехода между фреймами
        :param frame: Имя фрейма \ ClassFile.ClassName
        :param partner_name: Имя партнера
        :return: Ничего
        """
        if partner_name != None:
            # Добавление в статический класс
            Partner.set_name(partner_name)


        # Переход между окнами
        new_frame = frame(controller=self)
        self.frames_container.removeWidget(new_frame)
        self.frames_container.addWidget(new_frame)
        self.frames_container.setCurrentWidget(new_frame)


style_sheet = """
QPushButton {
background: #67BA80;
color: black;
font-size: 20px;
}

#Title {
qproperty-alignment: AlignCenter;
font-size: 30px;
}

#card {
border: 2px solid white;
}

#hint_text {
padding-left: 20px;
font-size: 20px;
font-weight: bold;
}



"""


app = QApplication(sys.argv)
app.setStyleSheet(style_sheet)
main_class = Application()
app.setFont('Segoe UI')
main_class.show()
app.exec()
import sys
from PyQt5 import uic
from PyQt5.QtCore import QByteArray
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QImage, QPixmap
import requests


class MapApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('map.ui', self)
        #Signals
        self.search_btn.clicked.connect(self.update_map)
        self.reset_btn.clicked.connect(self.reset_map)
        #vars

        self.map_img_api_server = 'http://static-maps.yandex.ru/1.x/'

    def get_map_type(self):
        text = self.map_view_cmbox.currentText()
        match text:
            case 'scheme':
                return 'map'
            case 'satellite':
                return 'sat'
            case 'hybrid':
                return 'skl'
    def reset_map(self):
        self.coords_le.clear()
        self.snp_le.clear()
        self.map_widget.clear()

    def generate_link(self):
        ll = self.coords_le.text()
        snp = self.snp_le.text()
        map_type = self.get_map_type()
        args = {
          'll': ll,
          'snp': snp,
          'l': map_type,
        }
        print(args)
        return args

    def update_map(self):
        map = self.get_map(self.generate_link())
        self.map_widget.setPixmap(QPixmap.fromImage(map))

    def get_map(self, args, lnk=None):
        response = requests.get(self.map_img_api_server, params=args)
        map_img = response.content
        print(response.url)
        if response:
            return QImage.fromData(QByteArray(map_img))
        else:
            print(response.url)
            print(f'Ошибка #{response.status_code}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MapApp()
    form.show()
    sys.exit(app.exec())
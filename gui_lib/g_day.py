from email.mime import base
from sort_lib.day import Day
import gui_lib.g_main_window
from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal, pyqtSlot
# from PyQt6.QtGui import 

class GDay(QWidget):

    def __init__(self, model: Day, base_layout: QBoxLayout, base_gparent: 'gui_lib.g_main_window.GMainWindow'):
        super().__init__()
        self._model = model
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(QLabel('Day'))
        self.base_gparent = base_gparent
        base_layout.addWidget(self)
        # TODO:
    

    @property
    def model(self):
        return self._model
from email.mime import base
from sort_lib.day import Day
import gui_lib.g_main_window
from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal, pyqtSlot
# from PyQt6.QtGui import 

class GDay(QFrame):

    def __init__(self, model: Day, base_layout: QBoxLayout, base_gparent: 'gui_lib.g_main_window.GMainWindow'):
        super().__init__()
        self._model = model
        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(3)
        self.setLayout(QGridLayout())
        for i in range(len(base_gparent.model.subjects)):
            btn = QPushButton(base_gparent.model.subjects[i])
            btn.setCheckable(True)
            self.layout().addWidget(btn, i // 5, i % 5)
        self.base_gparent = base_gparent
        base_layout.insertWidget(base_layout.count() - 1, self)
    

    @property
    def model(self):
        return self._model
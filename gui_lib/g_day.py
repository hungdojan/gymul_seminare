from sort_lib.day import Day
import gui_lib.g_main_window
from PySide6.QtWidgets import *
from PySide6.QtCore import Signal, Slot

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
            btn.toggled.connect(self.button_toggle)
            self.layout().addWidget(btn, i // 5, i % 5)
        self._base_gparent = base_gparent
        base_layout.insertWidget(base_layout.count() - 1, self)
    

    @property
    def model(self):
        return self._model
    

    @Slot()
    def button_toggle(self):
        btn: QPushButton = self.sender()
        if btn.isChecked():
            self._model.add_subject_name(btn.text())
        else:
            self._model.remove_subject(btn.text())
        print(list(map(lambda x: x.name, self._model.subjects)))
        self._base_gparent.content_refreshed.emit()
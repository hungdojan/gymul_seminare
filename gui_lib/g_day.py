from sort_lib.day import Day
import gui_lib.g_main_window
from gui_lib.g_subject import GSubject
from PySide6.QtWidgets import *
from PySide6.QtCore import Signal, Slot, Qt
from PySide6.QtGui import QPaintEvent, QPainter, QMouseEvent

class GDay(QFrame):

    def __init__(self, model: Day, base_layout: QBoxLayout, base_gparent: 'gui_lib.g_main_window.GMainWindow'):
        super().__init__()
        self._model = model
        self._base_gparent = base_gparent
        self.gsubjects = []
        self._highlight_filter = False
        self.setProperty('isSelected', False)

        self.setLayout(QGridLayout())
        self.WIDTH = 5
        for i in range(len(base_gparent.model.subjects)):
            subj = GSubject(base_gparent.model.subjects[i], self)
            self._base_gparent.content_refreshed.connect(subj.content_update)
            subj.mouse_pressed.connect(self.update_layout)
            self.gsubjects.append(subj)
            self.layout().addWidget(subj, i // self.WIDTH, i % self.WIDTH)
        base_layout.insertWidget(base_layout.count() - 1, self)
        self.update_style()

    
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.setProperty('isSelected', not self.property('isSelected'))
            self._base_gparent.select_day(self, self.property('isSelected'))
            self.update_style()
        super().mousePressEvent(event)
    

    @property
    def model(self):
        return self._model
    

    @Slot()
    def update_layout(self):
        if self._highlight_filter:
            # zobrazi na zacatku tabulky oznacene predmety
            list(map(lambda x: x.setParent(None), self.gsubjects))
            selected = sorted(list(filter(lambda x: x.property('isSelected'), self.gsubjects)), key=lambda x: x.name)
            not_selected = sorted(list(filter(lambda x: not x.property('isSelected'), self.gsubjects)), key=lambda x: x.name)
            for i in range(len(self.gsubjects)):
                if i < len(selected):
                    self.layout().addWidget(selected[i], i // self.WIDTH, i % self.WIDTH)
                else:
                    self.layout().addWidget(not_selected[i - len(selected)], i // self.WIDTH, i % self.WIDTH)
        else:
            list(map(lambda x: x.setParent(None), self.gsubjects))
            for i in range(len(self.gsubjects)):
                self.layout().addWidget(self.gsubjects[i], i // self.WIDTH, i % self.WIDTH)
    

    def delete_gday(self):
        self._base_gparent.model.remove_day(self.model)
        self.setParent(None)
    

    def paintEvent(self, event: QPaintEvent) -> None:
        """Predefinuje funkci paintEvent

        Args:
            event (QPaintEvent): Promenna udalosti QPaintEvent
        """
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, p, self)
        super().paintEvent(event)
    

    @Slot()
    def filter_toggle(self):
        btn: QPushButton = self.sender()
        self._highlight_filter = btn.isChecked()
        self.update_layout()
    

    @Slot()
    def update_style(self):
        """Aktualizuje vzhled GComboBox"""
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()
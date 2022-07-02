from sort_lib.subject import Subject
import gui_lib.g_day 
from PySide6.QtWidgets import QFrame, QLabel, QHBoxLayout, QStyle, QStyleOption
from PySide6.QtCore import Signal, Slot, Qt
from PySide6.QtGui import QMouseEvent, QPaintEvent, QPainter

class GSubject(QFrame):

    update_style_triggered = Signal()
    mouse_pressed = Signal()

    def __init__(self, name: str, base_gparent: 'gui_lib.g_day.GDay', model: Subject=None):
        super().__init__()
        self._base_gparent = base_gparent
        self._model = model
        self._name = name

        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(5,2,5,2)
        self.update_style_triggered.connect(self.update_style)
        self.name_lbl = QLabel(self._name)
        self.counter_lbl = QLabel('0')
        self.setProperty('isSelected', False)

        self.layout().addWidget(self.name_lbl, alignment=Qt.AlignmentFlag.AlignCenter)


    @property
    def model(self):
        return self._model
    

    @property
    def name(self):
        return self._name


    @model.setter
    def model(self, value):
        self._model = value


    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.setProperty('isSelected', not self.property('isSelected'))
            if self.property('isSelected'):
                self._model = self._base_gparent.model.add_subject_name(self._name)
            else:
                self._base_gparent.model.remove_subject(self._name)
                self._model = None
            self.content_update()
            self.mouse_pressed.emit()
        else:
            super().mousePressEvent(event)
    

    def paintEvent(self, event: QPaintEvent) -> None:
        """Predefinuje funkci paintEvent

        Args:
            event (QPaintEvent): Promenna udalosti QPaintEvent
        """
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_CustomBase, opt, p, self)
        super().paintEvent(event)
    

    @Slot()
    def update_style(self):
        """Aktualizuje vzhled GSubject"""
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()
    

    @Slot()
    def content_update(self):
        if self._model is None:
            self.counter_lbl.setParent(None)
        else:
            self.layout().addWidget(self.counter_lbl, alignment=Qt.AlignmentFlag.AlignRight)
            self.counter_lbl.setText(str(self._model.student_count()))
        self.update_style()
    

    def __repr__(self) -> str:
        return self._name
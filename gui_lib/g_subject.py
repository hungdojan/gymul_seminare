from sort_lib.file_log import FileLog
from sort_lib.subject import Subject
import gui_lib.g_day 
from gui_lib.commands.g_subject_actions import SelectSubjectAction
from PySide6.QtWidgets import QFrame, QLabel, QHBoxLayout, QStyle, QStyleOption
from PySide6.QtCore import Signal, Slot, Qt
from PySide6.QtGui import QMouseEvent, QPaintEvent, QPainter

class GSubject(QFrame):
    """Graficka reprezentace predmetu ve dni."""

    # Signal se vysle v pripade zmeny vybranych predmetu
    selected_subjects_changed = Signal()

    def __init__(self, name: str, base_gparent: 'gui_lib.g_day.GDay', model: Subject=None):
        super().__init__()
        self._base_gparent = base_gparent
        self._model = model
        # Jmeno predmetu
        self._name = name

        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(5,2,5,2)
        self._setupUI()

        self.setProperty('isSelected', model is not None)
        self.content_update()


    def _setupUI(self):
        """Vygeneruje obsah g-predmetu."""
        self.name_lbl = QLabel(self._name)
        self.counter_lbl = QLabel('0')

        self.layout().addWidget(self.name_lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(self.counter_lbl, alignment=Qt.AlignmentFlag.AlignRight)

    @property
    def model(self):
        return self._model
    

    @property
    def base_gparent(self) -> 'gui_lib.g_day.GDay':
        return self._base_gparent
    

    @property
    def name(self):
        return self._name


    @model.setter
    def model(self, value):
        self._model = value


    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Prepsana funkce reakce na udalost mysi."""
        # leve tlacitko na mysi prepina stav oznaceni predmetu
        if event.button() == Qt.MouseButton.LeftButton:
            FileLog.loggers['default'].info(f'FE: Subject of day [{self.base_gparent}]'
                                            f' {self._name}\'s selection status changed to {self.property("isSelected")}')
            self._base_gparent._base_gparent._base_gparent.command_builder.execute(SelectSubjectAction(self))
        else:
            super().mousePressEvent(event)
    

    def paintEvent(self, event: QPaintEvent) -> None:
        """Predefinuje funkci paintEvent.

        Args:
            event (QPaintEvent): Promenna udalosti QPaintEvent.
        """
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_CustomBase, opt, p, self)
        super().paintEvent(event)
    

    @Slot()
    def update_style(self):
        """Aktualizuje vzhled GSubject."""
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()
    

    @Slot()
    def content_update(self):
        """Upravuje obsah g-predmetu."""
        if self._model is None:
            self.counter_lbl.setParent(None)
        else:
            self.layout().addWidget(self.counter_lbl, alignment=Qt.AlignmentFlag.AlignRight)
            self.counter_lbl.setText(str(self._model.student_count()))
        self.update_style()
    

    def __repr__(self) -> str:
        return self._name
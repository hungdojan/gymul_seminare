from sort_lib.student import Student
from PySide6.QtWidgets import *
from PySide6.QtCore import Slot, Qt, Signal
from PySide6.QtGui import QMouseEvent, QPalette, QPaintEvent, QPainter
import gui_lib.g_main_window
from gui_lib.g_combobox import GComboBox
from gui_lib.g_constants import StudentStatus

class GStudent(QWidget):

    locked_triggered = Signal()

    def __init__(self, model: Student, base_layout: QBoxLayout, base_gparent: 'gui_lib.g_main_window.GMainWindow'):
        super().__init__()
        self._model = model
        self._base_gparent = base_gparent
        # self._is_selected = False
        self._base_gparent.content_refreshed.connect(self.update_content)

        self._setupUI()
        self.setProperty('status', StudentStatus.NO_COMB)
        self.setProperty('isSelected', False)
        self.update_style()

        base_layout.insertWidget(base_layout.count() - 1, self)
        self.setAutoFillBackground(True)
        self._base_gparent.subject_list_update.connect(self.update_lof_items)
    

    @property
    def model(self):
        return self._model


    def get_status(self):
        return self.property('status')


    def isSelected(self):
        return self.property('isSelected')


    def _setupUI(self):
        self.hlayout = QHBoxLayout()
        self.hlayout.setSpacing(1)
        self.hlayout.setContentsMargins(10, 3, 10, 3)
        self.setLayout(self.hlayout)
        self.locked_triggered.connect(self.on_locked_triggered)

        # FIXME: lock_checkbox = QCheckBox()
        self.id_lbl = QLabel(self.model.id)
        self.first_name_lbl = QLabel(self.model.first_name)
        self.last_name_lbl = QLabel(self.model.last_name)
        self.class_id_lbl = QLabel(self.model.class_id)
        self.subjects_cb = []
        for i in self._model.lof_subjects:
            cb = GComboBox()
            cb.addItems(self._base_gparent.model.subjects)
            # FIXME:
            # cb.model().sort(0)
            # cb.insertItem(0, '-')
            index = cb.findText(i)
            cb.setCurrentIndex(index)
            cb.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            cb.setEditable(True)
            cb.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.subjects_cb.append(cb)
        

        self.hlayout.addWidget(self.id_lbl)
        self.hlayout.addWidget(self.first_name_lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        self.hlayout.addWidget(self.last_name_lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        self.hlayout.addWidget(self.class_id_lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        self.update_content()
        list(map(lambda x: self.hlayout.addWidget(x), self.subjects_cb))


    def mousePressEvent(self, a0: QMouseEvent) -> None:
        if a0.button() == Qt.MouseButton.RightButton:
            self.model.is_locked = not self.model.is_locked
            self.locked_triggered.emit()
        if a0.button() == Qt.MouseButton.LeftButton:
            self.setProperty('isSelected', not self.property('isSelected'))
            self._base_gparent.select_student(self, self.property('isSelected'))
            self.update_style()
            # TODO: choose subject combination
            pass
        super().mousePressEvent(a0)


    def remove_widget(self):
        self.setParent(None)
    

    def update_style(self):
        list(map(lambda x: x.update_style(), self.subjects_cb))
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()
    

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
    def update_content(self):
        # TODO:

        # nastaveni barvy pozadi zaka
        if len(self.model.possible_comb) < 1:
            self.setProperty('status', StudentStatus.NO_COMB)
        elif len(self.model.possible_comb) > 0 and self.model.chosen_comb is None:
            self.setProperty('status', StudentStatus.MUL_COMB)
        elif len(self.model.possible_comb) > 1 and self.model.chosen_comb is not None:
            self.setProperty('status', StudentStatus.MUL_SET)
        else:
            self.setProperty('status', StudentStatus.ONLY_ONE)
        self.update_style()
        self.on_locked_triggered()


    @Slot(list)
    def update_lof_items(self, subjects: list):
        """Aktualizace obsahu jednotlivych predmetovych Combobox

        Args:
            subjects (list): List jmen nove pridanych/smazanych predmetu
        """
        for s in subjects:
            # aktualizace nove pridanych predmetu
            if s in self._base_gparent.model.subjects:
                list(map(lambda x: x.addItem(s), self.subjects_cb))
            # odstraneni smazanych predmetu
            else:
                for cb in self.subjects_cb:
                    index = self.subjects_cb[cb].findText(s)
                    self.subjects_cb[cb].removeIndex(index)
        
        # serazeni nazvu predmetu v combobox
        list(map(lambda x: x.model().sort(0), self.subjects_cb))
        # TODO: removed subj in lof
                
        # TODO:
        # for i in range(len(self.subjects_cb)):
        #     self.subjects_cb[i].clear()
        #     self.subjects_cb[i].addItems(self._base_gparent.model.subjects)
        
            # index = self.subjects_cb[i].findText(i)
        # pass


    @Slot()
    def on_locked_triggered(self):
        # self.model.is_locked = not self.model.is_locked
        if self.model.is_locked:
            # self.id_lbl.setDisabled(True)
            # self.first_name_lbl.setDisabled(True)
            # self.last_name_lbl.setDisabled(True)
            # self.class_id_lbl.setDisabled(True)
            list(map(lambda x: x.setDisabled(True), self.subjects_cb))
        else:
            # self.id_lbl.setDisabled(False)
            # self.first_name_lbl.setDisabled(False)
            # self.last_name_lbl.setDisabled(False)
            # self.class_id_lbl.setDisabled(False)
            list(map(lambda x: x.setDisabled(False), self.subjects_cb))

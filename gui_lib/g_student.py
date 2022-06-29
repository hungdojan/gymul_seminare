from sort_lib.student import Student
from PySide6.QtWidgets import *
from PySide6.QtCore import Slot, Qt, Signal
from PySide6.QtGui import QMouseEvent, QPalette
import gui_lib.g_main_window
from gui_lib.g_combobox import GComboBox
import gui_lib.g_constants

class GStudent(QWidget):

    locked_triggered = Signal()

    def __init__(self, model: Student, base_layout: QBoxLayout, base_gparent: 'gui_lib.g_main_window.GMainWindow'):
        super().__init__()
        self._model = model
        self._base_gparent = base_gparent
        self._is_selected = False
        self._base_gparent.content_refreshed.connect(self.update_content)

        self._setupUI()

        base_layout.insertWidget(base_layout.count() - 1, self)
        self.setAutoFillBackground(True)
    

    @property
    def model(self):
        return self._model


    def _setupUI(self):
        self.hlayout = QHBoxLayout()
        self.hlayout.setSpacing(1)
        self.hlayout.setContentsMargins(10, 1, 10, 4)
        self.setLayout(self.hlayout)
        self.locked_triggered.connect(self.on_locked_triggered)

        lock_checkbox = QCheckBox()
        self.id_lbl = QLabel(self.model.id)
        self.first_name_lbl = QLabel(self.model.first_name)
        self.last_name_lbl = QLabel(self.model.last_name)
        self.class_id_lbl = QLabel(self.model.class_id)
        self.subjects_cb = []
        for i in self._model.lof_subjects:
            cb = GComboBox()
            cb.addItems(self._base_gparent.model.subjects)
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
            self.locked_triggered.emit()
        if a0.button() == Qt.MouseButton.LeftButton:
            # self.setVisible(False)
            pass
        # TODO:
        super().mousePressEvent(a0)


    def remove_widget(self):
        self.setParent(None)

    @Slot()
    def update_content(self):
        # TODO:

        # nastaveni barvy pozadi zaka
        pal = QPalette()
        if len(self.model.possible_comb) < 1:
            pal.setColor(QPalette.ColorRole.Window, gui_lib.g_constants.GWidgetColors.STUDENT_FAILED)
        elif len(self.model.possible_comb) > 0 and self.model.chosen_comb is None:
            pal.setColor(QPalette.ColorRole.Window, gui_lib.g_constants.GWidgetColors.STUDENT_MULTIPLE)
        elif len(self.model.possible_comb) > 1 and self.model.chosen_comb is not None:
            pal.setColor(QPalette.ColorRole.Window, gui_lib.g_constants.GWidgetColors.STUDENT_MULTIPLE_CHOSEN)
        else:
            pal.setColor(QPalette.ColorRole.Window, gui_lib.g_constants.GWidgetColors.STUDENT_PASSED)
        self.setPalette(pal)


    @Slot()
    def update_lof_items(self):
        # TODO:
        for i in len(self.subjects_cb):
            self.subjects_cb[i].clear()
            self.subjects_cb[i].addItems(self._base_gparent.model.subjects)
        
            index = self.subjects_cb[i].findText(i)
        pass


    @Slot()
    def on_locked_triggered(self):
        self.model.is_locked = not self.model.is_locked
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

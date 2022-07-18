from sort_lib.student import Student
from PySide6.QtWidgets import *
from PySide6.QtCore import Slot, Qt, Signal, QPoint
from PySide6.QtGui import QMouseEvent, QPaintEvent, QPainter, QFont, QAction
import gui_lib.g_main_window
import gui_lib.g_student_panel
from gui_lib.g_combobox import GComboBox
from gui_lib.g_constants import StudentStatus
from gui_lib.g_edit_student_dialog import GEditStudentDialog
from gui_lib.g_combination_dialog import GCombinationDialog
import gui_lib.g_student_control_dialog


class GStudent(QWidget):

    # Signal se vysle, pokud se aktualizuje seznam pozadovanych predmetu studenta
    required_subjects_changed = Signal()

    def __init__(self, model: Student, base_gparent: 'gui_lib.g_student_panel.GStudentPanel'):
        super().__init__()
        self._model = model
        self._base_gparent = base_gparent

        # propojeni signalu a slotu
        self.customContextMenuRequested.connect(self.show_context_menu)

        # nastaveni studentova widgetu
        self._setupUI()
        self.setProperty('status', StudentStatus.NO_COMB)
        self.setProperty('isSelected', False)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
    

    @property
    def model(self) -> Student:
        return self._model
    

    @property
    def base_gparent(self) -> 'gui_lib.g_main_window.GMainWindow':
        return self._base_gparent


    def get_status(self) -> str:
        return self.property('status')


    def isSelected(self) -> bool:
        return self.property('isSelected')
    

    def _setupUI(self) -> None:
        """Vygeneruje obsah g-student."""
        self.setLayout(QHBoxLayout())
        self.layout().setSpacing(1)
        self.layout().setContentsMargins(10, 3, 10, 3)

        font = QFont('Font Awesome 6 Free Solid')
        # znak zamku
        self.lock_lbl = QLabel(objectName='id')
        self.lock_lbl.setFixedWidth(20)
        self.lock_lbl.setFont(font)
        self.lock_lbl.setText('\uf023')
        self.lock_lbl.hide()

        self.id_lbl = QLabel(self.model.id, objectName='id')
        self.id_lbl.setFixedWidth(20)
        self.first_name_lbl = QLabel(self.model.first_name)
        self.last_name_lbl = QLabel(self.model.last_name)
        self.class_id_lbl = QLabel(self.model.class_id)

        # ComboBoxy jednotlivych predmetu
        self.subjects_cb = []
        for i in range(len(self._model.required_subjects)):
            cb = GComboBox(self, i)
            cb.currentIndexChanged.connect(self.update_subjects)
            self.subjects_cb.append(cb)
        
        # pridani jednotlivych elementu do hlavniho elementu GStudent
        self.layout().addWidget(self.lock_lbl)
        self.layout().addWidget(self.id_lbl)
        self.layout().addWidget(self.first_name_lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(self.last_name_lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(self.class_id_lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        list(map(lambda x: self.layout().addWidget(x), self.subjects_cb))


    def mousePressEvent(self, a0: QMouseEvent) -> None:
        """Prepsana funkce reakce na udalost mysi."""
        if a0.button() == Qt.MouseButton.MiddleButton:
            # uzamceni studenta
            self.setProperty('isSelected', not self.property('isSelected'))
            self._base_gparent.select_gstudent(self, self.property('isSelected'))
            self.update_style()
        elif a0.button() == Qt.MouseButton.LeftButton:
            # vyber kombinaci
            if not self.model.is_locked:
                GCombinationDialog(self).exec()
        super().mousePressEvent(a0)


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


    def update_style(self):
        """Aktualizuje vzhled GStudent"""
        self.lock_lbl.style().unpolish(self.lock_lbl)
        self.lock_lbl.style().polish(self.lock_lbl)
        self.lock_lbl.update()

        self.id_lbl.style().unpolish(self.id_lbl)
        self.id_lbl.style().polish(self.id_lbl)
        self.id_lbl.update()

        self.style().unpolish(self)
        self.style().polish(self)
        self.update()


    def update_personal_data(self) -> None:
        """Aktualizace dat studenta z backendu"""
        self.first_name_lbl.setText(self.model.first_name)
        self.last_name_lbl.setText(self.model.last_name)
        self.class_id_lbl.setText(self.model.class_id)
    

    def load_from_model(self) -> None:
        """Aktualizuje studentovy data z student modelu."""
        self.update_personal_data()
        for i in range(len(self.subjects_cb)):
            text = self._model.required_subjects[i] if self._model.required_subjects[i] else '-'
            index = self.subjects_cb[i].findText(text)
            self.subjects_cb[i].setCurrentIndex(index)
        self.update_content()
    

    @Slot()
    def update_content(self) -> None:
        """Aktualizuje hodnotu 'status'"""
        # nastaveni barvy pozadi zaka
        if len(self.model.possible_comb) < 1:
            self.setProperty('status', StudentStatus.NO_COMB)
            self.lock_trigger()
        elif len(self.model.possible_comb) > 0 and self.model.chosen_comb is None:
            self.setProperty('status', StudentStatus.MUL_COMB)
        elif len(self.model.possible_comb) > 1 and self.model.chosen_comb is not None:
            self.setProperty('status', StudentStatus.MUL_SET)
        else:
            self.setProperty('status', StudentStatus.ONLY_ONE)
        self.update_style()


    @Slot(QPoint)
    def show_context_menu(self, point: QPoint):
        """Zobrazuje context menu po kliknutim pravym tlacitkem na element

        Args:
            point (QPoint): Informace o miste kliknuti
        """
        context_menu = QMenu(self)

        # vybira kombinaci studenta
        self._choose_action = context_menu.addAction('Vybrat kombinaci')
        self._choose_action.triggered.connect(lambda: GCombinationDialog(self).exec())
        self._choose_action.setDisabled(self.model.is_locked)
        context_menu.addSeparator()

        # zamyka studenta pred upravou
        lock_action = context_menu.addAction('Zamknout')
        lock_action.setEnabled(self._model.chosen_comb is not None)
        lock_action.setCheckable(True)
        lock_action.setChecked(self.model.is_locked)
        lock_action.triggered.connect(self.lock_trigger)

        # upravuje data studenta
        edit_action = context_menu.addAction('Upravit data')
        edit_action.triggered.connect(lambda: GEditStudentDialog(self).exec())
        context_menu.addSeparator()

        # maze studenta
        delete_action = context_menu.addAction('Smazat')
        delete_action.triggered.connect(self.delete_gstudent)

        context_menu.exec(self.mapToGlobal(point))
    
    @Slot()
    def lock_trigger(self) -> None:
        """Slot, ktery reaguje na prepnuti zamku"""
        action: QAction = self.sender()
        if isinstance(action, QAction):
            self.model.is_locked = action.isChecked()
        if self.model.is_locked:
            self.lock_lbl.show()
            list(map(lambda x: x.setDisabled(True), self.subjects_cb))
        else:
            self.lock_lbl.hide()
            list(map(lambda x: x.setDisabled(False), self.subjects_cb))
    

    @Slot()
    def delete_gstudent(self) -> None:
        """Mazani tohoto studenta z programu"""
        gui_lib.g_student_control_dialog.GStudentControlDialog.delete_student_from_model(self._model.id)
        self._base_gparent.delete_gstudent(self)
    

    @Slot(int)
    def update_subjects(self, index: int):
        cb = self.sender()
        if not isinstance(cb, GComboBox):
            return
        if not cb.model().available:
            cb.update_view()
            return

        _index = self.subjects_cb.index(cb)
        if self._model.required_subjects[_index] == cb.currentText():
            return
        current_comb = tuple([cb.currentText() if cb.currentText() != '-' else None 
                              for cb in self.subjects_cb])
        self._model.required_subjects = current_comb
        self._base_gparent._base_gparent.view_updated.emit()
        self.required_subjects_changed.emit()
        gui_lib.g_student_control_dialog.GStudentControlDialog.update_row(self._model)
from sort_lib.student import Student
from PySide6.QtWidgets import *
from PySide6.QtCore import Slot, Qt, Signal, QPoint
from PySide6.QtGui import QMouseEvent, QPaintEvent, QPainter, QFont, QAction
import gui_lib.g_main_window
from gui_lib.g_combobox import GComboBox
from gui_lib.g_constants import StudentStatus
from gui_lib.g_edit_student_dialog import GEditStudentDialog
from gui_lib.g_combination_dialog import GCombinationDialog

class GStudent(QWidget):

    locked_triggered = Signal()
    update_style_triggered = Signal()

    def __init__(self, model: Student, base_layout: QBoxLayout, base_gparent: 'gui_lib.g_main_window.GMainWindow'):
        super().__init__()
        self._model = model
        self._base_gparent = base_gparent

        # propojeni signalu a slotu
        self._base_gparent.subject_list_update.connect(self.update_lof_items)
        self.update_style_triggered.connect(self.update_style)
        self._base_gparent.content_refreshed.connect(self.update_content)
        self.customContextMenuRequested.connect(self.show_context_menu)

        # nastaveni studentova widgetu
        self._setupUI()
        self.setProperty('status', StudentStatus.NO_COMB)
        self.setProperty('isSelected', False)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        # vlozeni do rozlozeni
        base_layout.insertWidget(base_layout.count() - 1, self)
    

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
        for i in self._model.lof_subjects:
            cb = GComboBox()
            cb.addItems(self._base_gparent.model.subjects)
            index = cb.findText(i)
            cb.setCurrentIndex(index)
            cb.currentIndexChanged.connect(self.update_subjects)
            self.update_style_triggered.connect(cb.update_style)
            self.subjects_cb.append(cb)
        
        # pridani jednotlivych elementu do hlavniho elementu GStudent
        self.layout().addWidget(self.lock_lbl)
        self.layout().addWidget(self.id_lbl)
        self.layout().addWidget(self.first_name_lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(self.last_name_lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(self.class_id_lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        list(map(lambda x: self.layout().addWidget(x), self.subjects_cb))


    def mousePressEvent(self, a0: QMouseEvent) -> None:
        if a0.button() == Qt.MouseButton.MiddleButton:
            self.setProperty('isSelected', not self.property('isSelected'))
            self._base_gparent.select_student(self, self.property('isSelected'))
            self.update_style_triggered.emit()
        elif a0.button() == Qt.MouseButton.LeftButton:
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


    @Slot()
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


    @Slot()
    def update_content(self) -> None:
        """Aktualizuje hodnotu 'status'"""
        # nastaveni barvy pozadi zaka
        if len(self.model.possible_comb) < 1:
            self.setProperty('status', StudentStatus.NO_COMB)
        elif len(self.model.possible_comb) > 0 and self.model.chosen_comb is None:
            self.setProperty('status', StudentStatus.MUL_COMB)
        elif len(self.model.possible_comb) > 1 and self.model.chosen_comb is not None:
            self.setProperty('status', StudentStatus.MUL_SET)
        else:
            self.setProperty('status', StudentStatus.ONLY_ONE)
        self.update_style_triggered.emit()
        self.locked_triggered.emit()


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
        self.model.is_locked = action.isChecked()
        if self.model.is_locked:
            self.lock_lbl.show()
            list(map(lambda x: x.setDisabled(True), self.subjects_cb))
        else:
            self.lock_lbl.hide()
            list(map(lambda x: x.setDisabled(False), self.subjects_cb))
    

    @Slot()
    def update_data(self) -> None:
        """Aktualizace dat studenta z backendu"""
        self.first_name_lbl.setText(self.model.first_name)
        self.last_name_lbl.setText(self.model.last_name)
        self.class_id_lbl.setText(self.model.class_id)
    

    @Slot()
    def delete_gstudent(self) -> None:
        """Mazani tohoto studenta z programu"""
        self._base_gparent.model.remove_student(self.model.id)
        self.setParent(None)
    

    @Slot(int)
    def update_subjects(self, index: int):
        cb: GComboBox = self.sender()
        sender_index = self.subjects_cb.index(cb)
        print(sender_index)
        # TODO:
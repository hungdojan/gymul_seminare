from PySide6.QtWidgets import QScrollArea, QVBoxLayout, QFrame
from PySide6.QtCore import Slot, Qt

from gui_lib.g_student import GStudent
import gui_lib.g_main_window
from gui_lib.g_constants import StudentStatus

from sort_lib.student import Student

class GStudentPanel(QScrollArea):
    
    def __init__(self, base_gparent: 'gui_lib.g_main_window.GMainWindow'):
        super().__init__()
        self._base_gparent = base_gparent
        # Seznam vsech g-studentu v ramci
        self.lof_gstudents: list[GStudent] = []
        # Seznam oznacenych studentu        
        self.selected_students: list[GStudent] = []
        self._setupUI()

        # nastaveni
        self.setMinimumWidth(500)
        self.setFrameShape(QFrame.Shape.Box)
        self.setFrameShadow(QFrame.Shadow.Plain)
        self.setWidgetResizable(True)
    

    def _setupUI(self) -> None:
        """Vygeneruje obsah GStudentPanel."""
        # nastaveni korene skrolovaciho widgetu
        self.main_frame = QFrame()
        self.main_frame.setLayout(QVBoxLayout())
        self.main_frame.layout().setContentsMargins(3, 3, 3, 3)
        self.main_frame.layout().setSpacing(3)
        self.main_frame.layout().addStretch()

        self.setWidget(self.main_frame)
    

    def add_gstudent(self, student: Student) -> GStudent:
        """Vytvori g-studenta podle modelu a vlozi ho do ramce.

        Args:
            student (Student): Model studenta.

        Returns:
            GStudent: Vytvorena instance g-studenta.
        """
        if student is None:
            return None

        gstudent = GStudent(student, self)

        # nastaveni signalu-slotu
        gstudent.required_subjects_changed.connect(
            self._base_gparent.table_view.model().sourceModel().update_model_counter)
        self._base_gparent.data_updated.connect(gstudent.update_content)

        self.main_frame.layout().insertWidget(len(self.lof_gstudents), gstudent)
        self.lof_gstudents.append(gstudent)
        return gstudent
    

    def select_gstudent(self, gstudent: GStudent, is_selected: bool) -> None:
        """Spravuje oznacene GStudenty

        Args:
            gstudent (GStudent): Instance GStudent, ktereho se Všechny operace tyka
            is_selected (bool): Pravdivostni hodnota, zda byl objekt oznacen ci ne
        """
        if is_selected:
            self.selected_students.append(gstudent)
        else:
            try:
                self.selected_students.remove(gstudent)
            except:
                pass
    
    
    def clear(self) -> None:
        """Smaze vsechny studenty z ramce a modelu."""
        for i in range(len(self.lof_gstudents) - 1, -1, -1):
            self.delete_gstudent(self.lof_gstudents[i])
        self.lof_gstudents.clear()
        self.selected_students.clear()
    

    @Slot()
    def delete_gstudent(self, gstudent: GStudent) -> None:
        """Smaze vybraneho studenta.

        Args:
            gstudent (GStudent): Vybrana instance g-studenta.
        """
        if gstudent not in self.lof_gstudents:
            return
        gstudent.required_subjects_changed.disconnect(
            self._base_gparent.table_view.model().sourceModel().update_model_counter)
        self._base_gparent.data_updated.disconnect(gstudent.update_content)
        self.lof_gstudents.remove(gstudent)
        self._base_gparent.model.remove_student(gstudent.model.id)
        gstudent.setParent(None)


    @Slot()
    def delete_selected(self) -> None:
        """Vymaze oznacene studenty."""
        self._base_gparent.status_bar.showMessage('Mažu studenty')
        list(map(lambda x: self.delete_gstudent(x), self.selected_gstudents))
        self._base_gparent.status_bar.showMessage('Všechny operace dokončené', 6000)
    

    @Slot()
    def filter_students(self) -> None:
        """Slot provadi filtraci studentu podle jejich statusu"""
        self._base_gparent.status_bar.showMessage('Provádím filtraci studentů')
        # red
        red_students = [gstudent for gstudent in self.lof_gstudents
                        if gstudent.get_status() == StudentStatus.NO_COMB]
        list(map(lambda x: x.setVisible(self._base_gparent.buttons['red'].isChecked()), red_students))

        # yellow
        yellow_students = [gstudent for gstudent in self.lof_gstudents
                           if gstudent.get_status() == StudentStatus.MUL_COMB]
        list(map(lambda x: x.setVisible(self._base_gparent.buttons['yellow'].isChecked()), yellow_students))

        # blue-ish
        blueish_students = [gstudent for gstudent in self.lof_gstudents
                            if gstudent.get_status() == StudentStatus.MUL_SET]
        list(map(lambda x: x.setVisible(self._base_gparent.buttons['blue-ish'].isChecked()), blueish_students))

        # green
        green_students = [gstudent for gstudent in self.lof_gstudents
                          if gstudent.get_status() == StudentStatus.ONLY_ONE]
        list(map(lambda x: x.setVisible(self._base_gparent.buttons['green'].isChecked()), green_students))

        for btn in self._base_gparent.buttons:
            self._base_gparent.buttons[btn].setText('ON' if self._base_gparent.buttons[btn].isChecked() else 'OFF')
        self._base_gparent.status_bar.showMessage('Všechny operace dokončené', 6000)

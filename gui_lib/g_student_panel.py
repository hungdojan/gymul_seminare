from PySide6.QtWidgets import QScrollArea, QVBoxLayout, QFrame
from PySide6.QtCore import Slot

from gui_lib.g_student import GStudent
import gui_lib.g_main_window
from gui_lib.g_constants import StudentStatus
from sort_lib.file_log import FileLog

from sort_lib.student import Student

class GStudentPanel(QScrollArea):
    
    def __init__(self, base_gparent: 'gui_lib.g_main_window.GMainWindow'):
        super().__init__()
        self._base_gparent = base_gparent
        # Seznam vsech g-studentu v ramci
        self.lof_gstudents: list[GStudent] = []
        self._setupUI()

        # nastaveni
        self.setMinimumWidth(500)
        self.setFrameShape(QFrame.Shape.Box)
        self.setFrameShadow(QFrame.Shadow.Plain)
        self.setWidgetResizable(True)
    

    @property
    def base_gparent(self) -> 'gui_lib.g_main_window.GMainWindow':
        return self._base_gparent
    

    def _setupUI(self) -> None:
        """Vygeneruje obsah GStudentPanel."""
        # nastaveni korene skrolovaciho widgetu
        self.main_frame = QFrame()
        self.main_frame.setLayout(QVBoxLayout())
        self.main_frame.layout().setContentsMargins(3, 3, 3, 3)
        self.main_frame.layout().setSpacing(3)
        self.main_frame.layout().addStretch()

        self.setWidget(self.main_frame)
    

    def add_gstudent(self, student: Student, index: int=-1) -> GStudent:
        """Vytvori g-studenta podle modelu a vlozi ho do ramce.

        Args:
            student (Student): Model studenta.
            index (int, optional): Radek, na ktery se ma student vlozit. Defaults to -1.

        Returns:
            GStudent: Vytvorena instance g-studenta.
        """
        if student is None:
            return None

        gstudent = GStudent(student, self)
        FileLog.loggers['default'].info(f'FE: Add {gstudent}')

        # nastaveni signalu-slotu
        gstudent.required_subjects_changed.connect(
            self._base_gparent.table_view.model().sourceModel().update_model_counter)
        self._base_gparent.data_updated.connect(gstudent.update_content)

        self.lof_gstudents.append(gstudent)
        if index < 0:
            self.main_frame.layout().insertWidget(len(self.lof_gstudents) - 1, gstudent)
        else:
            self.main_frame.layout().insertWidget(index, gstudent)
        return gstudent
    
    
    def clear(self) -> None:
        """Smaze vsechny studenty z ramce a modelu."""
        for i in range(len(self.lof_gstudents) - 1, -1, -1):
            self.delete_gstudent(self.lof_gstudents[i])
        self.lof_gstudents.clear()
    

    def update_student(self, student_id: str):
        """Aktualizuje data studenta.
        
        Args:
            student_id (str): Identifikacni hodnota studenta.
        """
        gstudent = [gs for gs in self.lof_gstudents
                    if gs.model.id == student_id]
        if gstudent:
            gstudent[0].load_from_model()
    

    def student_index(self, student: Student) -> int:
        """Vraci radek, na kterem se student nachazi.

        Args:
            student (Student): Model (instance) studenta.

        Returns:
            int: Vysledny radek, -1 pokud student nebyl nalezen v seznamu.
        """
        gstudent = [gstudent for gstudent in self.lof_gstudents
                    if gstudent.model == student]
        if not gstudent:
            return -1
        return self.lof_gstudents.index(gstudent[0])
    

    def delete_student_id(self, student_id: str):
        """Smaze studenta z modelu.

        Args:
            student_id (str): Identifikacni hodnota studenta.
        """
        gstudent = [gs for gs in self.lof_gstudents
                    if gs.model.id == student_id]
        if gstudent:
            self.delete_gstudent(gstudent[0])


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
        self._base_gparent.model.remove_student(gstudent.model)
        FileLog.loggers['default'].info(f'FE: {gstudent} deleted')
        gstudent.deleteLater()


    @Slot()
    def filter_students(self) -> None:
        """Slot provadi filtraci studentu podle jejich statusu"""
        self._base_gparent.status_bar.showMessage('Provádím filtraci studentů')
        # red
        red_students = [gstudent for gstudent in self.lof_gstudents
                        if gstudent.get_status() == StudentStatus.NO_COMB]
        list(map(lambda x: x.setVisible(self._base_gparent.student_buttons['red'].isChecked()), red_students))

        # yellow
        yellow_students = [gstudent for gstudent in self.lof_gstudents
                           if gstudent.get_status() == StudentStatus.MUL_COMB]
        list(map(lambda x: x.setVisible(self._base_gparent.student_buttons['yellow'].isChecked()), yellow_students))

        # blue-ish
        blueish_students = [gstudent for gstudent in self.lof_gstudents
                            if gstudent.get_status() == StudentStatus.MUL_SET]
        list(map(lambda x: x.setVisible(self._base_gparent.student_buttons['blue-ish'].isChecked()), blueish_students))

        # green
        green_students = [gstudent for gstudent in self.lof_gstudents
                          if gstudent.get_status() == StudentStatus.ONLY_ONE]
        list(map(lambda x: x.setVisible(self._base_gparent.student_buttons['green'].isChecked()), green_students))

        for btn in self._base_gparent.student_buttons:
            self._base_gparent.student_buttons[btn].setText('ON' if self._base_gparent.student_buttons[btn].isChecked() else 'OFF')
        self._base_gparent.status_bar.showMessage('Všechny operace dokončené', 6000)

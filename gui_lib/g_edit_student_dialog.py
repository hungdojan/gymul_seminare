from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QVBoxLayout, QWidget, QDialogButtonBox
import gui_lib.g_student

class GEditStudentDialog(QDialog):
    """Trida pro okno upravujici studentovy osobni data."""
    
    def __init__(self, gstudent: 'gui_lib.g_student.GStudent'):
        super().__init__()
        self.gstudent = gstudent

        self.setWindowTitle('Upravit data studenta')
        self.setLayout(QVBoxLayout())

        self._setupUI()
    

    def _setupUI(self):
        """Vygenerovani okna GEditStudentDialog."""
        # nastaveni rozlozeni formulare
        form_w = QWidget()
        form_w.setLayout(QFormLayout())
        self.fn_lbl = QLineEdit(self.gstudent.model.first_name)
        self.ln_lbl = QLineEdit(self.gstudent.model.last_name)
        self.class_lbl = QLineEdit(self.gstudent.model.class_id)
        form_w.layout().addRow('Jméno:', self.fn_lbl)
        form_w.layout().addRow("Příjmení:", self.ln_lbl)
        form_w.layout().addRow("Třída:", self.class_lbl)
        self.layout().addWidget(form_w)

        # tlacitka v dolni casti okna
        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        self.layout().addWidget(button_box)
    

    def accept(self) -> None:
        """Akce po uspesnem ukonceni dialogoveho okna"""
        self.gstudent.model.first_name = self.fn_lbl.text()
        self.gstudent.model.last_name = self.ln_lbl.text()
        self.gstudent.model.class_id = self.class_lbl.text()
        self.gstudent.update_personal_data()
        super().accept()
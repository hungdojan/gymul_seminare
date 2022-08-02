from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QVBoxLayout, QDialogButtonBox
import gui_lib.g_student
from gui_lib.commands.edit_student_dialog_action import EditStudentDialogAction
from sort_lib.file_log import FileLog

class GEditStudentDialog(QDialog):
    """Trida pro okno upravujici studentovy osobni data."""
    
    def __init__(self, gstudent: 'gui_lib.g_student.GStudent'):
        super().__init__()
        self.gstudent = gstudent

        self.setWindowTitle('Upravit data studenta')
        self.setLayout(QVBoxLayout())

        self._setupUI()
        FileLog.loggers['default'].info('FE: GEditStudentDialog window opened')
    

    def _setupUI(self):
        """Vygenerovani okna GEditStudentDialog."""
        # nastaveni rozlozeni formulare
        self.fn_lbl = QLineEdit(self.gstudent.model.first_name)
        self.ln_lbl = QLineEdit(self.gstudent.model.last_name)
        self.class_lbl = QLineEdit(self.gstudent.model.class_id)

        form_layout = QFormLayout()
        form_layout.addRow('Jméno:', self.fn_lbl)
        form_layout.addRow("Příjmení:", self.ln_lbl)
        form_layout.addRow("Třída:", self.class_lbl)
        
        self.layout().addLayout(form_layout)

        # tlacitka v dolni casti okna
        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        self.layout().addWidget(button_box)
    

    def accept(self) -> None:
        """Akce po uspesnem ukonceni dialogoveho okna"""
        gmainwindow = self.gstudent.base_gparent.base_gparent
        gmainwindow.command_builder.execute(EditStudentDialogAction(self))
        FileLog.loggers['default'].info('FE: GEditStudentDialog window accepted')
        super().accept()
    
    def reject(self) -> None:
        FileLog.loggers['default'].info('FE: GEditStudentDialog window rejected')
        return super().reject()
from sort_lib.command import Command

import gui_lib.g_edit_student_dialog
from gui_lib.g_student_control_dialog import GStudentControlDialog
from sort_lib.file_log import FileLog

class EditStudentDialogAction(Command):

    def __init__(self, parent: 'gui_lib.g_edit_student_dialog.GEditStudentDialog') -> None:
        self._parent = parent
        self._model = parent.gstudent.model
        self._fname = (self._model.first_name, parent.fn_lbl.text())
        self._lname = (self._model.last_name, parent.ln_lbl.text())
        self._class_id = (self._model.class_id, parent.class_lbl.text())

    def execute(self) -> None:
        # aktualizuje osobni udaje studentu
        FileLog.loggers['default'].info('CMD: Execute EditStudentDialogAction')
        self._model.first_name = self._fname[1]
        self._model.last_name = self._lname[1]
        self._model.class_id = self._class_id[1]
        self._parent.gstudent.update_personal_data()
        GStudentControlDialog.update_row(self._model)


    def redo(self) -> None:
        self.execute()

    def undo(self) -> None:
        self._model.first_name = self._fname[0]
        self._model.last_name = self._lname[0]
        self._model.class_id = self._class_id[0]
        self._parent.gstudent.update_personal_data()
        GStudentControlDialog.update_row(self._model)
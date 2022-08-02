from sort_lib.command import Command

import gui_lib.g_student
import gui_lib.g_student_control_dialog

class StudentRequiredSubjectsChange(Command):

    def __init__(self, parent: 'gui_lib.g_student.GStudent', combobox_index: int):
        self._parent = parent
        self._model = parent.model
        self._old_comb = self._model.required_subjects
        self._new_comb = tuple([cb.currentText() if cb.currentText() != '-' else None 
                              for cb in parent.subjects_cb])
        self._combobox_index = combobox_index
        self._gmainwindow = parent.base_gparent.base_gparent

    def execute(self) -> None:
        self._model.required_subjects = self._new_comb
        self._gmainwindow.view_updated.emit()
        self._parent.required_subjects_changed.emit()
        gui_lib.g_student_control_dialog.GStudentControlDialog.update_row(self._model)

    def redo(self) -> None:
        # nastaveni comboboxu
        text = self._new_comb[self._combobox_index] if self._new_comb[self._combobox_index] else '-'
        index = self._parent.subjects_cb[self._combobox_index].findText(text)
        self._parent.subjects_cb[self._combobox_index].setCurrentIndex(index)

        self._gmainwindow.view_updated.emit()
        self._parent.required_subjects_changed.emit()
        gui_lib.g_student_control_dialog.GStudentControlDialog.update_row(self._model)

    def undo(self) -> None:
        # nastaveni comboboxu
        text = self._old_comb[self._combobox_index] if self._old_comb[self._combobox_index] else '-'
        index = self._parent.subjects_cb[self._combobox_index].findText(text)
        self._parent.subjects_cb[self._combobox_index].setCurrentIndex(index)

        self._gmainwindow.view_updated.emit()
        self._parent.required_subjects_changed.emit()
        gui_lib.g_student_control_dialog.GStudentControlDialog.update_row(self._model)
    
class StudentDeleteAction(Command):

    def __init__(self, parent: 'gui_lib.g_student.GStudent') -> None:
        self._parent = parent
        self._gmainwindow = parent.base_gparent.base_gparent
        self._model = parent.model
        self._index = parent.base_gparent.student_index(self._model)

    def execute(self) -> None:
        gui_lib.g_student_control_dialog.GStudentControlDialog.delete_student_from_model(self._model.id)
        self._parent._base_gparent.delete_gstudent(self._parent)

    def redo(self) -> None:
        gui_lib.g_student_control_dialog.GStudentControlDialog.delete_student_from_model(self._model.id)
        self._parent._base_gparent.delete_gstudent(self._parent)

    def undo(self) -> None:
        self._gmainwindow.model.add_student(self._model)
        self._parent = self._parent._base_gparent.add_gstudent(self._model, self._index)
        gui_lib.g_student_control_dialog.GStudentControlDialog.add_student_to_model(self._model)
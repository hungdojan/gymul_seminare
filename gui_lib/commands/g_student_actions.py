from sort_lib.command import Command

import gui_lib.g_student

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
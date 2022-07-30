from sort_lib.command import Command
from sort_lib.student import Student

import gui_lib.g_main_window
import gui_lib.g_student_control_dialog

class StudentControlAdd(Command):

    def __init__(self, model: Student, gmainwindow: 'gui_lib.g_main_window.GMainWindow'):
        super().__init__()
        self._gmainwindow = gmainwindow
        self._model = model
        self._required_subjects = model.required_subjects
        self._possible_comb = model._possible_comb
        self._chosen_comb = model.chosen_comb
    
    def execute(self):
        # prida studenta
        self._gmainwindow.model.add_student(self._model)
        self._gmainwindow.student_panel.add_gstudent(self._model)
        gui_lib.g_student_control_dialog.GStudentControlDialog.add_student_to_model(self._model)
        self._gmainwindow.subject_counter_changed.emit()
        self._index = self._gmainwindow.student_panel.student_index(self._model)

    def undo(self):
        # odebere studenta
        self._gmainwindow.student_panel.delete_student_id(self._model.id)
        gui_lib.g_student_control_dialog.GStudentControlDialog.delete_student_from_model(self._model.id)
        self._gmainwindow.subject_counter_changed.emit()

    def redo(self):
        # nacteni udaju studenta
        self._model.required_subjects = self._required_subjects
        self._model._possible_comb = self._possible_comb
        if self._chosen_comb is not None:
            self._model.set_comb(self._model.possible_comb.index(self._chosen_comb))

        # vlozeni studenta do okna a modelu
        self._gmainwindow.model.add_student(self._model)
        self._gmainwindow.student_panel.add_gstudent(self._model, self._index)
        gui_lib.g_student_control_dialog.GStudentControlDialog.add_student_to_model(self._model)
        self._gmainwindow.subject_counter_changed.emit()


class StudentControlEdit(Command):

    def __init__(self, parent: 'gui_lib.g_student_control_dialog.GStudentControlDialog.GStudentControlDialogEdit'):
        self.fname = (parent.model.first_name, parent.fname_le.text())
        self.lname = (parent.model.last_name, parent.lname_le.text())
        self.class_id = (parent.model.class_id, parent.class_le.text())
        self.old_comb = parent.model.required_subjects
        self.new_comb = tuple([cb.currentText() if cb.currentText() != '-' else None
                      for cb in parent.subject_cb])
        self.gmainwindow = parent.gmainwindow
        self.model = parent.model


    def execute(self) -> None:
        self.model.first_name = self.fname[1]
        self.model.last_name = self.lname[1]
        self.model.class_id = self.class_id[1]
        if self.new_comb != self.old_comb:
            self.model.required_subjects = self.new_comb
            self.gmainwindow.subject_counter_changed.emit()
        self.gmainwindow.student_panel.update_student(str(self.model.id))
        gui_lib.g_student_control_dialog.GStudentControlDialog.update_row(self.model)

    def undo(self) -> None:
        self.model.first_name = self.fname[0]
        self.model.last_name = self.lname[0]
        self.model.class_id = self.class_id[0]
        if self.new_comb != self.old_comb:
            self.model.required_subjects = self.old_comb
            self.gmainwindow.subject_counter_changed.emit()
        self.gmainwindow.student_panel.update_student(str(self.model.id))
        gui_lib.g_student_control_dialog.GStudentControlDialog.update_row(self.model)

    def redo(self) -> None:
        self.execute()
    
class StudentControlDelete(Command):

    def __init__(self, gmainwindow: 'gui_lib.g_main_window.GMainWindow', id_value: int) -> None:
        self._gmainwindow = gmainwindow
        self._model = gmainwindow.model.get_student(id_value)

        self._student_id = id_value
        self._required_subjects = self._model.required_subjects
        self._possible_comb = self._model._possible_comb
        self._chosen_comb = self._model.chosen_comb
        # radek, na kterem se nachazi student v student_panelu
        self._index = gmainwindow.student_panel.student_index(self._model)
        super().__init__()

    def execute(self) -> None:
        self._gmainwindow.student_panel.delete_student_id(self._student_id)
        gui_lib.g_student_control_dialog.GStudentControlDialog.delete_student_from_model(self._student_id)
        self._gmainwindow.subject_counter_changed.emit()

    def undo(self) -> None:
        # nacteni udaju studenta
        self._model.required_subjects = self._required_subjects
        self._model._possible_comb = self._possible_comb
        if self._chosen_comb is not None:
            self._model.set_comb(self._model.possible_comb.index(self._chosen_comb))

        # vlozeni do okna a modelu
        self._gmainwindow.model.add_student(self._model)
        self._gmainwindow.student_panel.add_gstudent(self._model, self._index)
        gui_lib.g_student_control_dialog.GStudentControlDialog.add_student_to_model(self._model)
        self._gmainwindow.subject_counter_changed.emit()

    def redo(self) -> None:
        self.execute()
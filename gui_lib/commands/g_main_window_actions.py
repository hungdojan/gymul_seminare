from sort_lib.command import Command

import sort_lib.sort
import gui_lib.g_main_window
from gui_lib.g_student_control_dialog import GStudentControlDialog
import sort_lib.student

class MainWindowImportStudents(Command):

    def __init__(self, parent: 'gui_lib.g_main_window.GMainWindow', filename: str) -> None:
        self._gmainwindow = parent
        self._model = parent.model
        self._fn = filename

    def execute(self) -> None:
        new_ids, self._new_subjs = self._model.load_file_students(self._fn)
        # nacteni novych predmetu
        if len(self._new_subjs) > 0:
            self._gmainwindow.subject_list_updated.emit(self._new_subjs)

        self._new_students: dict[int, sort_lib.student.Student] = {}
        self._student_data: dict[sort_lib.student.Student, tuple] = {}
        # ulozeni nove pridanych studentu
        for student_id in new_ids:
            student = self._model.get_student(student_id)
            if student is None:
                continue
            self._new_students[self._model.students.index(student)] = student
            # ulozeni udaju jednotlivych studentu
            self._student_data[student] = (student.required_subjects,
                                           student._possible_comb,
                                           student.chosen_comb)

        for index in self._new_students:
            self._gmainwindow.student_panel.add_gstudent(self._new_students[index]) 
            GStudentControlDialog.add_student_to_model(self._new_students[index])

    def redo(self) -> None:
        # nacteni novych predmetu
        if self._new_subjs:
            for subj in self._new_subjs:
                self._model.add_subject(subj)
            self._gmainwindow.subject_list_updated.emit(self._new_subjs)
        
        # nacteni smazanych studentu
        for index in self._new_students:
            student = self._new_students[index]
            # nacteni dat studenta
            student.required_subjects = self._student_data[student][0]
            student._possible_comb = self._student_data[student][1]
            if self._student_data[student][2] is not None:
                student.set_comb(student._possible_comb.index(self._student_data[student][2]))

            # vlozeni do vsech modelu a oken
            self._model.add_student(self._new_students[index], index)
            self._gmainwindow.student_panel.add_gstudent(self._new_students[index], index)
            GStudentControlDialog.add_student_to_model(self._new_students[index])
        
        # aktualizace pocitadla studentu na predmet
        self._gmainwindow.subject_counter_changed.emit()

    def undo(self) -> None:
        # mazani nove pridanych predmetu
        if self._new_subjs:
            for subj in self._new_subjs:
                self._model.remove_subject(subj)
            self._gmainwindow.subject_list_updated.emit(self._new_subjs)

        # mazani nove pridanych studentu ze vsech modelu a oken
        for index in self._new_students:
            self._model.remove_student(self._new_students[index].id)
            self._gmainwindow.student_panel.delete_student_id(self._new_students[index].id)
            GStudentControlDialog.delete_student_from_model(self._new_students[index].id)

        # aktualizace pocitadla studentu na predmet
        self._gmainwindow.subject_counter_changed.emit()
        
class MainWindowImportSubjects(Command):

    def __init__(self, parent: 'gui_lib.g_main_window.GMainWindow', filename: str) -> None:
        self._gmainwindow = parent
        self._model = parent.model
        self._fn = filename
        super().__init__()

    def execute(self) -> None:
        self._new_subj = self._model.load_file_subjects(self._fn)
        self._gmainwindow.subject_list_updated.emit(self._new_subj)

    def redo(self) -> None:
        for subj in self._new_subj:
            self._model.add_subject(subj)
        self._gmainwindow.subject_list_updated.emit(self._new_subj)

    def undo(self) -> None:
        for subj in self._new_subj:
            self._model.remove_subject(subj)
        self._gmainwindow.subject_list_updated.emit(self._new_subj)

from sort_lib.command import Command

import gui_lib.g_subject_control_dialog

class SubjectControlAction(Command):

    def __init__(self, dialog: 'gui_lib.g_subject_control_dialog.GSubjectControlDialog'):
        self.dialog = dialog
        self._gmainwindow = dialog.base_gparent
        self._changes = dialog.changes


    def execute(self) -> None:
        for subj in self._changes:
            if self._gmainwindow.model.subjects.get(subj) is None:
                self._gmainwindow.model.add_subject(subj)
            else:
                self._gmainwindow.model.remove_subject(subj)
        self._gmainwindow.subject_list_updated.emit(self._changes)

    def redo(self) -> None:
        self.execute()

    def undo(self) -> None:
        self.execute()
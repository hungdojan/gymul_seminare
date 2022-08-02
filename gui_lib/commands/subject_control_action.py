from sort_lib.command import Command

import gui_lib.g_subject_control_dialog
from sort_lib.file_log import FileLog

class SubjectControlAction(Command):

    def __init__(self, dialog: 'gui_lib.g_subject_control_dialog.GSubjectControlDialog'):
        self.dialog = dialog
        self._gmainwindow = dialog.base_gparent
        self._changes = dialog.changes


    def execute(self) -> None:
        FileLog.loggers['default'].info('CMD: Execute SubjectControlAction')
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
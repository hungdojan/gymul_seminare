from sort_lib.command import Command

import gui_lib.g_subject

class SelectSubjectAction(Command):

    def __init__(self, parent: 'gui_lib.g_subject.GSubject') -> None:
        self._parent = parent
        self._subj_name = parent.name
        self._day_panel = parent.base_gparent._base_gparent
        self._gday = parent.base_gparent
        self._index = self._day_panel.lof_gdays.index(self._gday)
        super().__init__()

    def execute(self) -> None:
        self._parent.setProperty('isSelected', not self._parent.property('isSelected'))

        # meni zobrazeni g-predmetu
        if self._parent.property('isSelected'):
            # TODO: preserve model with students??
            self._parent.model = self._parent.base_gparent.model.add_subject_name(self._parent.name)
        else:
            self._parent.base_gparent.model.remove_subject(self._parent.name)
            self._parent.model = None

        self._parent.content_update()
        self._parent.selected_subjects_changed.emit()
        self._parent.base_gparent._base_gparent._base_gparent.view_updated.emit()

    def redo(self) -> None:
        self._gday = self._day_panel.lof_gdays[self._index]
        self._parent = self._gday.gsubjects[self._subj_name]
        self.execute()

    def undo(self) -> None:
        self._gday = self._day_panel.lof_gdays[self._index]
        self._parent = self._gday.gsubjects[self._subj_name]
        self.execute()
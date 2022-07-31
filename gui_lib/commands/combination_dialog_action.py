from sort_lib.command import Command
import gui_lib.g_combination_dialog

class CombinationDialogAction(Command):

    def __init__(self, parent: 'gui_lib.g_combination_dialog.GCombinationDialog'):
        self._parent = parent
        self.old_index = -1 if parent.gstudent.model.chosen_comb is None \
                            else parent.gstudent.model.possible_comb.index(parent.gstudent.model.chosen_comb)
        self.new_index = parent.subjs.currentIndex() - 1

    def execute(self) -> None:
        self._parent.gstudent.model.set_comb(self.new_index)
        self._parent.gmainwindow.view_updated.emit()

    def redo(self) -> None:
        self.execute()

    def undo(self) -> None:
        self._parent.gstudent.model.set_comb(self.old_index)
        self._parent.gmainwindow.view_updated.emit()
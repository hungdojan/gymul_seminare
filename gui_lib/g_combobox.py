from PySide6.QtWidgets import QComboBox, QWidget
from PySide6.QtGui import QWheelEvent
from PySide6.QtCore import Qt
import gui_lib.g_student

class GComboBox(QComboBox):

    def __init__(self, base_gparent: 'gui_lib.g_student.GStudent', index: int):
        super().__init__()

        self._base_gparent = base_gparent
        self._index = index

        # nastaveni ComboBoxu
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setEditable(True)
        self.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit().setReadOnly(True)

        # nastaveni dat
        self.setModel(self._base_gparent._base_gparent.subject_model)
        self.update_view()
    

    @property
    def base_gparent(self) -> QWidget:
        return self._base_gparent
    

    def wheelEvent(self, e: QWheelEvent) -> None:
        # ignore event
        pass
    

    def update_view(self):
        if self._base_gparent.model.required_subjects is None:
            return
        subj_name = '-' if self._base_gparent.model.required_subjects[self._index] is None \
                        else self._base_gparent.model.required_subjects[self._index]
        item_index = self.findText(subj_name)
        self.setCurrentIndex(item_index)
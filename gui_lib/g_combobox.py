from PySide6.QtWidgets import QComboBox, QWidget
from PySide6.QtGui import QWheelEvent
from PySide6.QtCore import Qt

class GComboBox(QComboBox):

    def __init__(self, parent: QWidget=None):
        super().__init__(parent)

        # nastaveni ComboBoxu
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setEditable(True)
        self.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit().setReadOnly(True)
    

    def wheelEvent(self, e: QWheelEvent) -> None:
        # ignore event
        pass
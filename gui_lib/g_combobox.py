from PySide6.QtWidgets import QComboBox, QWidget
import PySide6.QtGui as QtGui

class GComboBox(QComboBox):

    def __init__(self, parent: QWidget=None):
        super().__init__(parent)
    

    def wheelEvent(self, e: QtGui.QWheelEvent) -> None:
        pass


    def focusOutEvent(self, e: QtGui.QFocusEvent) -> None:
        self.setCurrentIndex(self.currentIndex())
        super().focusOutEvent(e)    

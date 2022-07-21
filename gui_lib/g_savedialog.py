from PySide6.QtWidgets import QMessageBox, QWidget

class GSaveDialog(QMessageBox):

    def __init__(self, parent: QWidget, title: str, text: str):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setText(text)
        self.setStandardButtons(QMessageBox.Save | QMessageBox.ButtonMask.No | QMessageBox.Cancel)
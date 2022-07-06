from PySide6.QtWidgets import QDialog

class GAboutDialog(QDialog):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle('O aplikaci')
        # TODO:
        self.show()
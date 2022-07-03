from PySide6.QtWidgets import QDialog

class GAboutDialog(QDialog):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('O aplikaci')
        # TODO:
from PySide6.QtWidgets import QDialog

class GHelpDialog(QDialog):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Nápověda')

from PySide6.QtWidgets import QDialog, QVBoxLayout

class GAboutDialog(QDialog):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle('O aplikaci')

        self.setLayout(QVBoxLayout())
        self._setupUI()
        # TODO:
        self.show()
    

    def _setupUI(self):
        pass
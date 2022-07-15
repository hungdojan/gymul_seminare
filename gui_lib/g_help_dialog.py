from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextBrowser
from PySide6.QtCore import QFile, QIODevice, Qt
import rc

class GHelpDialog(QDialog):
    """Trida pro okno s napovedou."""
    
    def __init__(self, parent):
        super().__init__(parent, Qt.Dialog)
        self.setWindowTitle('Nápověda')
        self.setMinimumWidth(1000)
        self.setMinimumHeight(500)

        # nacteni obsahu navodu
        content_tb = QTextBrowser()
        content_text = QFile(':/help.md')
        content_text.open(QIODevice.OpenModeFlag.ReadOnly)
        content_tb.setMarkdown(str(content_text.readAll(), 'utf-8'))

        # uprava velikosti fontu
        font = content_tb.font()
        font.setPointSize(13)
        content_tb.setFont(font)

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().addWidget(content_tb)


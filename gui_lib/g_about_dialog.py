from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QFormLayout, QFrame, QStyle, QStyleOption
from PySide6.QtGui import QPainter, QPaintEvent
from PySide6.QtCore import Qt

class GAboutDialog(QDialog):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle('O aplikaci')
        font = self.font()
        font.setPointSize(13)
        self.setFont(font)

        self.setLayout(QVBoxLayout())
        self._setupUI()
    

    def _setupUI(self):
        """Vygenerovani okna 'O aplikaci'."""
        name_lbl = QLabel('Semináře')
        name_lbl.setObjectName('AppNameLabel')
        self.layout().addWidget(name_lbl, alignment=Qt.AlignmentFlag.AlignHCenter)

        about_lbl = QLabel('Tento program slouží k tvorbě rozvrhu seminárních předmětů a\nroztřízení studentů do nich.')
        about_lbl.setAlignment(Qt.AlignHCenter)
        self.layout().addWidget(about_lbl, alignment=Qt.AlignHCenter)

        form_frame = QFrame()
        form_frame.setLayout(QFormLayout())
        form_frame.layout().setContentsMargins(0,0,0,0)

        author_lbl = QLabel('Hung Do')
        author_lbl.setAlignment(Qt.AlignCenter)
        form_frame.layout().addRow(QLabel('Autor:'), author_lbl)

        mail_lbl = QLabel()
        mail_lbl.setTextFormat(Qt.RichText)
        mail_lbl.setTextInteractionFlags(Qt.TextBrowserInteraction)
        mail_lbl.setOpenExternalLinks(True)
        mail_lbl.setText("<a href='mailto:hungdojan@gmail.com'>hungdojan@gmail.com</a>")
        mail_lbl.setAlignment(Qt.AlignCenter)
        form_frame.layout().addRow(QLabel('Email:'), mail_lbl)

        gh_lbl = QLabel()
        gh_lbl.setTextFormat(Qt.RichText)
        gh_lbl.setTextInteractionFlags(Qt.TextBrowserInteraction)
        gh_lbl.setOpenExternalLinks(True)
        gh_lbl.setText("<a href='https://github.com/hungdojan/gymul_seminare'>Link</a>")
        gh_lbl.setAlignment(Qt.AlignCenter)
        form_frame.layout().addRow(QLabel('Github page:'), gh_lbl)
        
        version_lbl = QLabel('0.1.1')
        version_lbl.setAlignment(Qt.AlignCenter)
        form_frame.layout().addRow(QLabel('Version:'), version_lbl)

        license_lbl = QLabel('MIT')
        license_lbl.setAlignment(Qt.AlignCenter)
        form_frame.layout().addRow(QLabel('Licence'), license_lbl)

        self.layout().addWidget(form_frame, alignment=Qt.AlignHCenter)

    
    def paintEvent(self, event: QPaintEvent) -> None:
        """Predefinuje funkci paintEvent.

        Args:
            event (QPaintEvent): Promenna udalosti QPaintEvent.
        """
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, p, self)
        super().paintEvent(event)
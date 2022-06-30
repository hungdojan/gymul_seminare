from PySide6.QtWidgets import QComboBox, QWidget, QStyleOption, QStyle
from PySide6.QtGui import QPaintEvent, QPainter, QKeyEvent, QWheelEvent, QFocusEvent
from PySide6.QtCore import Qt

class GComboBox(QComboBox):

    def __init__(self, parent: QWidget=None):
        super().__init__(parent)
        self.setProperty('valid', 'true')
        self.setDisabled(True)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    

    def wheelEvent(self, e: QWheelEvent) -> None:
        # ignore event
        pass
    

    def focusInEvent(self, e: QFocusEvent) -> None:
        # ignore event
        pass

    
    def keyPressEvent(self, e: QKeyEvent) -> None:
        # ignore event
        pass


    def update_style(self):
        """Aktualizuje vzhled GComboBox"""
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()


    def paintEvent(self, event: QPaintEvent) -> None:
        """Predefinuje funkci paintEvent

        Args:
            event (QPaintEvent): Promenna udalosti QPaintEvent
        """
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_CustomBase, opt, p, self)
        super().paintEvent(event)
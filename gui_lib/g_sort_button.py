from PySide6.QtWidgets import QPushButton, QStyle, QStyleOption
from PySide6.QtGui import QPaintEvent, QPainter
from PySide6.QtCore import Slot

class GSortButton(QPushButton):
    """Rozsirena trida QPushButton o komunikaci s QCSS."""
    def __init__(self, name: str):
        super().__init__(name)
        self.setProperty('isSorted', False)

    
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


    def update_style(self):
        """Aktualizuje vzhled GSortButton."""
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()
    

    @Slot(bool)
    def sort_button_update(self, value: bool):
        """Aktualizuje stav GSortButton."""
        self.setProperty('isSorted', value)
        self.update_style()
from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QDialogButtonBox, QComboBox, QWidget
import gui_lib.g_student

class GCombinationDialog(QDialog):

    def __init__(self, gstudent: 'gui_lib.g_student.GStudent'):
        super().__init__()
        self.setWindowTitle('Výběr kombinace předmětů')
        self.gstudent = gstudent

        # vrchni cast okna
        self.setLayout(QVBoxLayout())
        self.create_combobox()
        form_w = QWidget()
        form_w.setLayout(QFormLayout())
        form_w.layout().addRow('Vybraná kombinace', self.subjs)
        self.layout().addWidget(form_w)

        # tlacitka v dolni casti okna
        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        self.layout().addWidget(button_box)
    

    def create_combobox(self) -> None:
        """Vytvori ComboBox s vybranymi moznostmi"""
        self.subjs = QComboBox()
        self.subjs.addItem('Žádná')
        combs = list(map(lambda x: str(x), self.gstudent.model.possible_comb))
        self.subjs.addItems(combs)

        # zobrazit momentalni kombinaci
        if self.gstudent.model.chosen_comb is None:
            index = 0
        else:
            index = self.gstudent.model.possible_comb.index(self.gstudent.model.chosen_comb) + 1
        self.subjs.setCurrentIndex(index)

        return self.subjs
    

    def accept(self) -> None:
        """Akce po uspesnem ukonceni dialogoveho okna"""
        # aktualizace kombinace a vyvolani signalu k aktualizaci
        self.gstudent.model.set_comb(self.subjs.currentIndex() - 1)
        self.gstudent.base_gparent.view_updated.emit()
        super().accept()
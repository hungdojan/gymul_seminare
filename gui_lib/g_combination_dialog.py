from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QDialogButtonBox, QComboBox, QWidget
import gui_lib.g_student

class GCombinationDialog(QDialog):

    def __init__(self, gstudent: 'gui_lib.g_student.GStudent'):
        super().__init__()
        self.setWindowTitle('Výběr kombinace předmětů')
        self.gstudent = gstudent

        self.setLayout(QVBoxLayout())
        self.subjs = self.get_combobox()
        # TODO: add items
        form_w = QWidget()
        form_w.setLayout(QFormLayout())
        form_w.layout().addRow('Vybraná kombinace', self.subjs)
        self.layout().addWidget(form_w)

        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        self.layout().addWidget(button_box)
    

    def get_combobox(self):
        cb = QComboBox()
        cb.addItem('Žádná')
        combs = list(map(lambda x: str(x), self.gstudent.model.possible_comb))
        cb.addItems(combs)

        # zobrazit momentalni kombinaci
        if self.gstudent.model.chosen_comb is None:
            index = 0
        else:
            index = self.gstudent.model.possible_comb.index(self.gstudent.model.chosen_comb) + 1
        cb.setCurrentIndex(index)

        return cb
    

    def accept(self) -> None:
        # TODO:
        self.gstudent.model.set_comb(self.subjs.currentIndex() - 1)
        self.gstudent.update_content()
        super().accept()
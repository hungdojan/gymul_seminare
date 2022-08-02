from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QDialogButtonBox, QComboBox, QWidget
import gui_lib.g_student
import gui_lib.g_main_window
from gui_lib.commands.combination_dialog_action import CombinationDialogAction
from sort_lib.file_log import FileLog

class GCombinationDialog(QDialog):

    def __init__(self, gstudent: 'gui_lib.g_student.GStudent'):
        super().__init__()
        self.setWindowTitle('Výběr kombinace předmětů')
        self.gstudent = gstudent
        self._gmainwindow = gstudent.base_gparent.base_gparent

        self._setupUI()
        FileLog.loggers['default'].info('FE: GCombinationDialog window opened')
    

    @property
    def gmainwindow(self) -> 'gui_lib.g_main_window.GMainWindow':
        return self._gmainwindow


    def _setupUI(self):
        """Vygeneruje okno GCombinationDialog."""

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
        chosen_comb = self.gstudent.model.possible_comb[self.subjs.currentIndex() - 1] \
                      if self.subjs.currentIndex() > 0 else None
        if chosen_comb != self.gstudent.model.chosen_comb:
            FileLog.loggers['default'].info(f'FE: Change student "{self.gstudent.model.id}" chosen combination: {self.gstudent.model.chosen_comb} -> {chosen_comb}')
            self._gmainwindow.command_builder.execute(CombinationDialogAction(self))
        FileLog.loggers['default'].info('GCombinationDialog window accepted')
        super().accept()
    
    def reject(self) -> None:
        FileLog.loggers['default'].info('GCombinationDialog window rejected')
        super().reject()
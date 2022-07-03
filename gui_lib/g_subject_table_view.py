from PySide6.QtWidgets import QTableView, QAbstractItemView, QHeaderView
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtCore import Qt, Slot, Signal, QAbstractTableModel, QModelIndex
import gui_lib.g_main_window

class GSubjectTableView(QTableView):

    def __init__(self, base_gparent: 'gui_lib.g_main_window.GMainWindow'):
        super().__init__()
        self._base_gparent = base_gparent
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        model = QStandardItemModel(len(self._base_gparent.model.subjects), 2)
        model.setHeaderData(0, Qt.Horizontal, "Předmět")
        model.setHeaderData(1, Qt.Horizontal, "Počet studentů")
        stats = self._base_gparent.model.get_students_per_subject()
        keys = sorted(stats.items(), key=lambda x: x[1], reverse=True)
        for i in range(len(keys)):
            name = model.index(i, 0, QModelIndex())
            model.setData(name, keys[i][0])
            value = model.index(i, 1, QModelIndex())
            model.setData(value, stats[keys[i][0]])
        
        # nastaveni tabulky (read-only)
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.setFocusPolicy(Qt.NoFocus)
        self.horizontalHeader().setHighlightSections(True)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.horizontalHeader().sectionClicked.connect(self.header_clicked)

        self.setModel(model)
    

    @Slot()
    def update_subjects(self):
        # TODO:
        pass


    @Slot(int)
    def header_clicked(self, index):
        # TODO:
        print('clicked:', index)
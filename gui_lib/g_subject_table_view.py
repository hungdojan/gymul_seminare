from PySide6.QtWidgets import QTableView, QAbstractItemView, QHeaderView
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtCore import Qt, Slot, Signal, QModelIndex, QSortFilterProxyModel
import gui_lib.g_main_window

class GSubjectTableView(QTableView):

    class ProxyModel(QSortFilterProxyModel):
        
        def __init__(self):
            super().__init__()
        
        def lessThan(self, source_left, source_right) -> bool:
            if source_left.data().isnumeric() and source_right.data().isnumeric():
                return int(source_left.data()) < int(source_right.data())
            return super().lessThan(source_left, source_right)


    def __init__(self, base_gparent: 'gui_lib.g_main_window.GMainWindow'):
        super().__init__()
        self._base_gparent = base_gparent
        self._sort_by_names = False

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # vytvoreni modelu
        self.data_model = QStandardItemModel()
        self.data_model.setColumnCount(2)
        self.data_model.setHorizontalHeaderLabels(['Předmět','Počet studentů'])

        proxy_model = GSubjectTableView.ProxyModel()
        proxy_model.setSourceModel(self.data_model)
        
        # prida data
        stats = self._base_gparent.model.get_students_per_subject()
        for i in stats:
            name = QStandardItem(i)
            name.setTextAlignment(Qt.AlignCenter)
            counter = QStandardItem(str(stats[i]))
            counter.setTextAlignment(Qt.AlignCenter)
            self.data_model.appendRow([name, counter])
        
        
        # nastaveni tabulky (read-only)
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.setFocusPolicy(Qt.NoFocus)
        self.horizontalHeader().setHighlightSections(True)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().setVisible(False)
        self.setSortingEnabled(True)
        font = self.font()
        font.setPointSize(11)
        self.setFont(font)

        self.setModel(proxy_model)
        self.sortByColumn(1, Qt.DescendingOrder)
    

    def clear_data(self):
        # smaze vsechna data z modelu
        self.data_model.removeRows(0, self.data_model().rowCount() - 1)
    

    def get_names(self) -> list:
        return list(map(
            lambda i: self.data_model.data(self.data_model().index(i, 0, QModelIndex())),
            range(self.data_model.rowCount())
        ))


    @Slot(list)
    def update_subjects_list(self, new_subjects: list):

        current_names = self.get_names()

        stats = self._base_gparent.model.get_students_per_subject()
        for subj in new_subjects:
            if subj in current_names:
                row_index = self.get_names().index(subj)
                self.data_model.removeRow(row_index)
            else:
                name = QStandardItem(subj)
                name.setTextAlignment(Qt.AlignCenter)
                value = QStandardItem(str(stats[subj]))
                value.setTextAlignment(Qt.AlignCenter)
                self.data_model.appendRow([name, value])


    @Slot()
    def update_subject_counter(self):
        """Aktualizuje model o pocet studentu"""

        stats = self._base_gparent.model.get_students_per_subject()
        for i in range(self.data_model.rowCount()):
            name = self.data_model.data(self.data_model.index(i, 0, QModelIndex()))
            value_model = self.data_model.index(i, 1, QModelIndex())
            self.data_model.setData(value_model, str(stats[name]))
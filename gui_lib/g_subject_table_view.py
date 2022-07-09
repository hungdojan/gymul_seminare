from PySide6.QtWidgets import QTableView, QAbstractItemView, QHeaderView
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtCore import Qt, Slot, QModelIndex, QSortFilterProxyModel
import gui_lib.g_main_window

class GSubjectTableView(QTableView):
    """Trida zobrazujici seznam predmetu s pocty zaku."""

    class ProxyModel(QSortFilterProxyModel):
        
        def __init__(self):
            super().__init__()
        
        def lessThan(self, source_left, source_right) -> bool:
            # Prepis pro porovnani cisel
            if source_left.data().isnumeric() and source_right.data().isnumeric():
                return int(source_left.data()) < int(source_right.data())
            return super().lessThan(source_left, source_right)


    def __init__(self, base_gparent: 'gui_lib.g_main_window.GMainWindow'):
        super().__init__()
        self._base_gparent = base_gparent
        self._sort_by_names = False

        self.generate_model()
        
        # nastaveni tabulky (read-only)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.setFocusPolicy(Qt.NoFocus)
        self.setSortingEnabled(True)

        # nastaveni hlavicky
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setHighlightSections(True)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().setVisible(False)
        
        # nastaveni vzhledu
        font = self.font()
        font.setPointSize(11)
        self.setFont(font)

        self.sortByColumn(1, Qt.DescendingOrder)
    

    def generate_model(self):
        """Vygeneruje model pro TableView"""
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
        self.setModel(proxy_model)
    

    def clear_data(self):
        """Smaze vsechna data z modelu."""
        self.data_model.removeRows(0, self.data_model().rowCount() - 1)
    

    def get_names(self) -> list:
        """Vraci seznam jmen predmetu v modelu.

        Returns:
            list: Seznam jmen v modelu.
        """
        return [self.data_model.data(self.data_model.index(i, 0, QModelIndex()))
                for i in range(self.data_model.rowCount())]


    @Slot(list)
    def update_subjects_list(self, new_subjects: list):
        """Aktualizuje seznam predmetu v modelu.

        Pokud predmet v _new_subjects_ se nachazi jiz v modelu, je z modelu odstranen.
        V opacnem pripade je pridan do modelu.

        Args:
            new_subjects (list): Seznam jmen predmetu, kterych se zmena tyka.
        """

        current_names = self.get_names()

        # aktualizovany seznam s poctem studentu na predmet
        stats = self._base_gparent.model.get_students_per_subject()

        for subj in new_subjects:
            # odstraneni predmetu
            if subj in current_names:
                row_index = self.get_names().index(subj)
                self.data_model.removeRow(row_index)
            # pridani predmetu
            else:
                name = QStandardItem(subj)
                name.setTextAlignment(Qt.AlignCenter)
                value = QStandardItem(str(stats[subj]))
                value.setTextAlignment(Qt.AlignCenter)
                self.data_model.appendRow([name, value])


    @Slot()
    def subject_counter_changed(self):
        """Aktualizuje model o pocet studentu."""

        stats = self._base_gparent.model.get_students_per_subject()
        for i in range(self.data_model.rowCount()):
            name = self.data_model.data(self.data_model.index(i, 0, QModelIndex()))
            value_model = self.data_model.index(i, 1, QModelIndex())
            self.data_model.setData(value_model, str(stats[name]))
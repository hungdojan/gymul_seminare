from PySide6.QtWidgets import QTableView, QAbstractItemView, QHeaderView
from PySide6.QtCore import Qt, QSortFilterProxyModel
import gui_lib.g_main_window
from gui_lib.subject_attendance_model import SubjectAttendanceModel

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

        model = SubjectAttendanceModel(self._base_gparent.model)
        self._base_gparent.subject_counter_changed.connect(model.update_model_counter)
        self._base_gparent.subject_list_updated.connect(model.update_model_list)
        self._base_gparent.subject_list_clear.connect(model.clear_model)

        proxy_model = GSubjectTableView.ProxyModel()
        proxy_model.setSourceModel(model)
        
        self.setModel(proxy_model)
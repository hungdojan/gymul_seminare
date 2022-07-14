from PySide6.QtCore import Signal, Slot, Qt, QModelIndex
from PySide6.QtGui import QStandardItem, QStandardItemModel

from sort_lib.sort import Sort

class SubjectAttendanceModel(QStandardItemModel):
    
    def __init__(self, base_model: Sort):
        super().__init__()
        self._base_model = base_model
        self._subjects = {}
        self._sort_info = None
        self.__initialize_model()

    
    @property
    def base_model(self) -> Sort:
        return self._base_model
    

    @base_model.setter
    def base_model(self, value: Sort):
        self.clear_model()
        self._base_model = value
        self.__initialize_model()
    

    def __initialize_model(self):
        """Naplni model daty."""
        if self._base_model is None:
            return
        subjects = self._base_model.subjects
        self.setHorizontalHeaderLabels(['Předmět','Počet studentů'])
        list(map(lambda x: self.__add_item(x, len(subjects[x])), subjects))
    

    def __add_item(self, name: str, value: int) -> None:
        """Prida polozku do modelu.

        Args:
            name (str): Jmeno predmetu.
            value (int): Pocet zapsanych studentu v predmetu.
        """
        name_item = QStandardItem(name)
        name_item.setTextAlignment(Qt.AlignCenter)
        value_item = QStandardItem(str(value))
        value_item.setTextAlignment(Qt.AlignCenter)

        self.appendRow([name_item, value_item])
        self._subjects[name] = value
    

    def __remove_item(self, name: str) -> None:
        """Vyjme polozku z modelu.

        Args:
            name (str): Jmeno predmetu.
        """
        try:
            index = list(self._subjects.keys()).index(name)
        except ValueError:
            return
        self.removeRow(index)
        del self._subjects[name]
    

    def __sort_subjects(self) -> None:
        """Setridi pomocnou tabulku."""
        if self._sort_info is None:
            return
        order = self._sort_info[1] == Qt.DescendingOrder
        self._subjects = dict(sorted(self._subjects.items(),
                                     key=lambda x: x[self._sort_info[0]],
                                     reverse=order))

    @Slot()
    def clear_model(self) -> None:
        """Smaze obsah modelu."""
        self.removeRows(0, self.rowCount())
        self._subjects.clear()
    

    @Slot(int, Qt.SortOrder)
    def update_sort_info(self, index: int, order: Qt.SortOrder) -> None:
        """Aktualizuje nastaveni filtru."""
        self._sort_info = (index, order)
    

    @Slot(list)
    def update_model_list(self, l: list) -> None:
        """Aktualizuje seznam predmetu v modelu.

        Args:
            l (list): Seznam predmetu, ktere se do/z modelu pridaly/odebraly.
        """
        self.__sort_subjects()
        for s in l:
            if self._subjects.get(s) is not None:
                self.__remove_item(s)
            else:
                self.__add_item(s, 0)
    

    @Slot()
    def update_model_counter(self) -> None:
        """Aktualizace poctu studentu na predmetu."""
        self.__sort_subjects()
        for subj in self._subjects:
            if len(self._base_model.subjects[subj]) != self._subjects[subj]:
                self._subjects[subj] = len(self._base_model.subjects[subj])
                index = list(self._subjects.keys()).index(subj)
                value = self.index(index, 1, QModelIndex())
                self.setData(value, str(self._subjects[subj]))
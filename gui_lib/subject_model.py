from email.mime import base
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Slot, Qt, Signal
from sort_lib.sort import Sort

class SubjectModel(QStandardItemModel):

    model_updated = Signal()

    def __init__(self, base_model: Sort):
        super().__init__()
        self._base_model = base_model
        self._subjects = []
        self.__initialize_model()
        self.__available = True

    
    @property
    def available(self) -> bool:
        return self.__available
    

    @property
    def base_model(self) -> Sort:
        return self._base_model

    
    @base_model.setter
    def base_model(self, value: Sort):
        if not isinstance(value, Sort):
            return
        self.clear_model()
        self.__available = False
        self._base_model = value
        self.__initialize_model()
        self.__available = True

    
    def __initialize_model(self):
        """Naplni model daty."""
        if self._base_model is None:
            return
        self.__add_item('-')
        list(map(lambda x: self.__add_item(x), self._base_model.subjects.keys()))
        self.sort_model()

    
    def __add_item(self, text: str):
        """Prida polozku do modelu.

        Args:
            text (str): Jmeno predmetu.
        """
        item = QStandardItem(text)
        item.setTextAlignment(Qt.AlignHCenter)
        self.appendRow(item)
        self._subjects.append(text)
    

    def __remove_item(self, text: str):
        """Vyjme polozku z modelu.

        V pripade, ze polozka nebyla nalezena v modelu, je akce ignorovana.

        Args:
            text (str): Jmeno predmetu.
        """
        try:
            index = self._subjects.index(text)
        except ValueError:
            return
        self._subjects.remove(text)
        self.removeRow(index)
    

    def sort_model(self):
        """Seradi polozky modelu podle jmena."""
        self.sort(0)
        self._subjects.sort()
    

    @Slot()
    def clear_model(self):
        self.__available = False
        self.removeRows(0, self.rowCount())
        self._subjects.clear()
        self.__available = True
    

    @Slot(list)
    def update_list(self, l: list):
        self.__available = False
        for subj in l:
            if subj in self._subjects:
                self.__remove_item(subj)
            else:
                self.__add_item(subj)
        self.sort_model()
        self.model_updated.emit()
        self.__available = True
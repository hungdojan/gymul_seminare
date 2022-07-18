from PySide6.QtWidgets import QDialog, QLineEdit, QGridLayout, QListView, QAbstractItemView, \
                              QDialogButtonBox, QPushButton
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import QModelIndex, Qt, Slot

import gui_lib.g_main_window

class GSubjectControlDialog(QDialog):

    def __init__(self, base_gparent: 'gui_lib.g_main_window.GMainWindow'):
        super().__init__()
        self._base_gparent = base_gparent
        self._support_model: list = []
        self._original_model = base_gparent.subject_model
        self._copy_model()
        self._changes: list[str] = []
        self._setupUI()
        self.setWindowTitle('Správce předmětů')

    
    def _copy_model(self) -> None:
        """Vytvori kopii dosavadniho modelu"""
        self._subject_model = QStandardItemModel()
        for i in range(1, self._original_model.rowCount()):
            name = self._original_model.data(self._original_model.index(i, 0, QModelIndex()))
            item = QStandardItem(name)
            item.setTextAlignment(Qt.AlignCenter)
            self._subject_model.appendRow(item)
            self._support_model.append(name)


    def _setupUI(self) -> None:
        """Vygenerovani obsahu GSubjectControl."""
        self.setLayout(QGridLayout())

        self.text_field = QLineEdit()
        self.text_field.setPlaceholderText('Jmeno predmetu')
        self.layout().addWidget(self.text_field, 0, 0)

        add_button = QPushButton('Přidat')
        add_button.clicked.connect(self.add_new_subject)
        self.layout().addWidget(add_button, 0, 1)

        self.list_view = QListView()
        self.list_view.setModel(self._subject_model)
        self.list_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.list_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.layout().addWidget(self.list_view, 1, 0, 3, 1)
        

        delete_button = QPushButton('Smazat')
        delete_button.clicked.connect(self.delete_selected_subjects)
        self.layout().addWidget(delete_button, 1 ,1)

        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        self.layout().addWidget(button_box, 4, 1)
    

    def accept(self) -> None:
        """Aktualizace originalniho modelu."""
        self._subject_model.deleteLater()
        for subj in self._changes:
            if self._base_gparent.model.subjects.get(subj) is None:
                self._base_gparent.model.add_subject(subj)
            else:
                self._base_gparent.model.remove_subject(subj)
        self._base_gparent.subject_list_updated.emit(self._changes)
        super().accept()
    

    @Slot()
    def add_new_subject(self) -> None:
        """Prida novy predmetu do docasneho modelu."""
        if not self.text_field.text():
            return
        name = self.text_field.text()
        if name in self._support_model:
            # TODO: warning
            self.text_field.clear()
            return
        item = QStandardItem(name)
        item.setTextAlignment(Qt.AlignCenter)
        self._subject_model.appendRow(item)
        self._support_model.append(name)
        self._changes.append(name)

        self.text_field.clear()


    @Slot()
    def delete_selected_subjects(self) -> None:
        """Smaze vybrane predmety z docasneho modelu."""
        indices = [model.row() for model in self.list_view.selectionModel().selectedIndexes()]
        indices = sorted(indices, reverse=True)
        # mazani od zadu
        for i in indices:
            self._subject_model.removeRow(i)
            self._changes.append(self._support_model[i])
            self._support_model.remove(self._support_model[i])
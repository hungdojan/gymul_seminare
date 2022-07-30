from PySide6.QtWidgets import *
from PySide6.QtGui import QStandardItem, QStandardItemModel, QKeySequence, QShortcut
from PySide6.QtCore import Qt, QModelIndex, Slot

import gui_lib.g_main_window
from gui_lib.g_subject_table_view import ProxyModel
from gui_lib.commands.student_control_actions import *

import sort_lib.sort
from  sort_lib.student import Student

class GStudentControlDialog(QDialog):

    class GStudentControlEditDialog(QDialog):
        
        def __init__(self, student_model: Student, gmainwindow: 'gui_lib.g_main_window.GMainWindow', new_student: bool=False):
            super().__init__()
            self._model = student_model
            self._gmainwindow = gmainwindow
            self._setupUI()
            # pravdivosti hodnota znacici, o jakou akci se jedna (pridat/upravit)
            self._to_add_student = new_student
        
        @property
        def model(self) -> Student:
            return self._model


        @property
        def gmainwindow(self) -> 'gui_lib.g_main_window.GMainWindow':
            return self._gmainwindow


        def _setupUI(self) -> None:
            """Vygeneruje obsah GStudentControlEditDialog."""
            self.setLayout(QVBoxLayout())

            form_layout = QFormLayout()
            self.fname_le = QLineEdit(self._model.first_name)
            self.fname_le.setPlaceholderText('Jméno')
            self.lname_le = QLineEdit(self._model.last_name)
            self.lname_le.setPlaceholderText('Příjmení')
            self.class_le = QLineEdit(self._model.class_id)
            self.class_le.setPlaceholderText('Třída')
            self.subject_cb = [QComboBox() for _ in range(3)]

            form_layout.addRow("Jméno:", self.fname_le)
            form_layout.addRow("Příjmení:", self.lname_le)
            form_layout.addRow("Třída:", self.class_le)

            for i in range(len(self.subject_cb)):
                self.subject_cb[i].setModel(self._gmainwindow.subject_model)
                text = self._model.required_subjects[i] if self._model.required_subjects[i] else '-'
                index = self.subject_cb[i].findText(text)
                self.subject_cb[i].setCurrentIndex(index)
                form_layout.addRow(f'{i+1}. předmět:', self.subject_cb[i])

            self.layout().addLayout(form_layout)
            
            button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
            button_box.accepted.connect(self.accept)
            button_box.rejected.connect(self.reject)
            self.layout().addWidget(button_box)
        

        def accept(self) -> None:
            """Aktualizace modelu v pripade uspesneho ukonceni dialogu."""
            if self._to_add_student:
                # u pridani studenta akci vytvari volajici (GStudentControlDialog)
                self._model.first_name = self.fname_le.text()
                self._model.last_name = self.lname_le.text()
                self._model.class_id = self.class_le.text()
                comb = tuple([cb.currentText() if cb.currentText() != '-' else None
                            for cb in self.subject_cb])
                if comb != self._model.required_subjects:
                    self._model.required_subjects = comb
                    self._gmainwindow.subject_counter_changed.emit()
            else:
                # pri uprave dat akci vyvolava tento dialog (GStudentControlDialogEdit)
                # vlozi akci do command builderu pro moznost undo/redo
                self._gmainwindow.command_builder.execute(StudentControlEdit(self))
            super().accept()

    # model studentu
    __student_model = None
    __sort_model = None

    @classmethod
    def __init_model(cls, model: 'sort_lib.sort.Sort'):
        cls.__sort_model = model
        cls.__student_model = QStandardItemModel()
        cls.__student_model.setHorizontalHeaderLabels(['ID', 'Jméno', 'Příjmení', 'Třída'])
        for student in cls.__sort_model.students:
            cls.add_student_to_model(student)
    
    @classmethod
    def add_student_to_model(cls, student: Student) -> None:
        """Prida novy radek se studentem.

        Args:
            student (Student): Instance studenta.
        """
        if cls.__student_model is None:
            return
        id_item = QStandardItem(str(student.id))
        id_item.setTextAlignment(Qt.AlignCenter)
        fname_item = QStandardItem(str(student.first_name))
        fname_item.setTextAlignment(Qt.AlignCenter)
        lname_item = QStandardItem(str(student.last_name))
        lname_item.setTextAlignment(Qt.AlignCenter)
        class_item = QStandardItem(str(student.class_id))
        class_item.setTextAlignment(Qt.AlignCenter)
        cls.__student_model.appendRow([id_item, fname_item, lname_item, class_item])
    
    @classmethod
    def update_row(cls, student: Student, row: int=None) -> None:
        """Aktualizuje radek se studentem.

        Args:
            student (Student): Instance studenta.
            row (int): Radek se studentem.
        """
        if cls.__student_model is None:
            return
        if not row:
            row = cls.__get_row(student.id)
            if row is None:
                return
        fname_item = cls.__student_model.index(row, 1, QModelIndex())
        cls.__student_model.setData(fname_item, student.first_name)
        lname_item = cls.__student_model.index(row, 2, QModelIndex())
        cls.__student_model.setData(lname_item, student.last_name)
        class_item = cls.__student_model.index(row, 3, QModelIndex())
        cls.__student_model.setData(class_item, student.class_id)
    

    @classmethod
    def __get_row(cls, student_id: str) -> int:
        """Vyhleda prislusny radek studenta v modelu.

        Args:
            student_id (str): Identifikacni hodnota studenta.

        Returns:
            int: Radek, na kterem se student nachazi.
        """
        for row in range(cls.__student_model.rowCount()):
            if cls.__student_model.data(cls.__student_model.index(row, 0, QModelIndex())) == student_id:
                return row
        else:
            return None
    

    @classmethod
    def delete_student_from_model(cls, student_id: str) -> None:
        """Smaze radek se studentem.

        Args:
            student_id (str): Identifikacni hodnota studenta.
        """
        if cls.__student_model is None:
            return
        row = cls.__get_row(student_id)
        if row is None:
            return
        cls.__student_model.removeRow(row)


    @classmethod
    def set_model(cls, model: 'sort_lib.sort.Sort'):
        """Nastavi novou hodnotu sort modelu.

        Args:
            model (sort_lib.sort.Sort): Nova instance sort modelu.
        """
        if cls.__sort_model is None:
            return
        cls.__student_model.removeRows(0, cls.__student_model.rowCount())
        cls.__sort_model = model
        for student in cls.__sort_model.students:
            cls.add_student_to_model(student)

    def __init__(self, base_gparent: 'gui_lib.g_main_window.GMainWindow'):
        super().__init__()
        self._base_gparent = base_gparent

        # klavesove zkratky pro undo/redo
        self.__redo_shortcut = QShortcut(QKeySequence('Ctrl+Y'), self)
        self.__redo_shortcut.activated.connect(base_gparent.command_builder.redo_slot)
        self.__undo_shortcut = QShortcut(QKeySequence('Ctrl+Z'), self)
        self.__undo_shortcut.activated.connect(base_gparent.command_builder.undo_slot)

        if __class__.__student_model is None:
            __class__.__init_model(self._base_gparent.model)
        self._changed = []
        self._setupUI()
        self.setWindowTitle('Správce studentů')

    
    def _setupUI(self):
        """Vygeneruje obsah GStudentControlDialog."""
        self.setLayout(QGridLayout())
        self.table_view = QTableView()
        self.table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.horizontalHeader().setHighlightSections(False)
        self.table_view.verticalHeader().setVisible(False)
        self.table_view.setFocusPolicy(Qt.NoFocus)
        self.table_view.setSortingEnabled(True)

        # tridici model
        pm = ProxyModel()
        pm.setSourceModel(__class__.__student_model)
        self.table_view.setModel(pm)
        pm.sort(0)
        self.layout().addWidget(self.table_view, 0, 0, 5, 1)

        # tlacitka na prave strane
        add_button = QPushButton('Přidat')
        add_button.clicked.connect(self.add_student)
        self.layout().addWidget(add_button, 0, 1)
        
        edit_button = QPushButton('Upravit')
        edit_button.clicked.connect(self.edit_student)
        self.layout().addWidget(edit_button, 1, 1)

        delete_button = QPushButton('Smazat')
        delete_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        delete_button.clicked.connect(self.delete_student)
        self.layout().addWidget(delete_button, 3, 1, 2, 1)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        self.layout().addWidget(button_box, 5, 1)
    

    def accept(self) -> None:
        self.__redo_shortcut.activated.disconnect(self._base_gparent.command_builder.redo_slot)
        self.__undo_shortcut.activated.disconnect(self._base_gparent.command_builder.undo_slot)
        super().accept()


    @Slot()
    def add_student(self):
        """Akce pro pridani studenta."""
        student = Student('', '', '', (None, None, None), self._base_gparent.model)
        if __class__.GStudentControlEditDialog(student, self._base_gparent, True).exec():
            # vlozi akci do command builderu pro moznost undo/redo
            self._base_gparent.command_builder.execute(StudentControlAdd(student, self._base_gparent))
        else:
            sort_lib.sort.Sort.student_id_counter -= 1

    @Slot()
    def edit_student(self):
        """Uprava dat oznaceneho studenta."""
        # vyhleda oznaceny radek
        index = list(set([model.row() for model in self.table_view.selectionModel().selectedIndexes()]))
        if index:
            # vyhleda id studenta na danem radku
            id_value = self.table_view.model().data(
                            self.table_view.model().index(index[0], 0, QModelIndex()))
            student = self._base_gparent.model.get_student(str(id_value))
            __class__.GStudentControlEditDialog(student, self._base_gparent).exec()


    @Slot()
    def delete_student(self):
        """Smazani studenta z modelu."""
        # vyhleda oznaceny radek
        index = list(set([model.row() for model in self.table_view.selectionModel().selectedIndexes()]))
        if index:
            # vyhleda id studenta na danem radku
            id_value = self.table_view.model().data(
                            self.table_view.model().index(index[0], 0, QModelIndex()))
            # vlozi akci do command builderu pro moznost undo/redo
            self._base_gparent.command_builder.execute(StudentControlDelete(self._base_gparent, id_value))
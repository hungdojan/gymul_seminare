from PySide6.QtWidgets import *
from PySide6.QtGui import QKeySequence, QPainter, QPaintEvent, QShortcut
from PySide6.QtCore import Slot, Signal, Qt, QFile, QIODevice

from gui_lib.g_student import GStudent
from gui_lib.g_day import GDay
from gui_lib.g_constants import StudentStatus
from gui_lib.g_about_dialog import GAboutDialog
from gui_lib.g_help_dialog import GHelpDialog
from gui_lib.g_subject_table_view import GSubjectTableView
from gui_lib.g_sort_button import GSortButton
from gui_lib.subject_model import SubjectModel

import rc
from sort_lib.day import Day
import sort_lib.sort
from sort_lib.student import Student

class GMainWindow(QMainWindow):
    """Trida reprezentujici hlavni okno programu."""

    # Signal se vysle, pokud je potreba aktualizovat zobrazeni dat
    view_updated = Signal()
    # Signal se vysle, pokud je potreba, aby se aktualizovaly deti tohoto okna
    data_updated = Signal()
    # Signal se vysle, pokud se zmeni seznam predmetu v modelu
    subject_list_updated = Signal(list)
    # Signal se vysle, pokud se ma smazat seznam predmetu
    subject_list_clear = Signal()
    # Signal se vysle, pokud se zmeni pocet studentu/student zmeni svuj vyber
    subject_counter_changed = Signal()


    def __init__(self, model: 'sort_lib.sort.Sort', parent: QWidget=None):
        super().__init__(parent)
        # hlavni sort model
        self._model = model
        # list g-dnu
        self.lof_gdays = []
        # list g-studentu
        self.lof_gstudents = []
        # model predmetu
        self._subject_model = SubjectModel(self._model)
        self.subject_list_updated.connect(self._subject_model.update_list)
        self.subject_list_clear.connect(self._subject_model.clear_model)

        self._setupUI()
        # seznam oznacenych g-studentu
        self.selected_gstudents = set()
        # seznam oznacenych g-dnu
        self.selected_gdays = set()

        self.view_updated.connect(self.view_update)
        self.load_stylesheet()


    @property
    def model(self) -> 'sort_lib.sort.Sort':
        return self._model
    

    @property
    def subject_model(self) -> SubjectModel:
        return self._subject_model


    def _setupUI(self) -> None:
        """Vygenerovani hlavniho okna."""
        self.setWindowTitle('Seminare')
        # nastaveni pracovni plochy
        main_widget = QWidget()
        self.main_grid_layout = QGridLayout()
        main_widget.setLayout(self.main_grid_layout)
        self.setCentralWidget(main_widget)

        self._setup_menu_bar()
        self._setup_subject_table_view()
        self._setup_student_panel()
        self._setup_day_panel()

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('Všechny operace dokončené', 6000)

        # klavesova zkratka pro roztrideni studentu
        sort_shortcut = QShortcut(QKeySequence('F5'), self)
        sort_shortcut.activated.connect(self.slt_sort)

        self.main_grid_layout.setRowStretch(0, 0)
        self.main_grid_layout.setRowStretch(1, 3)
        self.main_grid_layout.setRowStretch(2, 0)
        self.main_grid_layout.setRowStretch(3, 1)
        self.main_grid_layout.setColumnStretch(0, 2)
        self.main_grid_layout.setColumnStretch(1, 3)
        self.main_grid_layout.setColumnStretch(2, 3)
        self.main_grid_layout.setColumnStretch(3, 1)

        self.showMaximized()
    

    def _setup_menu_bar(self) -> None:
        """ Vygeneruje horni listu """
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        # tovarni funkce
        def add_action(name, actionslt, parent: QMenu, shortcut=None):
            """ Vytvari polozku v menu """
            if parent is None or actionslt is None:
                raise Exception("add_action failed")
            action = parent.addAction(name)
            action.triggered.connect(actionslt)
            if shortcut is not None:
                action.setShortcut(QKeySequence(shortcut))
                action.setShortcutVisibleInContextMenu(True)
            return action

        # soubor menu
        file_menu = self.menu_bar.addMenu("Soubor")
        add_action('Nový', self.slt_new_project, file_menu, 'Ctrl+N')
        add_action('Otevřít soubor', self.slt_open_file, file_menu, 'Ctrl+O')
        add_action('Uložit', self.slt_save, file_menu, 'Ctrl+S')
        file_menu.addSeparator()
        add_action('Načíst předměty', self.slt_import_subjects, file_menu)
        add_action('Načíst studenty', self.slt_import_students, file_menu)
        add_action('Exportovat data', self.slt_export, file_menu, 'Ctrl+E')

        file_menu.addSeparator()
        self.auto_refresh_action = file_menu.addAction('Auto-refresh')
        self.auto_refresh_action.setCheckable(True)
        file_menu.addSeparator()
        add_action('Zavřít', self.close, file_menu, 'Alt+F4')

        # student menu
        # TODO:
        # edit_menu = self.menu_bar.addMenu('Upravit')
        # add_action('Přidat studenta', self.slt_add_student, edit_menu)
        # add_action('Smazat studenta', self.slt_delete_student, edit_menu)
        # edit_menu.addSeparator()

        view_menu = self.menu_bar.addMenu('Zobrazit')
        todo = view_menu.addAction('TODO')
        # TODO:

        help_menu = self.menu_bar.addMenu('Nápověda')
        add_action('Nápověda', self.slt_help, help_menu, 'F1')
        add_action('O apllikaci', self.slt_about, help_menu)


    def _setup_student_panel(self) -> None:
        # skrolovaci plocha
        lof_students_scrar = QScrollArea(self)
        lof_students_scrar.setMinimumWidth(500)
        lof_students_scrar.setLineWidth(2)
        lof_students_scrar.setFrameShape(QFrame.Shape.Box)
        lof_students_scrar.setFrameShadow(QFrame.Shadow.Plain)

        # koren skrolovaci plochy
        self.student_frame = QFrame(lof_students_scrar)
        self.student_frame.setLayout(QVBoxLayout())
        # rozvrzeni skrolovaci plochy
        self.student_frame.layout().setContentsMargins(3, 3, 3, 3)
        self.student_frame.layout().setSpacing(3)
        self.student_frame.layout().addStretch()

        # self.student_frame.setLayout(self.student_vbox)
        lof_students_scrar.setWidgetResizable(True)
        lof_students_scrar.setWidget(self.student_frame)
        # vlozeni do hlavni plochy
        self.main_grid_layout.addWidget(lof_students_scrar, 1, 0, 3, 2)

        # hlavicka sekce
        self.main_grid_layout.addWidget(QLabel("Studenti"), 0, 0)

        # filtrovaci tlacitka
        self.buttons = {
            'red': QPushButton('ON', objectName='FailedButton'),
            'yellow': QPushButton('ON', objectName='MultipleButton'),
            'green': QPushButton('ON', objectName='SuccessButton'),
            'blue-ish': QPushButton('ON', objectName='ChosenButton')
        }
        student_filter_widget = QWidget()
        student_filter_widget.setLayout(QHBoxLayout())
        for btn in self.buttons:
            self.buttons[btn].setCheckable(True)
            self.buttons[btn].setChecked(True)
            self.buttons[btn].setAutoFillBackground(True)
            self.buttons[btn].toggled.connect(self.filter_students)
            student_filter_widget.layout().addWidget(self.buttons[btn])
        self.main_grid_layout.addWidget(student_filter_widget, 0, 1)

        # pridani studentu z modelu
        list(map(lambda x: self.create_gstudent(x), self._model.students))
    

    def _setup_day_panel(self) -> None:
        # hlavni plocha s moznosti skrolovat
        self.days_scrollarea = QScrollArea()
        self.days_scrollarea.setWidgetResizable(True)
        self.days_scrollarea.setWidget(QFrame())
        self.days_scrollarea.widget().setLayout(QVBoxLayout())
        self.days_scrollarea.widget().layout().addStretch()

        # nazev useku
        self.main_grid_layout.addWidget(QLabel('Dny'), 0, 2)

        # pracovni plocha pro operace se dny (pridani, mazani, filtrace)
        day_buttons_widget = QWidget()
        day_buttons_widget.setLayout(QHBoxLayout())
        add_btn = QPushButton('ADD')
        add_btn.clicked.connect(self.slt_add_day)
        self.filter_btn = QPushButton('FILTER')
        self.filter_btn.setCheckable(True)
        delete_btn = QPushButton('DELETE')
        delete_btn.clicked.connect(self.slt_delete_days)
        day_buttons_widget.layout().addWidget(add_btn)
        day_buttons_widget.layout().addWidget(self.filter_btn)
        day_buttons_widget.layout().addWidget(delete_btn)
        self.main_grid_layout.addWidget(day_buttons_widget, 0, 3)

        # pracovni plocha se dny
        self.day_widget = QWidget()
        self.day_widget.setLayout(QVBoxLayout())

        # pridani dnu z modelu
        list(map(lambda x: self.create_gday(x), self._model.days))

        self.main_grid_layout.addWidget(self.days_scrollarea, 1, 2, 1, 2)
    

    def _setup_subject_table_view(self) -> None:
        # Nazev useku
        self.main_grid_layout.addWidget(QLabel('Statistiky'), 2, 2, alignment=Qt.AlignmentFlag.AlignCenter)

        # tabulka s predmety
        self.table_view = GSubjectTableView(self)
        self.main_grid_layout.addWidget(self.table_view, 3, 2)

        # tlacitko na roztrideni dat
        self.sort_button = GSortButton('sort')
        self.sort_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.sort_button.clicked.connect(self.slt_sort)
        self._model.sort_toggle.connect(self.sort_button.sort_button_update)
        self.main_grid_layout.addWidget(self.sort_button, 3, 3)

    
    def load_stylesheet(self) -> None:
        """Nacte data z QCSS"""
        stylesheet = QFile(":/stylesheet.qss")
        stylesheet.open(QIODevice.OpenModeFlag.ReadOnly)
        style = str(stylesheet.readAll(), 'utf-8')
        self.setStyleSheet(style)
    

    def create_gstudent(self, student: Student) -> GStudent:
        gstudent = GStudent(student, self.student_frame.layout(), self)

        # pripojeni signalu a slotu
        gstudent.required_subjects_changed.connect(self.table_view.model().sourceModel().update_model_counter)
        self.data_updated.connect(gstudent.update_content)

        self.lof_gstudents.append(gstudent)
        return gstudent
    

    def create_gday(self, day: Day) -> GDay:
        gday = GDay(day, self.days_scrollarea.widget().layout(), self)

        self.filter_btn.toggled.connect(gday.filter_toggle)
        self.lof_gdays.append(gday)
        return gday


    def select_student(self, gstudent: 'GStudent', status: bool):
        """Spravuje oznacene GStudenty

        Args:
            gstudent (GStudent): Instance GStudent, ktereho se Všechny operace tyka
            status (bool): Pravdivostni hodnota, zda byl objekt oznacen ci ne
        """
        if status:
            self.selected_gstudents.add(gstudent)
        else:
            self.selected_gstudents.discard(gstudent)
    

    def select_day(self, gday: 'GDay', status: bool):
        """Spravuje oznacene GDny

        Args:
            gstudent (GStudent): Instance GDay, ktereho se Všechny operace tyka
            status (bool): Pravdivostni hodnota, zda byl objekt oznacen ci ne
        """
        if status:
            self.selected_gdays.add(gday)
        else:
            self.selected_gdays.discard(gday)


    def paintEvent(self, event: QPaintEvent) -> None:
        """Predefinuje funkci paintEvent

        Args:
            event (QPaintEvent): Promenna udalosti QPaintEvent
        """
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, p, self)
        super().paintEvent(event)


    def init_new_project(self, model: sort_lib.sort.Sort):
        # odpojeni starych widgetu
        self.selected_gdays = set(self.lof_gdays)
        self.selected_gstudents = set(self.lof_gstudents)
        # smazani widgetu
        self.slt_delete_days()
        self.slt_delete_student()

        self.subject_list_clear.emit()
        del self._model
        self._model = model
        
        # aktualizace zavislosti na novy sort model
        self.table_view.model().sourceModel().base_model = self._model
        self._subject_model.base_model = self._model
        self._model.sort_toggle.connect(self.sort_button.sort_button_update)

    
    # slots  
    @Slot()
    def slt_new_project(self):
        self.init_new_project(sort_lib.sort.Sort())


    @Slot()
    def slt_delete_student(self) -> None:
        """Funkce maze oznacene studenty"""
        self.status_bar.showMessage('Mažu studenty')
        list(map(lambda x: x.delete_gstudent(), self.selected_gstudents))
        self.status_bar.showMessage('Všechny operace dokončené', 6000)


    @Slot()
    def slt_open_file(self) -> None:
        self.status_bar.showMessage('Otevírám soubor s uloženou prací')
        # nacteni souboru
        filename = QFileDialog.getOpenFileName(self, "Otevřít soubor", "", "JSON soubor (*.json)")
        if not filename[0]:
            self.status_bar.showMessage('Úloha byla předčasně ukončena', 5000)
            return
        try:
            model = sort_lib.sort.Sort.load_save_file(filename[0])
        except sort_lib.sort.Sort.JsonFileCorruptedException:
            # chybova hlaska pro nesetrizena data
            self.status_bar.showMessage('Nastala chyba při otevírání souboru', 5000)
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Critical)
            # FIXME: update warning text
            msg_box.setWindowTitle('Špatná data v souboru')
            msg_box.setText('Nelze otevřít soubor\nSoubor je buďto poškozený, nebo nesplňuje formát.')
            msg_box.exec()
            return

        # TODO: TEST IT
        self.init_new_project(model)
        
        # pridani dat
        self._model = model
        list(map(lambda x: self.create_gstudent(x), self._model.students))
        list(map(lambda x: self.create_gday(x), self._model.days))

        self.view_updated.emit()
        self.subject_list_updated.emit(self._model.subjects.keys())
        # TODO: self.subject_counter_changed.emit()
        self.sort_button.sort_button_update(True)
        # TODO: subjects
        
        self.status_bar.showMessage('Všechny operace dokončené', 6000)


    @Slot()
    def slt_save(self) -> None:
        self.status_bar.showMessage('Ukládám práci do souboru')
        filename = QFileDialog.getSaveFileName(self, 'Uložit', "Bez názvu", "JSON soubor (*.json)", )

        # otevreni okna pro vyber souboru
        if not filename[0]:
            self.status_bar.showMessage('Úloha byla předčasně ukončena', 5000)
            return
        try:
            content = self._model.save_to_json()
            with open(filename[0], 'w') as f:
                f.write(content)
        except sort_lib.sort.Sort.DataNotSortedException:
            # chybova hlaska pro nesetrizena data
            self.status_bar.showMessage('Nastala chyba při exportu', 5000)
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Critical)
            # FIXME: update warning text
            msg_box.setWindowTitle('Nesetřízená data')
            msg_box.setText('Nelze uložit práci\nPřed uložení je potřeba data setřídit')
            msg_box.exec()
        self.status_bar.showMessage('Všechny operace dokončené', 6000)


    @Slot()
    def slt_import_subjects(self) -> None:
        """Slot pro nacteni souboru s predmety"""
        dialog = QFileDialog(self)
        dialog.setWindowTitle('Importovat předměty')
        dialog.setNameFilter('CSV soubor (*.csv)')
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)

        # otevreni okna pro vyber souboru
        self.status_bar.showMessage('Načítám soubor s předměty')
        if not dialog.exec():
            self.status_bar.showMessage('Úloha byla předčasně ukončena', 5000)
            return
        filename = dialog.selectedFiles()[0]
        try:
            new_subj = self.model.load_file_subjects(filename)
            self.subject_list_updated.emit(new_subj)
        except sort_lib.sort.Sort.FileContentFormatException:
            # chybova hlaska programu
            self.status_bar.showMessage('Nastala chyba při načítání', 5000)
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowTitle('Chyba při načítání předmětů')
            msg_box.setText('Vybraný soubor nesplňuje formát pro načtění předmětů')
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()
        self.status_bar.showMessage('Všechny operace dokončené', 6000)


    @Slot()
    def slt_export(self) -> None:
        """Slot pro vytvoreni vyslednych souboru"""
        dialog = QFileDialog(self)
        dialog.setWindowTitle('Exportovat data')
        dialog.setFileMode(QFileDialog.FileMode.Directory)

        # otevreni okna pro vyber slozky
        self.status_bar.showMessage('Exportuju data')
        if not dialog.exec():
            self.status_bar.showMessage('Úloha byla předčasně ukončena', 5000)
            return
        dirname = dialog.selectedFiles()[0]
        try:
            self.model.export_data(dirname)
        except sort_lib.sort.Sort.DataNotSortedException:
            # chybova hlaska pro nesetrizena data
            self.status_bar.showMessage('Nastala chyba při exportu', 5000)
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Critical)
            # FIXME: update warning text
            msg_box.setWindowTitle('Nesetřízená data')
            msg_box.setText('Nelze exportovat zastaralá data\nPřed exportem je potřeba data setřídit')
            msg_box.exec()
        self.status_bar.showMessage('Všechny operace dokončené', 6000)
    

    @Slot()
    def slt_import_students(self) -> None:
        """Slot pro nacteni souboru se studenty"""
        dialog = QFileDialog(self)
        dialog.setWindowTitle('Importovat studenty')
        dialog.setNameFilter('CSV soubor (*.csv)')
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)

        # TODO: SUBJECT CHECK
        # otevreni okna pro vyber souboru
        self.status_bar.showMessage('Načítám soubor se studenty')
        if not dialog.exec():
            self.status_bar.showMessage('Úloha byla předčasně ukončena', 5000)
            return
        filename = dialog.selectedFiles()[0]
        try:
            new_ids = self.model.load_file_students(filename)
            new_students = [student for student in self.model.students if student.id in new_ids]
            list(map(lambda x: self.create_gstudent(x), new_students))
        except sort_lib.sort.Sort.FileContentFormatException:
            # chybova hlaska programu
            self.status_bar.showMessage('Nastala chyba při načítání', 5000)
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setText('Chyba při načítání studentů\nVybraný soubor nesplňuje formát pro načtění studentů')
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()
        self.status_bar.showMessage('Všechny operace dokončené', 6000)
        self.subject_counter_changed.emit()


    @Slot()
    def slt_close_app(self) -> None:
        """Funkce ukoncuje program"""
        # TODO: ask to save progress
        self.status_bar.showMessage('Zavírám aplikaci')
        self.close()
    

    @Slot()
    def slt_add_student(self) -> None:
        # TODO:
        self.status_bar.showMessage('Přidávám nového studenta')
        print('add student')
        self.status_bar.showMessage('Všechny operace dokončené', 6000)

    
    @Slot()
    def slt_add_day(self) -> None:
        """Slot prida vygeneruje novy den"""
        self.status_bar.showMessage('Přidávám novýho den')
        new_day = self.model.add_day()
        self.create_gday(new_day)
        self.status_bar.showMessage('Všechny operace dokončené', 6000)
    

    @Slot()
    def slt_delete_days(self) -> None:
        """Slot smaze vybrane dny"""
        self.status_bar.showMessage('Mažu vybrané dny')
        list(map(lambda x: x.delete_gday(), self.selected_gdays))
        self.status_bar.showMessage('Všechny operace dokončené', 6000)

    
    @Slot()
    def slt_help(self) -> None:
        """Slot otevre okno s napovedou"""
        self.status_bar.showMessage('Otevírám okno s nápovědou')
        GHelpDialog(self)
        self.status_bar.showMessage('Všechny operace dokončené', 6000)

    @Slot()
    def slt_about(self) -> None:
        """Slot otevre okno s informacemi o aplikaci"""
        self.status_bar.showMessage('Otevírám okno s informacemi o aplikaci')
        GAboutDialog(self)
        self.status_bar.showMessage('Všechny operace dokončené', 6000)

    @Slot()
    def slt_sort(self) -> None:
        """Slot provede setrizeni dat"""
        self.status_bar.showMessage('Provádím třídění studentů')
        self.model.sort_data()
        for student in self.lof_gstudents:
            student.update_content()
        self.view_updated.emit()
        self.status_bar.showMessage('Všechny operace dokončené', 6000)
    

    @Slot()
    def view_update(self):
        self.data_updated.emit()
        self.filter_students()
    

    @Slot()
    def filter_students(self) -> None:
        """Slot provadi filtraci studentu podle jejich statusu"""
        self.status_bar.showMessage('Provádím filtraci studentů')
        # red
        red_students = [gstudent for gstudent in self.lof_gstudents
                        if gstudent.get_status() == StudentStatus.NO_COMB]
        list(map(lambda x: x.setVisible(self.buttons['red'].isChecked()), red_students))

        # yellow
        yellow_students = [gstudent for gstudent in self.lof_gstudents
                           if gstudent.get_status() == StudentStatus.MUL_COMB]
        list(map(lambda x: x.setVisible(self.buttons['yellow'].isChecked()), yellow_students))

        # blue-ish
        blueish_students = [gstudent for gstudent in self.lof_gstudents
                            if gstudent.get_status() == StudentStatus.MUL_SET]
        list(map(lambda x: x.setVisible(self.buttons['blue-ish'].isChecked()), blueish_students))

        # green
        green_students = [gstudent for gstudent in self.lof_gstudents
                          if gstudent.get_status() == StudentStatus.ONLY_ONE]
        list(map(lambda x: x.setVisible(self.buttons['green'].isChecked()), green_students))

        for btn in self.buttons:
            self.buttons[btn].setText('ON' if self.buttons[btn].isChecked() else 'OFF')
        self.status_bar.showMessage('Všechny operace dokončené', 6000)

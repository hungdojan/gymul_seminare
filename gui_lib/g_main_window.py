from PySide6.QtWidgets import *
from PySide6.QtGui import QKeySequence, QPainter, QPaintEvent, QShortcut, QCloseEvent
from PySide6.QtCore import Slot, Signal, Qt, QFile, QIODevice
from gui_lib.commands.g_main_window_actions import MainWindowImportStudents, MainWindowImportSubjects
from gui_lib.g_day_panel import GDayPanel
from gui_lib.commands.day_panel_actions import DayPanelAddDay

from gui_lib.g_student_panel import GStudentPanel
from gui_lib.g_about_dialog import GAboutDialog
from gui_lib.g_help_dialog import GHelpDialog
from gui_lib.g_subject_table_view import GSubjectTableView
from gui_lib.g_sort_button import GSortButton
from gui_lib.subject_model import SubjectModel
from gui_lib.g_subject_control_dialog import GSubjectControlDialog
from gui_lib.g_student_control_dialog import GStudentControlDialog
from gui_lib.g_savedialog import GSaveDialog

import gui_lib.rc   # generated resource file
import sort_lib.sort
from sort_lib.command import CommandBuilder

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
        # model predmetu
        self._subject_model = SubjectModel(self._model)
        self.subject_list_updated.connect(self._subject_model.update_list)
        self.subject_list_clear.connect(self._subject_model.clear_model)
        self._command_builder = CommandBuilder()

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
    

    @property
    def command_builder(self) -> CommandBuilder:
        return self._command_builder


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
        # klavesove zkratky pro undo/redo akce
        self.redo_shortcut = QShortcut(QKeySequence('Ctrl+Y'), self)
        self.redo_shortcut.activated.connect(self._command_builder.redo_slot)
        self.undo_shortcut = QShortcut(QKeySequence('Ctrl+Z'), self)
        self.undo_shortcut.activated.connect(self._command_builder.undo_slot)

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
        add_action('Uložit jako', self.slt_save_as, file_menu, 'Ctrl+Shift+S')
        file_menu.addSeparator()
        add_action('Načíst předměty', self.slt_import_subjects, file_menu)
        add_action('Načíst studenty', self.slt_import_students, file_menu)
        add_action('Exportovat data', self.slt_export, file_menu, 'Ctrl+E')
        file_menu.addSeparator()
        self.auto_refresh_action = file_menu.addAction('Auto-refresh')
        self.auto_refresh_action.setCheckable(True)
        file_menu.addSeparator()
        add_action('Zavřít', self.close, file_menu, 'Alt+F4')

        # spravovat menu
        control_menu = self.menu_bar.addMenu('Spravovat')
        add_action('Spravovat studenty', self.slt_open_student_control, control_menu)
        add_action('Spravovat předměty', self.slt_open_subject_control, control_menu)

        # napoveda menu
        help_menu = self.menu_bar.addMenu('Nápověda')
        add_action('Nápověda', self.slt_help, help_menu, 'F1')
        add_action('O apllikaci', self.slt_about, help_menu)


    def _setup_student_panel(self) -> None:

        self.student_panel = GStudentPanel(self)
        self.main_grid_layout.addWidget(self.student_panel, 1, 0, 3, 2)

        # hlavicka sekce
        self.main_grid_layout.addWidget(QLabel("Studenti"), 0, 0)

        # filtrovaci tlacitka
        self.student_buttons = {
            'red': QPushButton('ON', objectName='FailedButton'),
            'yellow': QPushButton('ON', objectName='MultipleButton'),
            'green': QPushButton('ON', objectName='SuccessButton'),
            'blue-ish': QPushButton('ON', objectName='ChosenButton')
        }
        student_filter_widget = QWidget()
        student_filter_widget.setLayout(QHBoxLayout())
        for btn in self.student_buttons:
            self.student_buttons[btn].setCheckable(True)
            self.student_buttons[btn].setChecked(True)
            self.student_buttons[btn].toggled.connect(self.student_panel.filter_students)
            student_filter_widget.layout().addWidget(self.student_buttons[btn])
        self.main_grid_layout.addWidget(student_filter_widget, 0, 1)

        # pridani studentu z modelu
        list(map(lambda x: self.student_panel.add_gstudent(x), self._model.students))
    

    def _setup_day_panel(self) -> None:
        # hlavni plocha s moznosti skrolovat
        self.day_panel = GDayPanel(self)

        # nazev useku
        self.main_grid_layout.addWidget(QLabel('Dny'), 0, 2)

        # pracovni plocha pro operace se dny (pridani, mazani, filtrace)
        day_buttons_widget = QWidget()
        day_buttons_widget.setLayout(QHBoxLayout())
        self.day_buttons = {
            'add': QPushButton('Přidat'),
            'filter': QPushButton('Filtr'),
            'delete': QPushButton('Odebrat')
        }
        self.day_buttons['add'].clicked.connect(self.slt_add_day)
        self.day_buttons['filter'].setCheckable(True)
        self.day_buttons['delete'].clicked.connect(self.day_panel.delete_selected)

        day_buttons_widget.layout().addWidget(self.day_buttons['add'])
        day_buttons_widget.layout().addWidget(self.day_buttons['filter'])
        day_buttons_widget.layout().addWidget(self.day_buttons['delete'])
        self.main_grid_layout.addWidget(day_buttons_widget, 0, 3)

        # pridani dnu z modelu
        list(map(lambda x: self.day_panel.add_gday(x), self._model.days))

        self.main_grid_layout.addWidget(self.day_panel, 1, 2, 1, 2)
    

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
        # odpojeni a smazani starych widgetu
        self.student_panel.clear()
        self.day_panel.clear()
        self._command_builder.clear()

        self.subject_list_clear.emit()
        del self._model

        # inicializace noveho modelu
        self._model = model
        sort_lib.sort.Sort.student_id_counter = 1
        
        # aktualizace zavislosti na novy sort model
        self.table_view.model().sourceModel().base_model = self._model
        self._subject_model.base_model = self._model
        self._model.sort_toggle.connect(self.sort_button.sort_button_update)
        GStudentControlDialog.set_model(model)

    
    # slots  
    @Slot()
    def slt_new_project(self):
        save_dialog = GSaveDialog(self, 'Uložit', 'Chcete uložit práci?')
        save_dialog.exec()
        reply = save_dialog.buttonRole(save_dialog.clickedButton())
        if reply == QMessageBox.AcceptRole:
            if not self.slt_save():
                return
        elif reply == QMessageBox.RejectRole:
            return
        self.init_new_project(sort_lib.sort.Sort())


    @Slot()
    def slt_open_file(self) -> None:
        save_dialog = GSaveDialog(self, 'Uložit', 'Chcete uložit práci?')
        save_dialog.exec()
        reply = save_dialog.buttonRole(save_dialog.clickedButton())
        if reply == QMessageBox.AcceptRole:
            if not self.slt_save():
                return
        elif reply == QMessageBox.RejectRole:
            return

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

        self.init_new_project(model)
        
        # pridani dat
        self._model = model
        list(map(lambda x: self.student_panel.add_gstudent(x), self._model.students))
        list(map(lambda x: self.day_panel.add_gday(x), self._model.days))

        self.view_updated.emit()
        self.subject_list_updated.emit(self._model.subjects.keys())
        # TODO: self.subject_counter_changed.emit()
        self.sort_button.sort_button_update(self._model.is_sorted)
        
        self.status_bar.showMessage('Všechny operace dokončené', 6000)


    @Slot()
    def slt_save(self) -> bool:
        if self._model.file_path is None:
            return self.slt_save_as()

        self.status_bar.showMessage('Ukládám práci do souboru')
        self._model.save_to_json()
        self.status_bar.showMessage('Všechny operace dokončené', 6000)
        return True
    

    @Slot()
    def slt_save_as(self) -> bool:
        self.status_bar.showMessage('Ukládám práci do souboru')
        filename = QFileDialog.getSaveFileName(self, 'Uložit jako...', "Bez názvu", "JSON soubor (*.json)", )

        # otevreni okna pro vyber souboru
        if not filename[0]:
            self.status_bar.showMessage('Úloha byla předčasně ukončena', 5000)
            return False
        fname = filename[0] if filename[0].endswith('.json') \
                            else f'{filename[0]}.json'

        self._model.save_to_json(fname)
        self.status_bar.showMessage('Všechny operace dokončené', 6000)
        return True


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
            self.command_builder.execute(MainWindowImportSubjects(self, filename))
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

        # otevreni okna pro vyber souboru
        self.status_bar.showMessage('Načítám soubor se studenty')
        if not dialog.exec():
            self.status_bar.showMessage('Úloha byla předčasně ukončena', 5000)
            return
        filename = dialog.selectedFiles()[0]
        try:
            self.command_builder.execute(MainWindowImportStudents(self, filename))
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
    def slt_add_day(self) -> None:
        """Slot prida vygeneruje novy den"""
        self.status_bar.showMessage('Přidávám novýho den')
        self.command_builder.execute(DayPanelAddDay(self))
        self.status_bar.showMessage('Všechny operace dokončené', 6000)
    

    @Slot()
    def slt_open_student_control(self):
        self.status_bar.showMessage('Otevírám okno s správou předmětů.')
        GStudentControlDialog(self).exec()
        self.status_bar.showMessage('Všechny operace dokončené', 6000)


    @Slot()
    def slt_open_subject_control(self):
        self.status_bar.showMessage('Otevírám okno s správou předmětů.')
        if GSubjectControlDialog(self).exec():
            self.view_updated.emit()
        self.status_bar.showMessage('Všechny operace dokončené', 6000)
    

    @Slot()
    def slt_help(self) -> None:
        """Slot otevre okno s napovedou"""
        self.status_bar.showMessage('Otevírám okno s nápovědou')
        GHelpDialog(self).show()
        self.status_bar.showMessage('Všechny operace dokončené', 6000)


    @Slot()
    def slt_about(self) -> None:
        """Slot otevre okno s informacemi o aplikaci"""
        self.status_bar.showMessage('Otevírám okno s informacemi o aplikaci')
        GAboutDialog(self).show()
        self.status_bar.showMessage('Všechny operace dokončené', 6000)


    @Slot()
    def slt_sort(self) -> None:
        """Slot provede setrizeni dat"""
        self.status_bar.showMessage('Provádím třídění studentů')
        self.model.sort_data()
        self.view_updated.emit()
        self.status_bar.showMessage('Všechny operace dokončené', 6000)
    

    @Slot()
    def view_update(self):
        self.data_updated.emit()
        self.student_panel.filter_students()
    

    def closeEvent(self, event: QCloseEvent) -> None:
        save_dialog = GSaveDialog(self, 'Uložit', 'Chcete uložit práci?')
        save_dialog.exec()
        reply = save_dialog.buttonRole(save_dialog.clickedButton())
        if reply == QMessageBox.AcceptRole:
            if not self.slt_save():
                event.ignore()
                return
        elif reply == QMessageBox.RejectRole:
            event.ignore()
            return
        super().closeEvent(event)
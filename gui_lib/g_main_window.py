from PySide6.QtWidgets import *
from PySide6.QtGui import QKeySequence, QPainter, QPaintEvent
from PySide6.QtCore import Slot, Signal, Qt, QFile, QIODevice
import sort_lib.sort
from gui_lib.g_student import GStudent
from gui_lib.g_day import GDay
from gui_lib.g_constants import StudentStatus
from gui_lib.g_about_dialog import GAboutDialog
from gui_lib.g_help_dialog import GHelpDialog
import rc

class GMainWindow(QMainWindow):

    content_refreshed = Signal()
    subject_list_update = Signal(list)


    def __init__(self, model: 'sort_lib.sort.Sort', parent: QWidget=None):
        super().__init__(parent)
        self._model = model

        # FIXME: TESTING PURPOSES
        self.model.load_file_subjects('./data/input_predmety.csv')
        self.model.load_file_students('./data/input_zaci-2R-anonym.csv')
        den1 = self.model.add_day()
        list(map(lambda x: den1.add_subject_name(x), ['Aj-FCE', 'Bi', 'Pr']))
        den2 = self.model.add_day()
        list(map(lambda x: den2.add_subject_name(x), ['Aj-FCE', 'Nj-DSD2', 'ZSV', 'Fy', 'Nj-DSD1']))
        den3 = self.model.add_day()
        list(map(lambda x: den3.add_subject_name(x), ['Aj-FCE', 'Aj-Konv', 'M-MZ', 'M-VS', 'ZSV']))
        den4 = self.model.add_day()
        list(map(lambda x: den4.add_subject_name(x), ['Ch', 'D', 'VV', 'Z']))
        # END TESTING

        self.setupUI()
        self.selected_gstudents = set()
        self.selected_gdays = set()

        self.lof_gdays = []
        self.content_refreshed.connect(self.filter_students) 
        self.load_stylesheet()

    @property
    def model(self):
        return self._model


    def setupUI(self):
        self.setWindowTitle('Seminare')
        # nastaveni pracovni plochy
        main_widget = QWidget()
        self.main_grid_layout = QGridLayout()
        main_widget.setLayout(self.main_grid_layout)
        self.setCentralWidget(main_widget)

        self._setup_menu_bar()
        self._setup_student_panel()
        self._setup_day_panel()
        self._setup_right_panel()

        self.main_grid_layout.setRowStretch(0, 0)
        self.main_grid_layout.setRowStretch(1, 3)
        self.main_grid_layout.setRowStretch(2, 0)
        self.main_grid_layout.setRowStretch(3, 1)
        self.main_grid_layout.setColumnStretch(0, 2)
        self.main_grid_layout.setColumnStretch(1, 3)
        self.main_grid_layout.setColumnStretch(2, 3)
        self.main_grid_layout.setColumnStretch(3, 1)

        self.showMaximized()
    

    def _setup_menu_bar(self):
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
        edit_menu = self.menu_bar.addMenu('Upravit')
        add_action('Přidat studenta', self.slt_add_student, edit_menu)
        add_action('Smazat studenta', self.slt_delete_student, edit_menu)
        # edit_menu.addSeparator()

        view_menu = self.menu_bar.addMenu('Zobrazit')
        todo = view_menu.addAction('TODO')
        # TODO:

        help_menu = self.menu_bar.addMenu('Nápověda')
        add_action('Nápověda', self.slt_help, help_menu, 'F1')
        add_action('O apllikaci', self.slt_about, help_menu)


    def _setup_student_panel(self):
        # skrolovaci plocha
        lof_students_scrar = QScrollArea(self)
        lof_students_scrar.setMinimumWidth(500)
        lof_students_scrar.setLineWidth(2)
        lof_students_scrar.setFrameShape(QFrame.Shape.Box)
        lof_students_scrar.setFrameShadow(QFrame.Shadow.Plain)

        # koren skrolovaci plochy
        frame = QFrame(lof_students_scrar)
        # rozvrzeni skrolovaci plochy
        self.student_vbox = QVBoxLayout(frame)
        self.student_vbox.setContentsMargins(3, 3, 3, 3)
        self.student_vbox.setSpacing(3)
        self.student_vbox.addStretch()

        frame.setLayout(self.student_vbox)
        lof_students_scrar.setWidgetResizable(True)
        lof_students_scrar.setWidget(frame)
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
        w = QWidget()
        w.setLayout(QHBoxLayout())
        for btn in self.buttons:
            self.buttons[btn].setCheckable(True)
            self.buttons[btn].setChecked(True)
            self.buttons[btn].setAutoFillBackground(True)
            self.buttons[btn].toggled.connect(self.filter_students)
            w.layout().addWidget(self.buttons[btn])
        self.main_grid_layout.addWidget(w, 0, 1)

        # zobrazeni dat
        self.lof_gstudents = [GStudent(student, self.student_vbox, self) 
                              for student in self.model.students]
    

    def _setup_day_panel(self):
        self.days_scrollarea = QScrollArea()
        self.days_scrollarea.setWidgetResizable(True)
        self.days_scrollarea.setWidget(QFrame())
        self.days_scrollarea.widget().setLayout(QVBoxLayout())
        self.days_scrollarea.widget().layout().addStretch()

        # FIXME: refactor
        self.main_grid_layout.addWidget(QLabel('Dny'), 0, 2)
        w = QWidget()
        w.setLayout(QHBoxLayout())
        add_btn = QPushButton('ADD')
        add_btn.clicked.connect(self.slt_add_day)
        self.filter_btn = QPushButton('FILTER')
        self.filter_btn.setCheckable(True)
        delete_btn = QPushButton('DELETE')
        delete_btn.clicked.connect(lambda: print('delete'))
        w.layout().addWidget(add_btn)
        w.layout().addWidget(self.filter_btn)
        w.layout().addWidget(delete_btn)
        self.main_grid_layout.addWidget(w, 0, 3)

        self.day_widget = QWidget()
        self.day_widget.setLayout(QVBoxLayout())
        self.main_grid_layout.addWidget(self.days_scrollarea, 1, 2, 1, 2)
        pass
    

    def _setup_right_panel(self):
        scroll = QScrollArea()
        scroll.setMinimumWidth(200)
        scroll.setWidgetResizable(True)
        frame = QFrame()
        # frame.mousePressEvent = lambda _: print('clicked')
        scroll.setWidget(frame)
        frame.setLayout(QVBoxLayout())
        # w = QWidget()
        # w.setLayout(QVBoxLayout())
        stats = self.model.get_students_per_subject()
        # FIXME: refactor 
        for stat in dict(sorted(stats.items(), key=lambda x: x[1], reverse=True)):
            w_stat = QWidget()
            w_stat.setLayout(QHBoxLayout())
            w_stat.layout().setContentsMargins(0, 4, 5, 1)
            w_stat.layout().setSpacing(5)

            w_stat.font()
            font = w_stat.font()
            font.setPointSize(15)
            w_stat.setFont(font)

            w_stat.layout().addWidget(QLabel(stat), alignment=Qt.AlignmentFlag.AlignCenter)
            w_stat.layout().addWidget(QLabel(f'{stats[stat]}'), alignment=Qt.AlignmentFlag.AlignCenter)
            frame.layout().addWidget(w_stat)
        frame.layout().setSpacing(1)
        frame.layout().setContentsMargins(0, 0, 0, 0)

        self.main_grid_layout.addWidget(QLabel('Statistiky'), 2, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_grid_layout.addWidget(scroll, 3, 2)
        btn = QPushButton('sort')
        btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        btn.clicked.connect(self.slt_sort)
        self.main_grid_layout.addWidget(btn, 3, 3)

    
    def load_stylesheet(self):
        """Nacte data z QCSS"""
        stylesheet = QFile(":/stylesheet.qss")
        stylesheet.open(QIODevice.OpenModeFlag.ReadOnly)
        style = str(stylesheet.readAll(), 'utf-8')
        self.setStyleSheet(style)


    def select_student(self, gstudent: 'GStudent', status: bool):
        """Spravuje oznacene GStudenty

        Args:
            gstudent (GStudent): Instance GStudent, ktereho se operace tyka
            status (bool): Pravdivostni hodnota, zda byl objekt oznacen ci ne
        """
        if status:
            self.selected_gstudents.add(gstudent)
        else:
            self.selected_gstudents.discard(gstudent)
    

    def select_day(self, gday: 'GDay', status: bool):
        """Spravuje oznacene GDny

        Args:
            gstudent (GStudent): Instance GDay, ktereho se operace tyka
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

    
    # slots  
    @Slot()
    def slt_delete_student(self):
        # TODO:
        print('delete student')
        list(map(lambda x: x.delete_gstudent(), self.selected_gstudents))
        # for gs in self.selected_gstudents:
        #     gs.remove_widget()
        #     self.model.remove_student(gs.model)

    @Slot()
    def slt_open_file(self):
        # TODO:
        print("open file")


    @Slot()
    def slt_save(self):
        # TODO:
        print('save')


    @Slot()
    def slt_import_subjects(self):
        # TODO:
        dialog = QFileDialog(self)
        dialog.setWindowTitle('Importovat předměty')
        dialog.setNameFilter('CSV soubor (*.csv)')
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)

        if not dialog.exec():
            return
        filename = dialog.selectedFiles()[0]
        try:
            new_subj = self.model.load_file_subjects(filename)
            self.subject_list_update.emit(new_subj)
            # TODO: ADD SUBJECT
        except sort_lib.sort.Sort.FileContentFormatException:
            # TODO: WRONG FORMAT DIALOG
            pass
        print('import subjects')


    @Slot()
    def slt_export(self):
        # TODO:
        if not self.model.is_sorted:
            # TODO: WARNING DIALOG
            pass
        dialog = QFileDialog(self)
        dialog.setWindowTitle('Exportovat data')
        dialog.setFileMode(QFileDialog.FileMode.Directory)

        if not dialog.exec():
            return
        dirname = dialog.selectedFiles()[0]
        try:
            new_students = self.model.export_data(dirname)
            # TODO: ADD STUDENT
        except sort_lib.sort.Sort.FileContentFormatException:
            # TODO: WRONG FORMAT DIALOG
            pass
        # self.model.sort_data()
        # # FIXME: remove hardcoded code
        # self.model.export_data(r'C:\Users\hungd\Documents\GitHub\gymul_seminare\data')
        print('export data')
    

    @Slot()
    def slt_import_students(self):
        dialog = QFileDialog(self)
        dialog.setWindowTitle('Importovat studenty')
        dialog.setNameFilter('CSV soubor (*.csv)')
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)

        # TODO: SUBJECT CHECK

        if not dialog.exec():
            return
        filename = dialog.selectedFiles()[0]
        try:
            new_ids = self.model.load_file_students(filename)
            new_students = list(filter(lambda x: x.id in new_ids, self.model.students))
            list(map(lambda x: self.lof_gstudents.append(GStudent(x, self.student_vbox, self)), new_students))
            # TODO: ADD STUDENT
        except sort_lib.sort.Sort.FileContentFormatException:
            # TODO: WRONG FORMAT DIALOG
            pass
        print('import students')


    @Slot()
    def slt_close_app(self):
        self.close()
    

    @Slot()
    def slt_add_student(self):
        # TODO:
        print('add student')

    
    @Slot()
    def slt_add_day(self):
        new_day = self.model.add_day()
        gday = GDay(new_day, self.days_scrollarea.widget().layout(), self)

        self.filter_btn.toggled.connect(gday.filter_toggle)
        self.lof_gdays.append(gday)
        print('add day')
    

    @Slot()
    def slt_remove_days(self):
        # TODO:
        # for gd in self.selected_gdays:
        #     student = gd.model
        #     gd.delete()
        #     self.subsort.delete_student(student)
        print('remove days')

    
    @Slot()
    def slt_help(self):
        help_dialog = GHelpDialog()
        help_dialog.show()
        help_dialog.exec()
        # TODO:
        print('help')

    @Slot()
    def slt_about(self):
        about_dialog = GAboutDialog()
        about_dialog.show()
        about_dialog.exec()
        # TODO:
        print('about')
    

    @Slot()
    def slt_sort(self):
        self.model.sort_data()
        # temp = list(filter(lambda x: len(x.possible_comb) > 1, self.model.students))
        # TODO: try-except
        # list(map(lambda x: x.set_comb(0), temp))
        self.content_refreshed.emit()
        print('sort')
    

    @Slot()
    def filter_students(self):
        # red
        red_students = list(filter(lambda x: x.get_status() == StudentStatus.NO_COMB, self.lof_gstudents))
        list(map(lambda x: x.setVisible(self.buttons['red'].isChecked()), red_students))

        # yellow
        yellow_students = list(filter(lambda x: x.get_status() == StudentStatus.MUL_COMB, self.lof_gstudents))
        list(map(lambda x: x.setVisible(self.buttons['yellow'].isChecked()), yellow_students))

        # blue-ish
        blueish_students = list(filter(lambda x: x.get_status() == StudentStatus.MUL_SET, self.lof_gstudents))
        list(map(lambda x: x.setVisible(self.buttons['blue-ish'].isChecked()), blueish_students))

        # green
        green_students = list(filter(lambda x: x.get_status() == StudentStatus.ONLY_ONE, self.lof_gstudents))
        list(map(lambda x: x.setVisible(self.buttons['green'].isChecked()), green_students))

        for btn in self.buttons:
            self.buttons[btn].setText('ON' if self.buttons[btn].isChecked() else 'OFF')

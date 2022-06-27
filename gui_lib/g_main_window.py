from PyQt6.QtWidgets import *
from PyQt6.QtGui import QKeySequence, QPalette, QColor
from PyQt6.QtCore import pyqtSlot, pyqtSignal, Qt
import sort_lib.sort
from gui_lib.g_student import GStudent
from gui_lib.g_day import GDay

class GMainWindow(QMainWindow):

    content_refreshed = pyqtSignal()

    def __init__(self, model: 'sort_lib.sort.Sort', parent: QWidget=None):
        super().__init__(parent)
        self._model = model

        # FIXME: TESTING PURPOSES
        self.model.load_file_subjects('./data/input_predmety.csv')
        self.model.load_file_students('./data/input_zaci-2R-anonym.csv')
        # END TESTING

        self.setupUI()
        self.selected_students = set()
        self.selected_days = set()

        self.lof_gdays = []
    

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
        self.main_grid_layout.setRowStretch(1, 2)
        self.main_grid_layout.setRowStretch(2, 0)
        self.main_grid_layout.setColumnStretch(0, 2)
        self.main_grid_layout.setColumnStretch(1, 3)
        self.main_grid_layout.setColumnStretch(2, 3)
        self.main_grid_layout.setColumnStretch(3, 1)
        self.main_grid_layout.setColumnStretch(4, 1)

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
        add_action('Exportovat data', self.slt_export, file_menu, 'Ctrl+E')

        file_menu.addSeparator()
        self.auto_refresh_action = file_menu.addAction('Auto-refresh')
        self.auto_refresh_action.setCheckable(True)
        file_menu.addSeparator()
        add_action('Zavřít', self.close, file_menu)

        # student menu
        student_menu = self.menu_bar.addMenu('Student')
        add_action('Přidat studenta', self.slt_add_student, student_menu)
        add_action('Smazat studenta', self.slt_delete_student, student_menu)
        student_menu.addSeparator()
        add_action('Načíst studenty', self.slt_import_students, student_menu)

        # dny menu
        day_menu = self.menu_bar.addMenu('Dny')
        add_action('Přidat den', self.slt_add_day, day_menu)
        add_action('Odstranit dny', self.slt_remove_days, day_menu)
        day_menu.addSeparator()
        add_action('Načíst předměty', self.slt_import_subjects, day_menu)

        # trideni
        add_action('AKTUALIZACE', self.slt_sort, self.menu_bar)


    def _setup_student_panel(self):
        # skrolovaci plocha
        lof_students_scrar = QScrollArea(self)
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
        self.main_grid_layout.addWidget(lof_students_scrar, 1, 0, 2, 2)

        # hlavicka sekce
        self.main_grid_layout.addWidget(QLabel("Studenti"), 0, 0)
        self.buttons = {
            'red': QPushButton('ON'),
            'yellow': QPushButton('ON'),
            'green': QPushButton('ON'),
        }
        w = QWidget()
        w.setLayout(QHBoxLayout())
        for btn in self.buttons:
            self.buttons[btn].setCheckable(True)
            self.buttons[btn].setChecked(True)
            self.buttons[btn].setAutoFillBackground(True)
            pal = QPalette()
            pal.setColor(QPalette.ColorRole.Button, QColor(btn))
            self.buttons[btn].setPalette(pal)
            self.buttons[btn].toggled.connect(self.filter_students)
            w.layout().addWidget(self.buttons[btn])
        self.main_grid_layout.addWidget(w, 0, 1)

        # zobrazeni dat
        self.lof_gstudents = [GStudent(student, self.student_vbox, self) 
                              for student in self.model.students]
    

    def _setup_day_panel(self):
        # FIXME: refactor
        self.main_grid_layout.addWidget(QLabel('Dny'), 0, 2)
        w = QWidget()
        w.setLayout(QHBoxLayout())
        add_btn = QPushButton('ADD')
        add_btn.clicked.connect(self.slt_add_day)
        delete_btn = QPushButton('DELETE')
        delete_btn.clicked.connect(lambda: print('delete'))
        w.layout().addWidget(add_btn)
        w.layout().addWidget(delete_btn)
        self.main_grid_layout.addWidget(w, 0, 3)

        self.day_widget = QWidget()
        self.day_widget.setLayout(QHBoxLayout())
        self.main_grid_layout.addWidget(self.day_widget, 1, 2, 2, 2)
        pass
    

    def _setup_right_panel(self):
        w = QWidget()
        vbox = QVBoxLayout()
        w.setLayout(vbox)
        stats = self.model.get_students_per_subject()
        # FIXME: refactor 
        for stat in dict(sorted(stats.items(), key=lambda x: x[1], reverse=True)):
            w_stat = QWidget()
            w_stat.setLayout(QHBoxLayout())
            w_stat.layout().setContentsMargins(0, 4, 5, 1)
            lbl = QLabel(f'{stat} {stats[stat]}')
            font = lbl.font()
            font.setPointSize(15)
            lbl.setFont(font)
            w_stat.layout().addWidget(lbl, alignment=Qt.AlignmentFlag.AlignCenter)
            vbox.addWidget(w_stat)
        vbox.setSpacing(1)
        vbox.setContentsMargins(0, 0, 0, 0)

        self.main_grid_layout.addWidget(QLabel('Statistiky'), 0, 4, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_grid_layout.addWidget(w, 1, 4)
        btn = QPushButton('button')
        btn.clicked.connect(lambda: print('button'))
        self.main_grid_layout.addWidget(btn, 2, 4)


    def select_student(self, gstudent: 'GStudent', status: bool):
        if status:
            self.selected_students.add(gstudent)
        else:
            self.selected_students.discard(gstudent)
    

    def select_day(self, gday: 'GDay', status: bool):
        if status:
            self.selected_days.add(gday)
        else:
            self.selected_days.discard(gday)

    
    # slots  
    @pyqtSlot()
    def slt_delete_student(self):
        # TODO:
        print('delete student')
        for gs in self.selected_gstudents:
            gs.remove_widget()
            self.model.delete_student(gs.model)

    @pyqtSlot()
    def slt_open_file(self):
        # TODO:
        print("open file")


    @pyqtSlot()
    def slt_save(self):
        # TODO:
        print('save')


    @pyqtSlot()
    def slt_import_subjects(self):
        # TODO:
        print('import subjects')


    @pyqtSlot()
    def slt_export(self):
        # TODO:
        self.model.sort_data()
        # FIXME: remove hardcoded code
        self.model.export_data(r'C:\Users\hungd\Documents\GitHub\gymul_seminare\data')
        print('export data')
    

    @pyqtSlot()
    def slt_import_students(self):
        # TODO:
        print('import students')


    @pyqtSlot()
    def slt_close_app(self):
        # TODO:
        print('close app')
    

    @pyqtSlot()
    def slt_add_student(self):
        # TODO:
        print('add student')

    
    @pyqtSlot()
    def slt_add_day(self):
        # TODO:
        new_day = self.model.add_day()
        self.lof_gdays.append(GDay(new_day, self.day_widget.layout(), self))
        print('add day')
    

    @pyqtSlot()
    def slt_remove_days(self):
        # TODO:
        # for gd in self.selected_gdays:
        #     student = gd.model
        #     gd.delete()
        #     self.subsort.delete_student(student)
        print('remove days')
    

    @pyqtSlot()
    def slt_sort(self):
        self.model.sort_data()
        self.content_refreshed.emit()
        print('sort')
    

    @pyqtSlot()
    def filter_students(self):
        # red
        red_students = list(filter(lambda x: len(x.model.possible_comb) < 1, self.lof_gstudents))
        list(map(lambda x: x.setVisible(self.buttons['red'].isChecked()), red_students))

        # yellow
        yellow_students = list(filter(
            lambda x: len(x.model.possible_comb) > 1 and x.model.chosen_comb is None,
            self.lof_gstudents))
        list(map(lambda x: x.setVisible(self.buttons['yellow'].isChecked()), yellow_students))

        # green
        green_students = list(filter(lambda x: x.model.chosen_comb is not None, self.lof_gstudents))
        list(map(lambda x: x.setVisible(self.buttons['green'].isChecked()), green_students))

        for btn in self.buttons:
            self.buttons[btn].setText('ON' if self.buttons[btn].isChecked() else 'OFF')
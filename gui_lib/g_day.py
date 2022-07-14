from sort_lib.day import Day
import gui_lib.g_main_window
from gui_lib.g_subject import GSubject
from PySide6.QtWidgets import *
from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QPaintEvent, QPainter, QMouseEvent

class GDay(QFrame):
    """Graficka reprezentace dnu."""

    def __init__(self, model: Day, base_layout: QBoxLayout, base_gparent: 'gui_lib.g_main_window.GMainWindow'):
        super().__init__()
        self._model = model
        self._base_gparent = base_gparent
        # Seznam bunek g-predmetu
        self.gsubjects = []
        # Stav usporadani predmetu
        self._highlight_filter = False
        self.setProperty('isSelected', False)

        # vygenerovani celeho widgetu a vlozeni do programu
        self._setupUI()
        base_layout.insertWidget(base_layout.count() - 1, self)
        self.update_style()
    

    @property
    def model(self):
        return self._model
    

    def _setupUI(self):
        """Vygeneruje obsah g-dnu."""
        self.setLayout(QGridLayout())
        self.WIDTH = 5

        # vlozeni g-predmetu do na platno dne
        sorted_subjects = sorted(self._base_gparent.model.subjects.keys())
        for i in range(len(sorted_subjects)):
            subj = GSubject(sorted_subjects[i], self,
                            self._model.get_subject(sorted_subjects[i]))
            self.gsubjects.append(subj)

            # pripojeni signalu a slotu
            self._base_gparent.data_updated.connect(subj.content_update)
            subj.selected_subjects_changed.connect(self.update_layout)

        # vlozeni na platno
        self.update_layout()


    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Prepsana funkce reakce na udalost mysi."""
        # leve tlacitko na mysi prepina stav oznaceni dne
        if event.button() == Qt.MouseButton.LeftButton:
            self.setProperty('isSelected', not self.property('isSelected'))
            self._base_gparent.select_day(self, self.property('isSelected'))
            self.update_style()
        super().mousePressEvent(event)
    

    def delete_gday(self):
        """Smaze den z programu."""
        # TODO: disconnect connections
        self._base_gparent.model.remove_day(self.model)
        self._base_gparent.lof_gdays.remove(self)
        self.setParent(None)
    

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
    

    # TODO: create connection with **subject_list_updated** and **subject_list_clear**

    @Slot()
    def update_subjects(self):
        # seznam predmetu
        subjects = self._base_gparent.model.subjects.keys()
        gsubj_names = [gsubject.name for gsubject in self.gsubjects]
        removed_subjects = [gsubject for gsubject in self.gsubjects if gsubject.name not in subjects]
        new_subjects = [name for name in subjects if name not in gsubj_names]

        # smazat stare predmety
        for gsubj in removed_subjects:
            gsubj.setParent(None)
            self.gsubjects.remove(gsubj)

        # nacist nove predmety
        for subj in new_subjects:
            self.gsubjects.append(GSubject(subj, self, self._model.get_subject(subj)))
        self.update_layout()


    @Slot()
    def update_layout(self):
        """Preusporada predmety podle stavu."""
        # zobrazi na zacatku tabulky oznacene predmety
        if self._highlight_filter:
            # funkce odstrani vsechny g-predmety a pote je vsechny zpatky vlozi
            list(map(lambda x: x.setParent(None), self.gsubjects))
            selected = sorted([gsubj for gsubj in self.gsubjects 
                               if gsubj.property('isSelected')], key=lambda x: x.name)
            not_selected = sorted([gsubj for gsubj in self.gsubjects 
                                   if not gsubj.property('isSelected')], key=lambda x: x.name)

            for i in range(len(self.gsubjects)):
                # nejprve vlozi oznacene predmety
                if i < len(selected):
                    self.layout().addWidget(selected[i], i // self.WIDTH, i % self.WIDTH)
                # pote vlozi zbytek predmetu
                else:
                    self.layout().addWidget(not_selected[i - len(selected)], i // self.WIDTH, i % self.WIDTH)
        else:
            list(map(lambda x: x.setParent(None), self.gsubjects))
            subjects = sorted([gsubj for gsubj in self.gsubjects], key=lambda x: x.name)
            for i in range(len(subjects)):
                self.layout().addWidget(subjects[i], i // self.WIDTH, i % self.WIDTH)
    

    @Slot()
    def filter_toggle(self):
        """Prepina stav usporadani predmetu."""
        btn: QPushButton = self.sender()
        self._highlight_filter = btn.isChecked()
        self.update_layout()
    

    @Slot()
    def update_style(self):
        """Aktualizuje vzhled GDay."""
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()
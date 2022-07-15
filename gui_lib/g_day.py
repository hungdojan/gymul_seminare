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
        self.gsubjects: dict[str, GSubject] = {}
        # Stav usporadani predmetu
        self._highlight_filter = False
        self.setProperty('isSelected', False)

        self._base_gparent.subject_list_updated.connect(self.update_list)

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
            self.gsubjects[sorted_subjects[i]] = subj

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
        list(map(lambda subj: self._base_gparent.data_updated.disconnect(subj.content_update), list(self.gsubjects.values())))
        
        self._base_gparent.subject_list_updated.disconnect(self.update_list)

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
    

    @Slot(list)
    def update_list(self, l: list) -> None:
        for name in l:
            # odstani predmet
            if self.gsubjects.get(name) is not None:
                self._base_gparent.data_updated.disconnect(self.gsubjects[name].content_update)
                self.gsubjects[name].selected_subjects_changed.disconnect(self.update_layout)

                self.gsubjects[name].setParent(None)
                del self.gsubjects[name]
            # prida predmet
            else:
                gsubject = GSubject(name, self, self._model.get_subject(name))

                self._base_gparent.data_updated.connect(gsubject.content_update)
                gsubject.selected_subjects_changed.connect(self.update_layout)

                self.gsubjects[name] = gsubject
        self.update_layout()


    @Slot()
    def update_layout(self):
        """Preusporada predmety podle stavu."""
        # zobrazi na zacatku tabulky oznacene predmety
        list(map(lambda x: x.setParent(None), list(self.gsubjects.values())))
        if self._highlight_filter:
            # funkce odstrani vsechny g-predmety a pote je vsechny zpatky vlozi
            selected = sorted([gsubj for gsubj in list(self.gsubjects.values()) 
                               if gsubj.property('isSelected')], key=lambda x: x.name)
            not_selected = sorted([gsubj for gsubj in list(self.gsubjects.values()) 
                                   if not gsubj.property('isSelected')], key=lambda x: x.name)

            for i in range(len(self.gsubjects)):
                # nejprve vlozi oznacene predmety
                if i < len(selected):
                    self.layout().addWidget(selected[i], i // self.WIDTH, i % self.WIDTH)
                # pote vlozi zbytek predmetu
                else:
                    self.layout().addWidget(not_selected[i - len(selected)], i // self.WIDTH, i % self.WIDTH)
        else:
            subjects = sorted(list(self.gsubjects.values()), key=lambda x: x.name)
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
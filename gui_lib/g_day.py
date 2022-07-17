import gui_lib.g_day_panel
from sort_lib.day import Day
from gui_lib.g_subject import GSubject
from PySide6.QtWidgets import *
from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QPaintEvent, QPainter, QMouseEvent

class GDay(QFrame):
    """Graficka reprezentace dnu."""

    def __init__(self, model: Day, base_gparent: 'gui_lib.g_day_panel.GDayPanel'):
        super().__init__()
        self._model = model
        self._base_gparent = base_gparent
        # Seznam bunek g-predmetu
        self.gsubjects: dict[str, GSubject] = {}
        # Stav usporadani predmetu
        self._highlight_filter = self._base_gparent._base_gparent.day_buttons['filter'].isChecked()
        self.setProperty('isSelected', False)

        # vygenerovani celeho widgetu a vlozeni do programu
        self._setupUI()
        self.update_style()
    

    @property
    def model(self):
        return self._model
    

    def _setupUI(self):
        """Vygeneruje obsah g-dnu."""
        self.setLayout(QGridLayout())
        self.WIDTH = 5

        # vlozeni g-predmetu do na platno dne
        sorted_subjects = sorted(self._base_gparent._base_gparent.model.subjects.keys())
        for i in range(len(sorted_subjects)):
            self.create_subject(sorted_subjects[i])

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


    def disconnect(self):
        """Odpoji signaly a sloty jednotlivych predmetu ve dni."""
        list(map(lambda subj: self._base_gparent._base_gparent.data_updated.disconnect(
                                subj.content_update), list(self.gsubjects.values())))


    def update_style(self):
        """Aktualizuje vzhled GDay."""
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()
    

    def create_subject(self, subject_name: str) -> GSubject:
        """Vytvori instanci g-predmetu ve dni.

        Vytvoreny predmet je ulozen v self.subjects, ale neni vlozen na platno.

        Args:
            subject_name (str): Jmeno predmetu.

        Returns:
            GSubject: Vytvorena instance predmetu.
        """
        gsubject = GSubject(subject_name, self, self._model.get_subject(subject_name))

        self._base_gparent._base_gparent.data_updated.connect(gsubject.content_update)
        gsubject.selected_subjects_changed.connect(self.update_layout)
        self.gsubjects[subject_name] = gsubject
        return gsubject
    

    def remove_subject(self, subject_name: str):
        """Vyjme a odstrani predmet ze dnu.

        Args:
            subject_name (str): Jmeno predmetu.
        """
        gsubject = self.gsubjects[subject_name]
        self._base_gparent._base_gparent.data_updated.disconnect(gsubject.content_update)
        gsubject.selected_subjects_changed.disconnect(self.update_layout)
        if gsubject.property('isSelected'):
            self._model.remove_subject(gsubject.name)
        gsubject.deleteLater()
        del self.gsubjects[subject_name]
    

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
                self.remove_subject(name)
            # prida predmet
            else:
                self.create_subject(name)
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
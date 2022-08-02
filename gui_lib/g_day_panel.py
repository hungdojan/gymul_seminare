from PySide6.QtWidgets import QScrollArea, QFrame, QVBoxLayout
from PySide6.QtCore import Slot
from gui_lib.commands.day_panel_actions import DayPanelDeleteDays

import gui_lib.g_main_window
from gui_lib.g_day import GDay

from sort_lib.day import Day

class GDayPanel(QScrollArea):
    
    def __init__(self, base_gparent: 'gui_lib.g_main_window.GMainWindow'):
        super().__init__()
        self._base_gparent = base_gparent
        self.lof_gdays: list[GDay] = []
        self.selected_gdays: list[GDay] = []
        self._setupUI()

        # nastaveni
        self.setWidgetResizable(True)
    

    @property
    def base_gparent(self) -> 'gui_lib.g_main_window.GMainWindow':
        return self._base_gparent
    

    def _setupUI(self):
        """Vygeneruje obsah GDayPanel."""
        self.main_frame = QFrame()
        self.main_frame.setLayout(QVBoxLayout())
        self.main_frame.layout().addStretch()

        self.setWidget(self.main_frame)
    

    def add_gday(self, day: Day, index: int=-1) -> GDay:
        """Vytvori instanci dne a prida ho na platno.

        Args:
            day (Day): Model dne.
            index (int, optional): Radek, na ktery se ma den pridat. Defaults to -1.

        Returns:
            GDay: Instance vytvoreneho g-dne.
        """
        gday = GDay(day, self)

        self._base_gparent.day_buttons['filter'].toggled.connect(gday.filter_toggle)
        self._base_gparent.subject_list_updated.connect(gday.update_list)
        if index < 0:
            self.lof_gdays.append(gday)
            self.main_frame.layout().insertWidget(len(self.lof_gdays) - 1, gday)
        else:
            self.lof_gdays.insert(index, gday)
            self.main_frame.layout().insertWidget(index, gday)
        return gday


    def select_day(self, gday: GDay, is_selected: bool):
        """Spravuje oznacene GDny

        Args:
            gday (GDay): Instance GDay, ktereho se Všechny operace tyka
            isSelected (bool): Pravdivostni hodnota, zda byl objekt oznacen ci ne
        """
        if is_selected:
            self.selected_gdays.append(gday)
        else:
            try:
                self.selected_gdays.remove(gday)
            except ValueError:
                pass
    

    def clear(self):
        """Smaze vsechny dny."""
        for i in range(len(self.lof_gdays) - 1, -1, -1):
            self.delete_gday(self.lof_gdays[i])
        self.lof_gdays.clear()
        self.selected_gdays.clear()


    def delete_gday(self, gday: GDay):
        """Smaze vybrany den.

        G-den je ignorovan, pokud neni soucasti panelu.

        Args:
            gday (GDay): Instance g-dnu, ktery bude smazan.
        """
        if gday not in self.lof_gdays:
            return

        gday.disconnect()
        self._base_gparent.day_buttons['filter'].toggled.disconnect(gday.filter_toggle)
        self._base_gparent.subject_list_updated.disconnect(gday.update_list)
        self._base_gparent.model.remove_day(gday.model)
        self.lof_gdays.remove(gday)
        gday.deleteLater()


    @Slot()
    def delete_selected(self):
        """Smaze oznacene predmety."""
        self._base_gparent.command_builder.execute(DayPanelDeleteDays(self))
        self._base_gparent.view_updated.emit()

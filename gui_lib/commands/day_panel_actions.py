from sort_lib.command import Command

import gui_lib.g_main_window
from sort_lib.file_log import FileLog

class DayPanelAddDay(Command):
    
    def __init__(self, gmainwindow: 'gui_lib.g_main_window.GMainWindow') -> None:
        self._gmainwindow = gmainwindow
        self._day = gmainwindow.model.add_day()
    
    def execute(self) -> None:
        FileLog.loggers['default'].info('CMD: Execute DayPanelAddDay')
        self._gday = self._gmainwindow.day_panel.add_gday(self._day)
        self._index = len(self._gmainwindow.model.days) - 1


    def redo(self) -> None:
        self._gmainwindow.model.add_day(self._day, self._index)
        self._gday = self._gmainwindow.day_panel.add_gday(self._day, self._index)

    def undo(self) -> None:
        self._gmainwindow.day_panel.delete_gday(self._gday)


class DayPanelDeleteDays(Command):
    
    def __init__(self, parent: 'gui_lib.g_day_panel.GDayPanel') -> None:
        self._parent = parent
        self._gmainwindow = parent.base_gparent
        self._selected_gdays = list(sorted(parent.selected_gdays, key=parent.lof_gdays.index))
        parent.selected_gdays = []
        self._days = {}
        for gday in self._selected_gdays:
            self._days[parent.lof_gdays.index(gday)] = gday.model
    
    def execute(self) -> None:
        list(map(lambda x: self._parent.delete_gday(x), self._selected_gdays))
        self._selected_gdays.clear()
        FileLog.loggers['default'].info('CMD: Execute DayPanelDeleteDays')

    def redo(self) -> None:
        self.execute()

    def undo(self) -> None:
        for i in self._days:
            self._gmainwindow.model.add_day(self._days[i], i)
            gday = self._gmainwindow.day_panel.add_gday(self._days[i], i)
            self._selected_gdays.append(gday)
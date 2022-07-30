from PySide6.QtCore import QObject, Slot
from abc import ABC, abstractmethod

class Command(ABC):

    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass

    @abstractmethod
    def redo(self) -> None:
        pass


class CommandBuilder(QObject):

    def __init__(self):
        super().__init__()
        # inicializuje seznamy prikazu
        self.undo_stack: list[Command] = []
        self.redo_stack: list[Command] = []
    

    def execute(self, command: Command):
        """Provede akci pri zavolani.

        Args:
            command (Command): Trida s definovanou akci.
        """
        if command is None:
            return

        self.redo_stack.clear()
        self.undo_stack.append(command)
        command.execute()
    

    def redo(self):
        """Provede krok vpred."""
        if not self.redo_stack:
            return

        cmd = self.redo_stack.pop()
        cmd.redo()
        self.undo_stack.append(cmd)


    def undo(self):
        """Provede krok zpet."""
        if not self.undo_stack:
            return
        cmd = self.undo_stack.pop()
        cmd.undo()
        self.redo_stack.append(cmd)
    

    def clear(self):
        self.redo_stack.clear()
        self.undo_stack.clear()


    @Slot()
    def redo_slot(self):
        self.redo()

    
    @Slot()
    def undo_slot(self):
        self.undo()
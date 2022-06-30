from sys import argv
from sort_lib.sort import Sort
from gui_lib.g_main_window import GMainWindow
from PySide6.QtWidgets import QApplication

def main():
    app = QApplication(argv)

    g_main_window = GMainWindow(Sort())
    g_main_window.show()

    app.exec()


if __name__ == "__main__":
    main()
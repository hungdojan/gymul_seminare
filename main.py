from sys import argv
from sort_lib.sort import Sort
from gui_lib.g_main_window import GMainWindow
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase

def main():
    app = QApplication(argv)

    # nacteni fontu
    QFontDatabase.addApplicationFont(":/font-awesome-brands.otf")
    QFontDatabase.addApplicationFont(":/font-awesome-regular.otf")
    QFontDatabase.addApplicationFont(":/font-awesome-solid.otf")

    g_main_window = GMainWindow(Sort())
    g_main_window.show()

    app.exec()


if __name__ == "__main__":
    main()
import os
from sys import argv
import gui_lib
from sort_lib.sort import Sort
from sort_lib.file_log import FileLog
from gui_lib.g_main_window import GMainWindow
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase

def main():
    FileLog.loggers['default'].info(f'Initialize application Seminare v{gui_lib.__version__}')
    app = QApplication(argv)

    # nacteni fontu
    QFontDatabase.addApplicationFont(":/font-awesome-brands.otf")
    QFontDatabase.addApplicationFont(":/font-awesome-regular.otf")
    QFontDatabase.addApplicationFont(":/font-awesome-solid.otf")

    g_main_window = GMainWindow(Sort())
    g_main_window.show()

    app.exec()


if __name__ == "__main__":
    # smazat stary log soubor
    if os.path.isfile('seminare.log'):
        os.remove('seminare.log')
    FileLog.init_log('default', 'seminare.log')
    main()
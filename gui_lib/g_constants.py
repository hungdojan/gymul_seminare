from PySide6.QtGui import QColor
from PySide6.QtCore import Qt

COLORS_DICT = {
    'green'   : '#c2ed98',
    'red'     : '#f59b7c',
    'yellow'  : '#fed776',
    'blue-ish': '#8ed2cd'
    
}
class GWidgetColors:
    # source: https://www.pinterest.com/pin/143130094399827603/
    STUDENT_PASSED = QColor('#c2ed98')
    STUDENT_FAILED = QColor('#f59b7c')
    STUDENT_MULTIPLE = QColor('#fed776')
    STUDENT_MULTIPLE_CHOSEN = QColor('#8ed2cd')

class LabelWidth:
    # TODO:
    STUD_ID_MIN=0
    STUD_ID_MAX=0
    STUD_FNAME_MIN=0
    STUD_FNAME_MAX=0
    STUD_LNAME_MIN=0
    STUD_LNAME_MAX=0
    STUD_CLASS_MIN=0
    STUD_CLASS_MAX=0

# Resource object code (Python 3)
# Created by: object code
# Created by: The Resource Compiler for Qt version 6.3.1
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore

qt_resource_data = b"\
\x00\x00\x05\x1f\
/\
* source: https:\
//www.pinterest.\
com/pin/14313009\
4399827603/ */\x0a\x0a\
/* Student filte\
r buttons */\x0aQPu\
shButton#FailedB\
utton {\x0a    back\
ground-color: #f\
59b7c;\x0a}\x0a\x0aQPushB\
utton#MultipleBu\
tton {\x0a    backg\
round-color: #fe\
d776;\x0a}\x0a\x0aQPushBu\
tton#SuccessButt\
on {\x0a    backgro\
und-color: #c2ed\
98;\x0a}\x0a\x0aQPushButt\
on#ChosenButton \
{\x0a    background\
-color: #8ed2cd;\
\x0a}\x0a\x0a/* GStudent \
settings */\x0a\x0aGSt\
udent[status = \x22\
noComb\x22] {\x0a    b\
ackground-color:\
 #f59b7c;\x0a}\x0a\x0aGSt\
udent[status = \x22\
mulComb\x22] {\x0a    \
background-color\
: #fed776;\x0a}\x0a\x0aGS\
tudent[status = \
\x22mulSet\x22] {\x0a    \
background-color\
: #8ed2cd;\x0a}\x0a\x0aGS\
tudent[status = \
\x22onlyOne\x22] {\x0a   \
 background-colo\
r: #c2ed98;\x0a}\x0a\x0aG\
Student[isSelect\
ed = \x22true\x22] {\x0a \
   border: dotte\
d;\x0a    border-co\
lor: #111;\x0a    b\
order-width: 2px\
;\x0a}\x0a\x0aGStudent[is\
Selected = \x22fals\
e\x22] {\x0a    border\
: none;\x0a}\x0a\x0a/* Su\
bject combobox c\
ollision highlig\
ht */\x0a/* https:/\
/www.colorxs.com\
/color/dark-past\
el-red */\x0aGCombo\
Box[valid = 'fal\
se'] {\x0a    backg\
round-color: #c2\
3b22;\x0a    color:\
 #eee;\x0a}\x0a\x0aGCombo\
Box[valid = 'tru\
e'] {\x0a    backgr\
ound-color: #fff\
;\x0a    color: #00\
0;\x0a}\x0a\x0aGComboBox:\
disabled {\x0a    /\
* TODO: WILL BE \
CHANGED IN THE F\
UTURE */\x0a    bac\
kground-color: #\
3e4772;\x0a    colo\
r: #eee;\x0a}\x0a\x0a/* G\
MainWindow style\
 */\x0aGMainWindow \
{\x0a}\x0a\x0a/* temporar\
y colors\x0ahttps:/\
/www.color-hex.c\
om/color-palette\
/94888\x0a{\x0a    bac\
kground-color: #\
3e4772;\x0a    colo\
r: #eee;\x0a}\x0a */\
"

qt_resource_name = b"\
\x00\x0e\
\x03\xc2\xd5\xc3\
\x00s\
\x00t\x00y\x00l\x00e\x00s\x00h\x00e\x00e\x00t\x00.\x00q\x00s\x00s\
"

qt_resource_struct = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x81\xb5\xb8\xecR\
"

def qInitResources():
    QtCore.qRegisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()

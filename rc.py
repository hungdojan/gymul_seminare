# Resource object code (Python 3)
# Created by: object code
# Created by: The Resource Compiler for Qt version 6.3.1
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore

qt_resource_data = b"\
\x00\x00\x02z\
Q\
PushButton#Faile\
dButton {\x0d\x0a    b\
ackground-color:\
 #f59b7c;\x0d\x0a}\x0d\x0a\x0d\x0a\
QPushButton#Mult\
ipleButton {\x0d\x0a  \
  background-col\
or: #fed776;\x0d\x0a}\x0d\
\x0a\x0d\x0aQPushButton#S\
uccessButton {\x0d\x0a\
    background-c\
olor: #c2ed98;\x0d\x0a\
}\x0d\x0a\x0d\x0aQPushButton\
#ChosenButton {\x0d\
\x0a    background-\
color: #8ed2cd;\x0d\
\x0a}\x0d\x0a\x0d\x0aGStudent[s\
tatus = \x22noComb\x22\
]{\x0d\x0a    backgrou\
nd-color: #f59b7\
c;\x0d\x0a}\x0d\x0a\x0d\x0aGStuden\
t[status = \x22mulC\
omb\x22]{\x0d\x0a    back\
ground-color: #f\
ed776;\x0d\x0a}\x0d\x0a\x0d\x0aGSt\
udent[status = \x22\
mulSet\x22]{\x0d\x0a    b\
ackground-color:\
 #8ed2cd;\x0d\x0a}\x0d\x0a\x0d\x0a\
GStudent[status \
= \x22onlyOne\x22]{\x0d\x0a \
   background-co\
lor: #c2ed98;\x0d\x0a}\
\x0d\x0a\x0d\x0a/*\x0d\x0a'green' \
  : '#c2ed98',\x0d\x0a\
'red'     : '#f5\
9b7c',\x0d\x0a'yellow'\
  : '#fed776',\x0d\x0a\
'blue-ish': '#8e\
d2cd'\x0d\x0a*/\
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
\x00\x00\x01\x81\xb3\xf6U\x8f\
"

def qInitResources():
    QtCore.qRegisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()

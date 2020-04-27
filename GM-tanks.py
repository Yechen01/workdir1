# coding=utf-8

import tanks
import sys
from threading import Thread
from GMGUI.MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore

# # 处理编码问题
# mycode = "utf-8"                                      
# code = QtCore.QTextCodec.codecForName(mycode)
# QtCore.QTextCodec.setCodecForLocale(code)
# QtCore.QTextCodec.setCodecForTr(code)
# QtCore.QTextCodec.setCodecForCStrings(code)

app = QApplication(sys.argv)
GMWindow = MainWindow(tanks)
GMWindow.show()
sys.exit(app.exec_())


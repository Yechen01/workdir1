# coding=utf-8

from PyQt5.QtWidgets import QGroupBox, QListWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer
from .Controller import Controller

class EnermyDataWidget(QGroupBox):
    """
        自动获取敌人数量类型和坐标
    """

    def __init__(self,tanks):
        super(EnermyDataWidget,self).__init__()
        self.Controller = Controller(tanks)

        self.setTitle("敌人坐标")
        self.Tanks = tanks

        self.MainLayout = QVBoxLayout()

        self.EnermyList = QListWidget()
        self.CountLabel = QLabel("敌人数量：")

        self.MainLayout.addWidget(self.CountLabel)
        self.MainLayout.addWidget(self.EnermyList)

        self.Timer = QTimer()
        self.Timer.timeout.connect(self.getData)
        self.Timer.start(100)

        self.setLayout(self.MainLayout)

    def getData(self):

        el = self.Controller.getEnemyList()
        if not el:
            return
        
        num = len(el)
        self.CountLabel.setText("敌人数量："+str(num))
        self.EnermyList.clear()
        for ene in el:
           self.EnermyList.addItem(ene[0] + str(ene[1]))
           



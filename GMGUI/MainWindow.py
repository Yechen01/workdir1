# coding=utf-8

#from PyQt5.QtWidgets import
from PyQt5.QtWidgets import QMessageBox,QWidget,QPushButton,QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon
from .PlayerDataWidget import PlayerDataWidget
from .PlayerControllerWidget import PlayerControllerWidget
from .EnermyDataWidget import EnermyDataWidget
from .AddBonusWidget import AddBonusWidget
from .AIWidget import AIWidget
from .AutoAIWidget import AutoAIWidget
from .FunctionWidget import FunctionWidget
from threading import Thread

from .TaskWidget import ControllerDataWidget

class MainWindow(QWidget):
    """
        主窗口，柔和各种窗口
    """

    def __init__(self,tanks):
        super(MainWindow,self).__init__()
        self.setWindowTitle("GM版坦克大战工具集")
        self.setWindowIcon(QIcon("icon.png"))


        self.Tanks = tanks

        self.ControllerDataWidget = ControllerDataWidget(self.Tanks)

        self.MainLayout = QHBoxLayout()
        self.BaseLayout = QVBoxLayout()

        self.PlayerDataWidget = PlayerDataWidget(self.Tanks)
        self.PlayerControllerWidget = PlayerControllerWidget(self.Tanks)
        self.EnermyDataWidget = EnermyDataWidget(self.Tanks)
        self.AddBonusWidget = AddBonusWidget(self.Tanks)
        self.FunctionWidget = FunctionWidget(self.Tanks)
        
        self.BaseLayout.addWidget(self.PlayerDataWidget)
        self.BaseLayout.addWidget(self.EnermyDataWidget)
        self.BaseLayout.addWidget(self.AddBonusWidget)
        self.BaseLayout.addWidget(self.FunctionWidget)
        self.BaseLayout.addWidget(self.PlayerControllerWidget) 

        self.AIWidget = AIWidget(self.Tanks)
        self.AutoAIWidget = AutoAIWidget(self.Tanks)
        self.AIWidget.StartAIButton.clicked.connect(lambda : self.startAIClick(True))
        self.AIWidget.StartAIButton2.clicked.connect(lambda : self.startAIClick(True))
        self.AutoAIWidget.StartAIButton.clicked.connect(lambda : self.startAIClick(False))
        self.AutoAIWidget.StartAIButton2.clicked.connect(lambda : self.startAIClick(False))
        
        self.AIWidget.StopAIButton.clicked.connect(self.stopAIClick)
        self.AutoAIWidget.StopAIButton.clicked.connect(self.stopAIClick)
        
        self.MainLayout.addWidget(self.ControllerDataWidget)
        self.MainLayout.addLayout(self.BaseLayout)
        self.MainLayout.addWidget(self.AIWidget)
        self.MainLayout.addWidget(self.AutoAIWidget)

        # 运行游戏的线程
        self.Gamethread = Thread(target=self.showGame, args=())
        self.Gamethread.start()  

        self.setLayout(self.MainLayout)

    def showGame(self):
        self.Tanks.game = self.Tanks.Game()
        self.Tanks.castle = self.Tanks.Castle()
        self.Tanks.game.showMenu()


    def stopAIClick(self):
        """
            点击后开启 开始AI按钮
        """
        self.AIWidget.StartAIButton.setEnabled(True)
        self.AIWidget.StartAIButton2.setEnabled(True)
        self.AutoAIWidget.StartAIButton.setEnabled(True)
        self.AutoAIWidget.StartAIButton2.setEnabled(True)
        self.AIWidget.StopAIButton.setEnabled(False)
        self.AutoAIWidget.StopAIButton.setEnabled(False)
    

    def startAIClick(self,left):
        """
            点击后开启 关闭AI按钮
        """
        if self.Gamethread.isAlive() == False:
            QMessageBox.information(self,"提示","出现致命错误，游戏已被关闭，请重启GM工具")
            return
        self.AIWidget.StartAIButton.setEnabled(False)
        self.AIWidget.StartAIButton2.setEnabled(False)
        self.AutoAIWidget.StartAIButton.setEnabled(False)
        self.AutoAIWidget.StartAIButton2.setEnabled(False)
        if left:
            self.AIWidget.StopAIButton.setEnabled(True)
            self.AutoAIWidget.StopAIButton.setEnabled(False)
        else: 
            self.AIWidget.StopAIButton.setEnabled(False)
            self.AutoAIWidget.StopAIButton.setEnabled(True)
        



# coding=utf-8

from PyQt5.QtWidgets import QMessageBox,QGroupBox, QListWidget, QGridLayout, QPushButton,QFileDialog
from PyQt5.QtCore import QTimer
from .AnaWidget import AnaWidget
from .Controller import Controller
from threading import Thread

def tips(fn):
    def wrapped(c):
        try:
            fn(c)
        except Exception as e:
            QMessageBox.information(c,"发生错误","错误信息"+repr(e)+"\n可能是没有启动游戏造成！")
    return wrapped

    
class FunctionWidget(QGroupBox):
    """
        一些有用的功能的集合
    """

    def __init__(self,tanks):
        super(FunctionWidget,self).__init__()
        self.Controller = Controller(tanks)

        self.setTitle("有用功能")
        self.Tanks = tanks

        self.MainLayout = QGridLayout()

        self.OpenAnaButton = QPushButton(self)
        self.OpenAnaButton.setText("打开测试汇总")
        self.OpenAnaButton.clicked.connect(self.openAna)
        self.MainLayout.addWidget(self.OpenAnaButton,0,0,1,2)

        self.AddTankButton = QPushButton(self)
        self.AddTankButton.setText("强制增加敌人")
        self.AddTankButton.clicked.connect(self.addTank)
        self.MainLayout.addWidget(self.AddTankButton,0,2)

        self.NextLevelButton = QPushButton(self)
        self.NextLevelButton.setText("下一关")
        self.NextLevelButton.clicked.connect(self.nextLevel)
        self.MainLayout.addWidget(self.NextLevelButton,1,0)

        self.GameOverButton = QPushButton(self)
        self.GameOverButton.setText("结束游戏")
        self.GameOverButton.clicked.connect(self.gameOver)
        self.MainLayout.addWidget(self.GameOverButton,1,1)

        self.ReloadPlayerButton = QPushButton(self)
        self.ReloadPlayerButton.setText("重生玩家")
        self.ReloadPlayerButton.clicked.connect(self.reloadPlayer)
        self.MainLayout.addWidget(self.ReloadPlayerButton,1,2)


        self.setLayout(self.MainLayout)

    @tips
    def addTank(self):
        self.Controller.addTank()

    def openAna(self):
        fname = QFileDialog.getOpenFileName(self,'打开测试汇总', './TestResult',"Res files(*.res)")
        if (fname[0]==""):
            return

        self.AnaWidget  = AnaWidget(fname[0])
        self.AnaWidget.show()

    @tips
    def nextLevel(self):
        self.Controller.nextLevel()

    @tips
    def gameOver(self):
        # 防止阻塞
        t = Thread(target=self.Controller.gameOver, args=())
        t.setDaemon(True)
        t.start()
    
    @tips
    def reloadPlayer(self):
        self.Controller.reloadPlayer()
    
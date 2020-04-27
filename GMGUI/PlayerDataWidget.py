# coding=utf-8

#from PyQt5.QtWidgets import 
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QPushButton,QLabel,QHBoxLayout,QVBoxLayout,QGroupBox
from .Controller import Controller

class PlayerDataWidget(QGroupBox):
    """
        自动获取玩家信息窗口
    """

    def __init__(self,tanks):
        super(PlayerDataWidget,self).__init__()
        self.Controller = Controller(tanks)

        self.setTitle("玩家数据")

        self.Tanks = tanks

        self.Pos1Label_ = QLabel("玩家1坐标：")
        self.Life1Label_ = QLabel("玩家1生命：")
        self.Score1Label_ = QLabel("玩家1得分：")

        self.Pos2Label_ = QLabel("玩家2坐标：")
        self.Life2Label_ = QLabel("玩家2生命：")
        self.Score2Label_ = QLabel("玩家2得分：")

        self.Pos1Label = QLabel("等待获取")
        self.Life1Label = QLabel("等待获取")
        self.Score1Label = QLabel("等待获取")
        self.Pos2Label = QLabel("等待获取")
        self.Life2Label = QLabel("等待获取")
        self.Score2Label = QLabel("等待获取")

        self.LeftLayout = QVBoxLayout()
        self.RightLayout = QVBoxLayout()
        self.MainLayout = QHBoxLayout()

        self.LeftLayout.addWidget(self.Pos1Label_)
        self.LeftLayout.addWidget(self.Life1Label_)
        self.LeftLayout.addWidget(self.Score1Label_)
        self.LeftLayout.addWidget(self.Pos2Label_)
        self.LeftLayout.addWidget(self.Life2Label_)
        self.LeftLayout.addWidget(self.Score2Label_)

        self.RightLayout.addWidget(self.Pos1Label)
        self.RightLayout.addWidget(self.Life1Label)
        self.RightLayout.addWidget(self.Score1Label)
        self.RightLayout.addWidget(self.Pos2Label)
        self.RightLayout.addWidget(self.Life2Label)
        self.RightLayout.addWidget(self.Score2Label)

        self.MainLayout.addLayout(self.LeftLayout)
        self.MainLayout.addLayout(self.RightLayout)

        self.setLayout(self.MainLayout)

        self.Timer = QTimer()
        self.Timer.timeout.connect(self.getData)
        self.Timer.start(100)


    def getData(self):

        num = len(self.Tanks.players)
        
        if num == 1:
            self.Score1Label.setText(str(self.Controller.getPlayerScore(0)))
            self.Life1Label.setText(str(self.Controller.getPlayerLives(0)))
            self.Pos1Label.setText(str(self.Controller.getPlayerTopLeft(0)))
        elif num == 2:
            self.Score1Label.setText(str(self.Controller.getPlayerScore(0)))
            self.Score2Label.setText(str(self.Controller.getPlayerScore(1)))
            self.Life1Label.setText(str(self.Controller.getPlayerScore(0)))
            self.Life2Label.setText(str(self.Controller.getPlayerLives(1)))
            self.Pos1Label.setText(str(self.Controller.getPlayerScore(0)))
            self.Pos2Label.setText(str(self.Controller.getPlayerTopLeft(1)))
        else:
            self.Pos1Label.setText("等待获取")
            self.Pos2Label.setText("等待获取")
            self.Life1Label.setText("等待获取")
            self.Life2Label.setText("等待获取")
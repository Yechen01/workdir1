# coding=utf-8

from PyQt5.QtWidgets import QMessageBox,QGroupBox,QPushButton,QLabel,QGridLayout
from .Controller import Controller
from PyQt5.QtCore import Qt,pyqtSignal
import traceback

def tips(fn):
    def wrapped(c,*args,**kwargs):
        try:
            fn(c,*args,**kwargs)
        except Exception as e:
            QMessageBox.information(c,"发生错误","错误信息"+traceback.format_exc()+"\n可能是没有启动游戏造成！")
    return wrapped

class MyButton(QPushButton):

    pressed = pyqtSignal()
    released = pyqtSignal()

    def __init__(self,*args,**kwargs):
        super(MyButton,self).__init__(*args,**kwargs)
        
    def mousePressEvent(self,event):
        if event.button() == Qt.LeftButton:
            self.pressed.emit()
    
    def mouseReleaseEvent(self,event):
        if event.button() == Qt.LeftButton:
            self.released.emit()

    
class PlayerControllerWidget(QGroupBox):
    """
        玩家控制窗口
    """

    def __init__(self,tanks):
        super(PlayerControllerWidget,self).__init__()
        self.Controller = Controller(tanks)

        self.setTitle("玩家控制")
        self.Tanks = tanks

        self.MainLayout = QGridLayout()

        self.Up1Button = MyButton("向上")
        self.Left1Button = MyButton("向左")
        self.Down1Button = MyButton("向下")
        self.Right1Button = MyButton("向右")
        self.Fire1Button = QPushButton("射击")

        self.Up1Button.pressed.connect(lambda: self.goUp(1))
        self.Left1Button.pressed.connect(lambda: self.goLeft(1))
        self.Down1Button.pressed.connect(lambda: self.goDown(1))
        self.Right1Button.pressed.connect(lambda: self.goRight(1))
        self.Fire1Button.clicked.connect(lambda: self.fire(1))

        self.Up1Button.released.connect(lambda: self.goUp(1))
        self.Left1Button.released.connect(lambda: self.goLeft(1))
        self.Down1Button.released.connect(lambda: self.goDown(1))
        self.Right1Button.released.connect(lambda: self.goRight(1))


        self.Up2Button = MyButton("向上")
        self.Left2Button = MyButton("向左")
        self.Down2Button = MyButton("向下")
        self.Right2Button = MyButton("向右")
        self.Fire2Button = QPushButton("射击")

        self.Up2Button.pressed.connect(lambda: self.goUp(2))
        self.Left2Button.pressed.connect(lambda: self.goLeft(2))
        self.Down2Button.pressed.connect(lambda: self.goDown(2))
        self.Right2Button.pressed.connect(lambda: self.goRight(2))
        self.Fire2Button.clicked.connect(lambda: self.fire(2))

        self.Up2Button.released.connect(lambda: self.goUp(2))
        self.Left2Button.released.connect(lambda: self.goLeft(2))
        self.Down2Button.released.connect(lambda: self.goDown(2))
        self.Right2Button.released.connect(lambda: self.goRight(2))

        self.SplitLabel = QLabel("")

        self.Label1 = QLabel("玩家一")
        self.Label2 = QLabel("玩家二")

        self.MainLayout.addWidget(self.Label1,0,0)
        self.MainLayout.addWidget(self.Up1Button,0,1)
        self.MainLayout.addWidget(self.Left1Button,1,0)
        self.MainLayout.addWidget(self.Down1Button,2,1)
        self.MainLayout.addWidget(self.Right1Button,1,2)
        self.MainLayout.addWidget(self.Fire1Button,1,1)

        self.MainLayout.addWidget(self.SplitLabel,3,1)
        self.MainLayout.addWidget(self.SplitLabel,3,0)
        self.MainLayout.addWidget(self.SplitLabel,3,2)

        self.MainLayout.addWidget(self.Label2,5,0)
        self.MainLayout.addWidget(self.Up2Button,5,1)
        self.MainLayout.addWidget(self.Left2Button,6,0)
        self.MainLayout.addWidget(self.Down2Button,7,1)
        self.MainLayout.addWidget(self.Right2Button,6,2)
        self.MainLayout.addWidget(self.Fire2Button,6,1)

        self.setLayout(self.MainLayout)

    @tips
    def fire(self,player):
        if player == 1:
            self.Controller.player1Fire()
        elif player == 2: 
            self.Controller.player2Fire()

    @tips
    def goUp(self,player):
        if player == 1:
            self.Controller.player1GoUp()
        elif player == 2: 
            self.Controller.player2GoUp()
    
    @tips
    def goLeft(self,player):
        if player == 1:
            self.Controller.player1GoLeft()
        elif player == 2: 
            self.Controller.player2GoLeft()

    @tips
    def goRight(self,player):
        if player == 1:
            self.Controller.player1GoRight()
        elif player == 2: 
            self.Controller.player2GoRight()
    
    @tips
    def goDown(self,player):
        if player == 1:
            self.Controller.player1GoDown()
        elif player == 2: 
            self.Controller.player2GoDown()


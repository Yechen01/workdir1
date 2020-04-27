# coding=utf-8

from PyQt5.QtWidgets import QMessageBox, QGroupBox, QListWidget, QGridLayout, QPushButton
from PyQt5.QtCore import QTimer

from .Controller import Controller

def tips(fn):
    def wrapped(c):
        try:
            fn(c)
        except Exception as e:
            QMessageBox.information(c,"发生错误","错误信息"+repr(e)+"\n可能是没有启动游戏造成！")
    return wrapped
    

class AddBonusWidget(QGroupBox):
    """
        使用道具栏，点击对应按钮，触发对应的效果
    """

    def __init__(self, tanks):
        super(AddBonusWidget,self).__init__()
        self.Controller = Controller(tanks)

        self.setTitle("使用道具")
        self.Tanks = tanks

        self.MainLayout = QGridLayout()

        self.BonusTankButton = QPushButton(self)
        self.BonusTankButton.setText("生命道具")
        self.BonusTankButton.clicked.connect(self.triggerTankBonus)
        self.MainLayout.addWidget(self.BonusTankButton,0,0)

        self.BonusShovelButton = QPushButton(self)
        self.BonusShovelButton.setText("铁墙道具")
        self.BonusShovelButton.clicked.connect(self.triggerShovelBonus)
        self.MainLayout.addWidget(self.BonusShovelButton,0,1)

        self.BonusStarButton = QPushButton(self)
        self.BonusStarButton.setText("升级道具")
        self.BonusStarButton.clicked.connect(self.triggerStarBonus)
        self.MainLayout.addWidget(self.BonusStarButton,0,2)

        self.BonusTimerButton = QPushButton(self)
        self.BonusTimerButton.setText("停滞道具")
        self.BonusTimerButton.clicked.connect(self.triggerTimerBonus)
        self.MainLayout.addWidget(self.BonusTimerButton,1,0)

        self.BonusHelmetButton = QPushButton(self)
        self.BonusHelmetButton.setText("保护道具")
        self.BonusHelmetButton.clicked.connect(self.triggerHelmetBonus)
        self.MainLayout.addWidget(self.BonusHelmetButton,1,1)

        self.BonusBoomButton = QPushButton(self)
        self.BonusBoomButton.setText("炸弹道具")
        self.BonusBoomButton.clicked.connect(self.triggerBoomBonus)
        self.MainLayout.addWidget(self.BonusBoomButton,1,2)


        self.setLayout(self.MainLayout)
    
    @tips
    def triggerBoomBonus(self):
        """
            使用炸弹道具
        """
        self.Controller.triggerBoomBonus()
       

    @tips
    def triggerTankBonus(self):
        """
            使用加生命道具
        """
        self.Controller.triggerTankBonus()
    
    @tips
    def triggerShovelBonus(self):
        """
            使用铁牢道具
        """
        self.Controller.triggerShovelBonus()

    @tips
    def triggerStarBonus(self):
        """
            使用升级道具
        """
        self.Controller.triggerStarBonus()

    @tips
    def triggerTimerBonus(self):
        """
            使用暂停道具
        """
        self.Controller.triggerTimerBonus()

    @tips
    def triggerHelmetBonus(self):
        """
            使用盔甲道具
        """
        self.Controller.triggerHelmetBonus()
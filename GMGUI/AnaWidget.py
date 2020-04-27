# coding=utf-8

from PyQt5.QtWidgets import QWidget, QListWidget,QLabel,QVBoxLayout, QGridLayout, QPushButton,QFileDialog
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap,QColor


class AnaWidget(QWidget):
    """
        用于打开测试记录
    """

    def __init__(self,filename):
        super(AnaWidget,self).__init__()
        self.setWindowTitle("测试结果分析")
        
        self.MainLayout = QVBoxLayout()

        self.DirPath = filename.replace(".res","")

        self.ResultList = QListWidget()
        self.ResultList.currentRowChanged.connect(self.setResLabel)
        self.ResultLabel = QLabel("结果图片")
        self.ResultLabel.resize(200,200)

        self.TotalResLabel = QLabel("死亡x次   生成x个   错误x次")

        self.MainLayout.addWidget(self.ResultList)
        self.MainLayout.addWidget(self.TotalResLabel)
        self.MainLayout.addWidget(self.ResultLabel)

        f = open(filename)
        r = f.read()
        strlist = r.splitlines()

        sc = 0
        de = 0
        er = 0
        # 统计信息
        for s in strlist:
            if s.find("生成") >=0: sc =sc +1
            if s.find("死亡") >=0: de =de +1
            if s.find("!") >=0: er =er +1
            self.ResultList.addItem(s)
            if s.find("!") >=0:
                self.ResultList.item(self.ResultList.count()-1).setBackground(QColor('red'))
            

        self.ResultList.setCurrentRow(self.ResultList.count()-1)
        self.TotalResLabel.setText("死亡"+str(de)+"次   生成"+str(sc)+"个   错误"+str(er)+"次")
        

        self.setLayout(self.MainLayout)

    def setResLabel(self):
        """
            设置图片
        """
        if self.ResultList.currentRow() == -1:
            return
        self.ResultLabel.setPixmap(QPixmap(self.DirPath+str(self.ResultList.currentRow())+".png").scaled(self.ResultLabel.width(),self.ResultLabel.width()))

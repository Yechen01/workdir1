# coding=utf-8

#from PyQt5.QtWidgets import 
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QPushButton,QMessageBox,QFileDialog,QLabel,QHBoxLayout,QVBoxLayout,QGroupBox

from .Controller import Controller
import importlib,os,sys
import imp,threading,copy

def deleteItemsOfLayout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                deleteItemsOfLayout(item.layout())

class ControllerDataWidget(QGroupBox):
    """
        自动获取玩家信息窗口
    """

    def __init__(self,tanks):
        super(ControllerDataWidget,self).__init__()
        self.setTitle("任务列表")

        self.tanks = tanks

        self.MainLayout = QVBoxLayout()

        self.LoadButton = QPushButton("加载脚本")

        self.MainLayout.addStretch()
        self.MainLayout.addWidget(self.LoadButton)
        self.LoadButton.clicked.connect(self.loadScript)

        self.setLayout(self.MainLayout)


    def loadScript(self):

       # sys.path.append("./GMGUI/test_script")
        
        from GMGUI.test_scripts import example

        example = imp.reload(example)

        self.TaskList = example.TaskList(Controller(self.tanks))

        QMessageBox.information(None,"加载成功","加载了"+str(len(self.TaskList.TaskFunctionList))+"个脚本")

        deleteItemsOfLayout(self.MainLayout)

        
        
        for i in range(len(self.TaskList.TaskFunctionList)):
            
            taskbutton = QPushButton(self.TaskList.TaskFunctionList[i].__name__)
            self.MainLayout.addWidget(taskbutton)
            taskbutton.clicked.connect(self.sysnc(self.TaskList.TaskFunctionList[i]))
            

        self.MainLayout.addStretch()
        self.MainLayout.addWidget(self.LoadButton)

    def sysnc(self, myfunc):
        def my():
            t = threading.Thread(target=myfunc, args=())
            t.setDaemon(True)
            t.start()
        return my
        
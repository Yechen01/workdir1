# coding=utf-8

from PyQt5.QtWidgets import QGroupBox, QListWidget, QHBoxLayout, QVBoxLayout, QPushButton,QLabel
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap,QColor
import math
import random
import time
import datetime
import os


def isinrange(x,l,r):
        if x>=l and x <= r:
            return True
        else:
            return False


class AutoAIWidget(QGroupBox):
    """
        自动测试35关AI窗口
        
        如果游戏结束（没有生命或基地爆炸），则自动进入下一关

        如果正常通关，也会自动进入下一关

        游戏会一直进行，直到跑了35关后，自动暂停AI并记录测试记录

        逻辑与AIWidget.py类似，注释请看AIWidget.py

    """

    def __init__(self,tanks):
        super(AutoAIWidget,self).__init__()
        self.setTitle("自动测试35关")
        self.Tanks = tanks

        self.LastPos = [[0,0],[0,0]]

        self.IsActive = False
        self.IsGaming = False
        self.IsSingle = False
        self.IsWaiting = True

        self.Player1Life = 0
        self.Player2Life = 0
        self.EnermyCount = 0
        self.Player1Pos = [0,0,0]
        self.Player2Pos = [0,0,0]
        self.EnermyPos = []

        self.CurLevel = 0

        self.MainLayout = QVBoxLayout()

        self.ActiveLabel = QLabel("")

        self.StartAIButton = QPushButton("开始单人自动战斗")
        self.StartAIButton.clicked.connect(lambda: self.startAI(1))

        self.StartAIButton2 = QPushButton("开始双人自动战斗")
        self.StartAIButton2.clicked.connect(lambda: self.startAI(2))

        self.StopAIButton = QPushButton("停止自动战斗")
        self.StopAIButton.clicked.connect(self.stopAI)
        self.StopAIButton.setEnabled(False)
        

        self.ResultList = QListWidget()
        self.ResultList.currentRowChanged.connect(self.setResLabel)
        self.ResultLabel = QLabel("结果图片")

        self.TotalResLabel = QLabel("跑了x关   死亡x次\n生成x个   错误x次")
        self.DeathTime = 0
        self.EnermyTime = 0

        self.MainLayout.addWidget(self.ActiveLabel)

        self.MainLayout.addWidget(self.StartAIButton)
        self.MainLayout.addWidget(self.StartAIButton2)
        self.MainLayout.addWidget(self.StopAIButton)
        self.MainLayout.addWidget(self.ResultList)
        self.MainLayout.addWidget(self.TotalResLabel)
        self.MainLayout.addWidget(self.ResultLabel)

        self.StateTimer = QTimer()
        self.StateTimer.timeout.connect(self.getCurState)
        self.ErrorTimes = 0

        self.AITimer = QTimer()
        self.AITimer.timeout.connect(self.nextStep)
        self.AITimer.start(150)

        self.setLayout(self.MainLayout)

    def setResLabel(self):
        if self.ResultList.currentRow() == -1:
            return
        self.ResultLabel.setPixmap(QPixmap(self.DirPath+str(self.ResultList.currentRow())+".png").scaled(self.ResultLabel.width(),self.ResultLabel.width()))

    def addLog(self,msg):
        nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.ResultFile.write(nowtime+" "+msg+'\n')
        self.ResultFile.flush()
        self.Tanks.pygame.image.save(self.Tanks.screen, self.DirPath+str(self.ResultList.count())+".png")
        self.ResultLabel.setPixmap(QPixmap(self.DirPath+str(self.ResultList.count())+".png").scaled(self.ResultLabel.width(),self.ResultLabel.width()))

        self.ResultList.addItem(nowtime+" "+msg)
        self.ResultList.setCurrentRow(self.ResultList.count()-1)

        if msg.find("!") >=0:
            self.ErrorTimes = self.ErrorTimes + 1
            self.ResultList.item(self.ResultList.count()-1).setBackground(QColor('red'))
        if self.ErrorTimes < 300:
            self.TotalResLabel.setText("跑了"+str(self.Tanks.game.stage)+"关   死亡"+str(self.DeathTime)+"次\n生成"+str(self.EnermyTime)+"个   错误"+str(self.ErrorTimes)+"次")
        
        if self.ErrorTimes >= 300:
            self.ResultList.addItem(nowtime+" 多次错误，停止测试！")
            self.ResultFile.write(nowtime+" "+'多次错误，停止测试！'+'\n')
            self.ResultFile.flush()
            self.stopAI()

    def getCurState(self):
        if hasattr(self.Tanks.game, 'active'):
            if self.Tanks.game.active: 
                if self.IsGaming == False:
                    self.addLog("第"+str(self.Tanks.game.stage)+"关开始")

                self.IsGaming = True
                self.IsWaiting = False
                ll = len(self.Tanks.enemies)
                if ll > self.EnermyCount:
                    for _ in range(ll-self.EnermyCount):
                        self.EnermyTime = self.EnermyTime + 1
                        self.addLog("生成敌人")
                self.EnermyCount = ll

                for index in range(ll):
                    if index >= len(self.EnermyPos):
                        li = list(self.Tanks.enemies[index].rect.topleft)
                        li.append(0)
                        self.EnermyPos.append(li)
                    else: 
                        if self.EnermyPos[index][0] == self.Tanks.enemies[index].rect.topleft[0] and self.EnermyPos[index][1] == self.Tanks.enemies[index].rect.topleft[1]:
                            self.EnermyPos[index][2] = self.EnermyPos[index][2] + 1
                        else: 
                            self.EnermyPos[index][2] = 0

                            self.EnermyPos[index][0] = self.Tanks.enemies[index].rect.topleft[0] 
                            self.EnermyPos[index][1] = self.Tanks.enemies[index].rect.topleft[1]

                for index in range(ll):
                    if self.EnermyPos[index][2] >= 110:
                        self.EnermyPos[index][2] = 0
                        self.addLog("敌人卡住了!")
                
                

                num = len(self.Tanks.players)
                if num is 1:
                    if self.Tanks.players[0].lives < self.Player1Life:
                        self.DeathTime = self.DeathTime + 1
                        self.addLog("玩家1死亡")
                    self.Player1Life = self.Tanks.players[0].lives

                    if self.Tanks.players[0].rect.topleft[0] == self.Player1Pos[0] and self.Tanks.players[0].rect.topleft[1] == self.Player1Pos[1]:
                        self.Player1Pos[2] = self.Player1Pos[2] + 1
                    else: 
                        self.Player1Pos[2] = 1
                    
                    self.Player1Pos[0] = self.Tanks.players[0].rect.topleft[0]
                    self.Player1Pos[1] = self.Tanks.players[0].rect.topleft[1]
                    
                    if self.Player1Pos[2] >= 50:
                        self.addLog("玩家1卡住了!")
                        self.Player1Pos[2] = 1

                    self.IsSingle = True
                    self.ActiveLabel.setText("单人游戏中")
                else:
                    if self.Tanks.players[0].lives < self.Player1Life:
                        self.DeathTime = self.DeathTime + 1
                        self.addLog("玩家1死亡")
                    if self.Tanks.players[1].lives < self.Player2Life:
                        self.DeathTime = self.DeathTime + 1
                        self.addLog("玩家2死亡")
                    self.Player1Life = self.Tanks.players[0].lives
                    self.Player2Life = self.Tanks.players[1].lives

                    if self.Tanks.players[0].rect.topleft[0] == self.Player1Pos[0] and self.Tanks.players[0].rect.topleft[1] == self.Player1Pos[1]:
                        self.Player1Pos[2] = self.Player1Pos[2] + 1
                    else: 
                        self.Player1Pos[2] = 1
                    
                    self.Player1Pos[0] = self.Tanks.players[0].rect.topleft[0]
                    self.Player1Pos[1] = self.Tanks.players[0].rect.topleft[1]
                    
                    if self.Player1Pos[2] >= 50:
                        self.addLog("玩家1卡住了!")
                        self.Player1Pos[2] = 1

                    if self.Tanks.players[1].rect.topleft[0] == self.Player2Pos[0] and self.Tanks.players[1].rect.topleft[1] == self.Player2Pos[1]:
                        self.Player2Pos[2] = self.Player2Pos[2] + 1
                    else: 
                        self.Player2Pos[2] = 1
                    
                    self.Player2Pos[0] = self.Tanks.players[1].rect.topleft[0]
                    self.Player2Pos[1] = self.Tanks.players[1].rect.topleft[1]
                    
                    if self.Player2Pos[2] >= 50:
                        self.addLog("玩家2卡住了!")
                        self.Player2Pos[2] = 1

                    self.IsSingle = False
                    self.ActiveLabel.setText("双人游戏中")
            else:
                if self.IsGaming:
                    self.CurLevel = self.CurLevel + 1
                if self.IsGaming:
                    self.addLog("第"+str(self.Tanks.game.stage)+"关结束")
                if self.Tanks.game.stage == 35:
                    self.addLog("成功通过35关！")
                    self.stopAI()
                    return

                self.IsGaming = False
                self.ActiveLabel.setText("等待游戏")
        else:
            self.IsWaiting = True
            self.IsGaming = False
            self.ActiveLabel.setText("等待界面")
        
        if hasattr(self.Tanks.game, 'game_over') and self.Tanks.game.game_over:
            
            self.IsWaiting = True
            if self.IsGaming:
                if self.Tanks.game.stage == 35:
                    self.addLog("成功通过35关！")
                    self.stopAI()
                    return
                self.addLog("游戏结束")
                self.IsGaming = False
                self.CurLevel = self.CurLevel + 1
                self.ActiveLabel.setText("游戏结束")
                time.sleep(15)
                event = self.Tanks.pygame.event.Event(self.Tanks.pygame.KEYDOWN,{'key':self.Tanks.pygame.K_RETURN})
                self.Tanks.pygame.event.post(event)
                time.sleep(7)
                self.Tanks.game.stage = self.CurLevel
                self.Tanks.game.nr_of_players = self.PlayerCount
                event = self.Tanks.pygame.event.Event(self.Tanks.pygame.KEYDOWN,{'key':self.Tanks.pygame.K_RETURN})
                self.Tanks.pygame.event.post(event)
                time.sleep(5)


    def startAI(self, count):
        if self.IsActive:
            return
        self.ResultList.clear()
        path = datetime.datetime.now().strftime('%Y%m%d%H%M%S')+"_AutoAI"
        os.makedirs("./TestResult/"+path)
        self.DirPath = "./TestResult/"+path+"/screen"
        self.ResultFile = open(self.DirPath+".res","w")

        self.addLog("开始测试")
        
        self.ErrorTimes = 0

        self.getCurState()
        self.PlayerCount = count
        self.StateTimer.start(100)
        if self.IsWaiting:
            self.Tanks.game.stage = self.CurLevel
            self.Tanks.game.nr_of_players = count
            event = self.Tanks.pygame.event.Event(self.Tanks.pygame.KEYDOWN,{'key':self.Tanks.pygame.K_RETURN})
            self.Tanks.pygame.event.post(event)

        self.Tanks.game.game_over = False
        self.IsActive = True

    def stopAI(self):
        if self.IsActive == False:
            return
        for player in self.Tanks.players:
            self.stopMove(player)

        self.IsActive = False
        self.addLog("停止测试")
        self.ResultFile.close()
        self.StateTimer.stop()
    
    def canFireUp(self,player):
        playerpos = player.rect.topleft
        for ene in self.Tanks.enemies:
            fire = False
            rect = ene.rect.topleft
            if isinrange(rect[0]+16,playerpos[0]+4,playerpos[0]+28) and rect[1]<playerpos[1]:
                fire = True
                for tile in self.Tanks.game.level.mapr:
                    if tile.type == self.Tanks.game.level.TILE_STEEL:
                        if isinrange(tile.topleft[1],rect[1],playerpos[1]) and isinrange(tile.topleft[0]+10,playerpos[0]+15,playerpos[0]+35):
                            fire = False
            if fire:
                return fire
        return False  

    def canFireDown(self,player):
        playerpos = player.rect.topleft
        if playerpos[1] < 340 and isinrange(playerpos[0],180,215):
            return False
        for ene in self.Tanks.enemies:
            fire = False
            rect = ene.rect.topleft
            if isinrange(rect[0]+16,playerpos[0]+4,playerpos[0]+28) and rect[1]>playerpos[1]:
                fire = True
                for tile in self.Tanks.game.level.mapr:
                    if tile.type == self.Tanks.game.level.TILE_STEEL:
                        if isinrange(tile.topleft[1],playerpos[1],rect[1]) and isinrange(tile.topleft[0]+10,playerpos[0]+15,playerpos[0]+35):
                            fire = False
            if fire:
                return fire
        return False 

    def canFireRight(self,player):
        playerpos = player.rect.topleft
        if playerpos[0] < 241 and isinrange(playerpos[1],389,400):
            return False
        for ene in self.Tanks.enemies:
            fire = False
            rect = ene.rect.topleft
            if isinrange(rect[1]+16,playerpos[1]+4,playerpos[1]+28) and rect[0]>playerpos[0]:
                fire = True
                for tile in self.Tanks.game.level.mapr:
                    if tile.type == self.Tanks.game.level.TILE_STEEL:
                        if isinrange(tile.topleft[0],playerpos[0],rect[0]) and isinrange(tile.topleft[1]+10,playerpos[1]+15,playerpos[1]+35):
                            fire = False
            if fire:
                return fire
        return False

    def canFireLeft(self,player):
        playerpos = player.rect.topleft
        if playerpos[0] > 241 and isinrange(playerpos[1],389,400):
            return False
        for ene in self.Tanks.enemies:
            fire = False
            rect = ene.rect.topleft
            if isinrange(rect[1]+16,playerpos[1]+4,playerpos[1]+28) and rect[0]<playerpos[0]:
                fire = True
                for tile in self.Tanks.game.level.mapr:
                    if tile.type == self.Tanks.game.level.TILE_STEEL:
                        if isinrange(tile.topleft[0],rect[0],playerpos[0]) and isinrange(tile.topleft[1]+10,playerpos[1]+15,playerpos[1]+35):
                            fire = False
            if fire:
                return fire
        return False
    
    def stopMove(self,player):
        for j in range(4): 
            player.pressed[j] = False

    def goUp(self,player):
        if player.state != player.STATE_ALIVE: return
        self.stopMove(player)
        player.pressed[0]= not player.pressed[0]

    def goLeft(self,player):
        if player.state != player.STATE_ALIVE: return
        self.stopMove(player)
        player.pressed[3]=not player.pressed[3]

    def goRight(self,player):
        if player.state != player.STATE_ALIVE: return
        self.stopMove(player)
        player.pressed[1]=not player.pressed[1]

    def goDown(self,player):
        if player.state != player.STATE_ALIVE: return
        self.stopMove(player)
        player.pressed[2]=not player.pressed[2]
    

    def checkFire(self):
        fired = []
        for player in self.Tanks.players:
            if player.state == player.STATE_ALIVE:
                if player.direction == player.DIR_UP and self.canFireUp(player):
                    player.fire()
                    fired.append(player)
                elif player.direction == player.DIR_DOWN and self.canFireDown(player):
                    player.fire()
                    fired.append(player)
                elif player.direction == player.DIR_RIGHT and self.canFireRight(player):
                    player.fire()
                    fired.append(player)
                elif player.direction == player.DIR_LEFT and self.canFireLeft(player):
                    player.fire()
                    fired.append(player)
        return fired

    
    def move(self):
        pi = 0
        for player in self.Tanks.players:
            if self.canFireUp(player) and player.direction is not player.DIR_UP: self.goUp(player)
            elif self.canFireDown(player) and player.direction is not player.DIR_DOWN: self.goDown(player)
            elif self.canFireLeft(player) and player.direction is not player.DIR_LEFT: self.goLeft(player)
            elif self.canFireRight(player) and player.direction is not player.DIR_RIGHT: self.goRight(player)
            else:
                if self.LastPos[pi][0] == player.rect.topleft[0]  and self.LastPos[pi][1] == player.rect.topleft[1]:
                    cur = 10000000
                    er = ()
                    pr = player.rect.topleft
                    for ene in self.Tanks.enemies:
                        dis = math.sqrt(abs(ene.rect.topleft[0]-player.rect.topleft[0])*abs(ene.rect.topleft[0]-player.rect.topleft[0])+abs(ene.rect.topleft[1]-player.rect.topleft[1])*abs(ene.rect.topleft[1]-player.rect.topleft[1]))  
                        if dis < cur:
                            cur = dis
                            er = ene.rect.topleft

                    if cur == 10000000:
                        if player.direction == player.DIR_UP: self.goUp(player)
                        if player.direction == player.DIR_DOWN: self.goDown(player)
                        if player.direction == player.DIR_LEFT: self.goLeft(player)
                        if player.direction == player.DIR_RIGHT: self.goRight(player)
                    else:
                        if er[0] <= pr[0] and er[1] <= pr[1]: 
                            if random.randint(1,2)==1:
                                if player.direction == player.DIR_LEFT: self.goUp(player)
                                elif player.direction == player.DIR_UP: self.goRight(player)
                                elif player.direction == player.DIR_RIGHT: self.goDown(player)
                                else: self.goLeft(player)
                            else:
                                if player.direction == player.DIR_UP: self.goLeft(player)
                                elif player.direction == player.DIR_LEFT: self.goDown(player)
                                elif player.direction == player.DIR_DOWN: self.goRight(player)
                                else: self.goUp(player)
                        elif er[0] > pr[0] and er[1] <= pr[1]: 
                            if random.randint(1,2)==1:
                                if player.direction == player.DIR_RIGHT: self.goUp(player)
                                elif player.direction == player.DIR_UP: self.goLeft(player)
                                elif player.direction == player.DIR_LEFT: self.goDown(player)
                                else: self.goRight(player)
                            else:
                                if player.direction == player.DIR_UP: self.goRight(player)
                                elif player.direction == player.DIR_RIGHT: self.goDown(player)
                                elif player.direction == player.DIR_DOWN: self.goLeft(player)
                                else: self.goUp(player)
                        elif er[0] > pr[0] and er[1] > pr[1]: 
                            if random.randint(1,2)==1:
                                if player.direction == player.DIR_DOWN: self.goRight(player)
                                elif player.direction == player.DIR_RIGHT: self.goUp(player)
                                elif player.direction == player.DIR_UP: self.goLeft(player)
                                else: self.goDown(player)
                            else:
                                if player.direction == player.DIR_RIGHT: self.goDown(player)
                                elif player.direction == player.DIR_DOWN: self.goLeft(player)
                                elif player.direction == player.DIR_LEFT: self.goUp(player)
                                else: self.goRight(player)
                        elif er[0] <= pr[0] and er[1] > pr[1]: 
                            if random.randint(1,2)==1:
                                if player.direction == player.DIR_LEFT: self.goDown(player)
                                elif player.direction == player.DIR_DOWN: self.goRight(player)
                                elif player.direction == player.DIR_RIGHT: self.goUp(player)
                                else: self.goLeft(player)
                            else:
                                if player.direction == player.DIR_DOWN: self.goLeft(player)
                                elif player.direction == player.DIR_LEFT: self.goUp(player)
                                elif player.direction == player.DIR_UP: self.goRight(player)
                                else: self.goDown(player)
                
            self.LastPos[pi][0] = player.rect.topleft[0]
            self.LastPos[pi][1] = player.rect.topleft[1]
            pi = pi + 1        

    def nextStep(self):
        if self.IsActive is False: return
        if self.IsGaming is False: return
        
        self.checkFire()
        self.move()
        

        


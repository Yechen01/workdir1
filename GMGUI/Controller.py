# coding=utf-8

import time


def isInRange(x, l, r):
	if x >= l and x <= r:
		return True
	else:
		return False


def distance(a, b):
	'''
	计算 a b两个点的距离
	:param a: 二元元组（x,y）
	:param b: 二元元组（x,y）
	:return:
	'''
	return ((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1])) ** 0.5


class Controller(object):
	"""
	所有GM指令汇总
	"""

	def __init__(self, tanks):

		self.Tanks = tanks

		self.TILE_EMPTY = 0
		self.TILE_BRICK = 1
		self.TILE_STEEL = 2
		self.TILE_WATER = 3
		self.TILE_GRASS = 4
		self.TILE_FROZE = 5

		self.UP = 0
		self.RIGHT = 1
		self.DOWN = 2
		self.LEFT = 3

		self._RunningGameOver = False

	def triggerTankBonus(self):
		"""
		使用加生命道具
		:return: 无
		"""
		b = self.Tanks.Bonus(self.Tanks.game.level)
		b.toggleVisibility()
		b.bonus = b.BONUS_TANK
		for player in self.Tanks.players:
			self.Tanks.bonuses.append(b)
			self.Tanks.game.triggerBonus(b, player)

	def triggerBoomBonus(self):
		"""
		使用炸弹道具
		:return: 无
		"""
		b = self.Tanks.Bonus(self.Tanks.game.level)
		b.toggleVisibility()
		b.bonus = b.BONUS_GRENADE
		for player in self.Tanks.players:
			self.Tanks.bonuses.append(b)
			self.Tanks.game.triggerBonus(b, player)

	def triggerShovelBonus(self):
		"""
		使用铁牢道具
		:return: 无
		"""
		b = self.Tanks.Bonus(self.Tanks.game.level)
		b.toggleVisibility()
		b.bonus = b.BONUS_SHOVEL
		for player in self.Tanks.players:
			self.Tanks.bonuses.append(b)
			self.Tanks.game.triggerBonus(b, player)

	def triggerStarBonus(self):
		"""
		使用升级道具
		:return: 无
		"""
		b = self.Tanks.Bonus(self.Tanks.game.level)
		b.toggleVisibility()
		b.bonus = b.BONUS_STAR
		for player in self.Tanks.players:
			self.Tanks.bonuses.append(b)
			self.Tanks.game.triggerBonus(b, player)

	def triggerTimerBonus(self):
		"""
		使用暂停道具
		:return: 无
		"""
		b = self.Tanks.Bonus(self.Tanks.game.level)
		b.toggleVisibility()
		b.bonus = b.BONUS_TIMER
		for player in self.Tanks.players:
			self.Tanks.bonuses.append(b)
			self.Tanks.game.triggerBonus(b, player)

	def triggerHelmetBonus(self):
		"""
		使用盔甲道具
		:return: 无
		"""
		b = self.Tanks.Bonus(self.Tanks.game.level)
		b.toggleVisibility()
		b.bonus = b.BONUS_HELMET
		for player in self.Tanks.players:
			self.Tanks.bonuses.append(b)
			self.Tanks.game.triggerBonus(b, player)

	def addTank(self):
		self.Tanks.enemies.append(self.Tanks.Enemy(self.Tanks.game.level, 1))

	def nextLevel(self):
		self.Tanks.game.finishLevel()

	def reloadPlayer(self):
		self.Tanks.game.reloadPlayers()

	def player1Fire(self):
		self.Tanks.players[0].fire()

	def player1GoUp(self):
		"""
			玩家1不停地向上走，再次触发，暂停向上走
		"""
		if self.Tanks.players == None or len(self.Tanks.players) < 1:
			return

		player = self.Tanks.players[0]
		d = self.UP
		for j in [self.UP, self.DOWN, self.LEFT, self.RIGHT]:
			if j != d:
				player.pressed[j] = False
		player.pressed[d] = not player.pressed[d]

	def player1GoLeft(self):
		"""
			玩家1不停地向上走，再次触发，暂停向上走
		"""
		if self.Tanks.players == None or len(self.Tanks.players) < 1:
			return

		player = self.Tanks.players[0]
		d = self.LEFT
		for j in [self.UP, self.DOWN, self.LEFT, self.RIGHT]:
			if j != d:
				player.pressed[j] = False
		player.pressed[d] = not player.pressed[d]

	def player1GoRight(self):
		"""
			玩家1不停地向上走，再次触发，暂停向上走
		"""
		if self.Tanks.players == None or len(self.Tanks.players) < 1:
			return

		player = self.Tanks.players[0]
		d = self.RIGHT
		for j in [self.UP, self.DOWN, self.LEFT, self.RIGHT]:
			if j != d:
				player.pressed[j] = False
		player.pressed[d] = not player.pressed[d]

	def player1GoDown(self):
		"""
			玩家1不停地向上走，再次触发，暂停向上走
		"""
		if self.Tanks.players == None or len(self.Tanks.players) < 1:
			return

		player = self.Tanks.players[0]
		d = self.DOWN
		for j in [self.UP, self.DOWN, self.LEFT, self.RIGHT]:
			if j != d:
				player.pressed[j] = False
		player.pressed[d] = not player.pressed[d]

	def player2Fire(self):
		"""
			玩家1开火
		"""
		self.Tanks.players[1].fire()

	def player2GoUp(self):
		if self.Tanks.players == None or len(self.Tanks.players) < 1:
			return

		player = self.Tanks.players[1]
		d = self.UP
		for j in [self.UP, self.DOWN, self.LEFT, self.RIGHT]:
			if j != d:
				player.pressed[j] = False
		player.pressed[d] = not player.pressed[d]

	def player2GoLeft(self):
		if self.Tanks.players == None or len(self.Tanks.players) < 1:
			return

		player = self.Tanks.players[1]
		d = self.LEFT
		for j in [self.UP, self.DOWN, self.LEFT, self.RIGHT]:
			if j != d:
				player.pressed[j] = False
		player.pressed[d] = not player.pressed[d]

	def player2GoRight(self):
		if self.Tanks.players == None or len(self.Tanks.players) < 1:
			return

		player = self.Tanks.players[1]
		d = self.RIGHT
		for j in [self.UP, self.DOWN, self.LEFT, self.RIGHT]:
			if j != d:
				player.pressed[j] = False
		player.pressed[d] = not player.pressed[d]

	def player2GoDown(self):
		if self.Tanks.players == None or len(self.Tanks.players) < 1:
			return

		player = self.Tanks.players[1]
		d = self.DOWN
		for j in [self.UP, self.DOWN, self.LEFT, self.RIGHT]:
			if j != d:
				player.pressed[j] = False
		player.pressed[d] = not player.pressed[d]

	def stopMove(self, player):
		for j in range(4):
			self.Tanks.players[player].pressed[j] = False

	def getPlayerTopLeft(self, player):
		"""
		返回玩家左上的坐标
		:param：player，0为玩家1，1为玩家2
		:return：tuple 坐标
		"""
		pass

	def getPlayerScore(self, player):
		"""
		返回玩家分数
		:param player: player，0为玩家1，1为玩家2
		:return: int 分数
		"""
		pass

	def getPlayerLives(self, player):
		"""
		返回玩家生命值
		:param ：player，0为玩家1，1为玩家2
		:return：int 生命值
		"""
		pass

	def setPlayerLives(self, player, live):
		"""
		设置玩家生命值
		:param:player，0为玩家1，1为玩家2
		:param:live，生命值
		"""
		self.Tanks.players[player].lives = live

	def getEnemyList(self):
		"""
		返回当前地方坦克列表
		:param：无
		:return：list 其中list的内容为二元tuple，
			第一维为坦克类型(基础坦克，快速坦克，升级坦克，厚血坦克)，
			第二维为坦克左上角的坐标
			如：[("基础坦克",(0,0)),("快速坦克",(100,100)),("厚血坦克",(200,200))]
		"""
		pass

	def isActive(self):
		return self.Tanks.game.active

	def buildFortress(self):
		"""
		生成铁囚笼
		"""
		if self.isActive():
			self.Tanks.game.level.buildFortress(self.Tanks.game.level.TILE_STEEL)  # 生成铁囚笼

	def getNearestBrick(self, pt, dir, brick_type, eps=-4):
		"""
		获取距离某个坐标某个方向最近的砖块坐标
		:param：pt 当前位置 (一个二元tuple代表位置)
		:param：dir 哪个方向 (0,1,2,3分别代表上下左右)
		:param：brick_type 最近的哪种类型砖块(共6种，详见__init__)
		:param：eps 精度控制
		:return：tuple 代表距离最近的方块的坐标
		"""

		pt = [pt[0], pt[1]]

		yu = pt[0] % 16
		if yu < 8:
			pt[0] = pt[0] - yu
		else:
			pt[0] = pt[0] + 16 - yu

		yu = pt[1] % 16
		if yu < 8:
			pt[1] = pt[1] - yu
		else:
			pt[1] = pt[1] + 16 - yu

		dis = 1000000000
		res = None
		for tile in self.Tanks.game.level.mapr:
			if tile.type == brick_type:
				if dir == self.UP:
					if isInRange(tile.topleft[1], 0, pt[1]) and (
							isInRange(tile.topleft[0], pt[0] - eps, pt[0] + 32 + eps) or isInRange(
						tile.topleft[0] + 16 + eps, pt[0] - eps, pt[0] + 32 + eps)):
						if distance(tile.topleft, pt) < dis:
							dis = distance(tile.topleft, pt)
							res = tile.topleft
				elif dir == self.DOWN:
					if isInRange(tile.topleft[1], pt[1] + 32 + eps, 1000) and (
							isInRange(tile.topleft[0], pt[0] - eps, pt[0] + 32 + eps) or isInRange(
						tile.topleft[0] + 16 + eps, pt[0] - eps, pt[0] + 32 + eps)):
						if distance(tile.topleft, pt) < dis:
							dis = distance(tile.topleft, pt)
							res = tile.topleft
				elif dir == self.LEFT:
					if isInRange(tile.topleft[0], 0, pt[0]) and (
							isInRange(tile.topleft[1], pt[1] - eps, pt[1] + 32 + eps) or isInRange(
						tile.topleft[1] + 16 + eps, pt[1] - eps, pt[1] + 32 + eps)):
						if distance(tile.topleft, pt) < dis:
							dis = distance(tile.topleft, pt)
							res = tile.topleft

				elif dir == self.RIGHT:
					if isInRange(tile.topleft[0], pt[0] + 32 + eps, 1000) and (
							isInRange(tile.topleft[1], pt[1] - eps, pt[1] + 32 + eps) or isInRange(
						tile.topleft[1] + 16 + eps, pt[1] - eps, pt[1] + 32 + eps)):
						if distance(tile.topleft, pt) < dis:
							dis = distance(tile.topleft, pt)
							res = tile.topleft
		return res

	def isInMenu(self):
		return self.Tanks.game.is_in_menu

	def isInGameOver(self):
		return self.Tanks.game.is_in_game_over_menu

	def getCurStage(self):
		return self.Tanks.game.stage

	def gameOver(self):
		'''
		强行结束当前游戏局
		:return: 无
		'''
		if self.isInMenu() == False:
			if self._RunningGameOver == False:
				self._RunningGameOver = True
				self.Tanks.game.gameOver()
				while self.isInGameOver() == False:
					time.sleep(1)
				event = self.Tanks.pygame.event.Event(self.Tanks.pygame.KEYDOWN, {'key': self.Tanks.pygame.K_RETURN})
				self.Tanks.pygame.event.post(event)
				self._RunningGameOver = False
				while self.isInMenu() == False:
					time.sleep(1)

	def startGame(self, num=1):
		'''
		开启单人/双人游戏局
		:param num: 默认是1，代表单人局；2，代表双人局
		:return: 无
		'''
		if num not in [1, 2]:
			return
		self.Tanks.game.nr_of_players = num
		event = self.Tanks.pygame.event.Event(self.Tanks.pygame.KEYDOWN, {'key': self.Tanks.pygame.K_RETURN})
		self.Tanks.pygame.event.post(event)
		time.sleep(1)  # 等待进入游戏

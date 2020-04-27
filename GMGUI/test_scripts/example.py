import threading
import time


class TaskList(object):

	def __init__(self, controller):
		self.Controller = controller
		self.TaskFunctionList = []
		self.addTaskFunction(self.task_example)

	def addTaskFunction(self, func):
		self.TaskFunctionList.append(func)

	def task_example(self):
		self.Controller.gameOver()
		self.Controller.startGame(2)
		self.Controller.player1GoUp()
		time.sleep(2)

from matplotlib import pyplot as plt
import numpy as np
import csv
import defines
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import imageio


# Grid colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 204)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
# Node types
EMPTY = 'E'
START = 'S'
SHELF = 'X'
GOAL = 'G'
UP = 'U'
DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'

DEBUG = False


def oppositeMove(moveA, moveB):
	test1 = (moveA == DOWN and moveB == UP)
	test2 = (moveA == UP and moveB == DOWN)
	test3 = (moveA == LEFT and moveB == RIGHT)
	test4 = (moveA == RIGHT and moveB == LEFT)
	return test1 or test2 or test3 or test4


def emptyTypeNode(nodeType):
	return nodeType == UP or nodeType == DOWN or nodeType == LEFT or nodeType == RIGHT


class Node(object):
	def __init__(self, id):
		self.id = id
		self.neighbors = []
		self.type = None
		self.occupied = False


class WHMap:
	# Class constructor
	def __init__(self):
		results = []
		# Read map from .csv
		with open(defines.FILE) as csvfile:
			reader = csv.reader(csvfile)  # change contents to floats
			for row in reader:  # each row is a list
				results.append(row)
		self.rows = len(results)
		self.columns = len(results[0])
		self.startNodes = []
		self.goalNodes = []
		self.targetNodes = []
		self.topNodes = []
		self.bottomNodes = []
		self.leftNodes = []
		self.rightNodes = []
		self.oneWayMap = False
		self.filenames = []
		self.counter = 0
		self.largestRobotIndex = 1

		# Initialize game board
		self.board = self.initBoard(self.rows, self.columns)

		# Create node map
		self.nodeMap = [None] * self.rows * self.columns
		for r in range(0, self.rows):
			for c in range(0, self.columns):
				# Set node ID
				id = r * self.columns + c
				node = Node(id)
				# Set node type
				node.type = results[r][c]
				if node.type == UP or node.type == DOWN or node.type == LEFT or node.type == RIGHT:
					self.oneWayMap = True
				# Add node to list
				self.nodeMap[id] = node
				# Check if this is a start node
				if node.type == START:
					# Add node to start node list
					self.startNodes.append(id)
				# Check if this is a goal node
				if node.type == GOAL:
					# Add node to goal node list
					self.goalNodes.append(id)
		# If using one-ways map, create special neighbors list
		if self.oneWayMap:
			for r in range(0, self.rows):
				for c in range(0, self.columns):
					id = r * self.columns + c
					# Verify this isn't a shelf
					if not self.nodeMap[id].type == SHELF:
						# Check each neighbor
						if r - 1 >= 0:
							ngID = (r-1) * self.columns + c
							if not self.nodeMap[ngID].type == SHELF and not self.nodeMap[ngID].type == DOWN and \
									not self.nodeMap[id].type == DOWN and \
									not oppositeMove(self.nodeMap[id].type, self.nodeMap[ngID].type):
								self.nodeMap[id].neighbors.append(ngID)
						if c + 1 < self.columns:
							ngID = r * self.columns + (c+1)
							if not self.nodeMap[ngID].type == SHELF and not self.nodeMap[ngID].type == LEFT and \
									not self.nodeMap[id].type == LEFT and \
									not oppositeMove(self.nodeMap[id].type, self.nodeMap[ngID].type):
								self.nodeMap[id].neighbors.append(ngID)
							elif emptyTypeNode(self.nodeMap[id].type):
								self.targetNodes.append(id)
						if r + 1 < self.rows:
							ngID = (r+1) * self.columns + c
							if not self.nodeMap[ngID].type == SHELF and not self.nodeMap[ngID].type == UP and \
									not self.nodeMap[id].type == UP and \
									not oppositeMove(self.nodeMap[id].type, self.nodeMap[ngID].type):
								self.nodeMap[id].neighbors.append(ngID)
						if c - 1 >= 0:
							ngID = r * self.columns + (c-1)
							if not self.nodeMap[ngID].type == SHELF and not self.nodeMap[ngID].type == RIGHT and \
									not self.nodeMap[id].type == RIGHT and \
									not oppositeMove(self.nodeMap[id].type, self.nodeMap[ngID].type):
								self.nodeMap[id].neighbors.append(ngID)
							elif emptyTypeNode(self.nodeMap[id].type):
								self.targetNodes.append(id)
						# Check if this is a good node to return to when stuck
						if r == 0:
							self.topNodes.append(id)
						if r == self.rows - 1:
							self.bottomNodes.append(id)
						if c == 0:
							self.leftNodes.append(id)
						if c == self.columns - 1:
							self.rightNodes.append(id)
		else:
			# Create regular neighbors list for each node
			for r in range(0, self.rows):
				for c in range(0, self.columns):
					id = r * self.columns + c
					# Verify this isn't a shelf
					if not self.nodeMap[id].type == SHELF:
						# Check each neighbor
						if r - 1 >= 0:
							ngID = (r-1) * self.columns + c
							if not self.nodeMap[ngID].type == SHELF:
								self.nodeMap[id].neighbors.append(ngID)
						if c + 1 < self.columns:
							ngID = r * self.columns + (c+1)
							if not self.nodeMap[ngID].type == SHELF:
								self.nodeMap[id].neighbors.append(ngID)
							elif self.nodeMap[id].type == EMPTY:
								self.targetNodes.append(id)
						if r + 1 < self.rows:
							ngID = (r+1) * self.columns + c
							if not self.nodeMap[ngID].type == SHELF:
								self.nodeMap[id].neighbors.append(ngID)
						if c - 1 >= 0:
							ngID = r * self.columns + (c-1)
							if not self.nodeMap[ngID].type == SHELF:
								self.nodeMap[id].neighbors.append(ngID)
							elif self.nodeMap[id].type == EMPTY:
								self.targetNodes.append(id)
						# Check if this is a good node to return to when stuck
						if r == 0:
							self.topNodes.append(id)
						if r == self.rows - 1:
							self.bottomNodes.append(id)
						if c == 0:
							self.leftNodes.append(id)
						if c == self.columns - 1:
							self.rightNodes.append(id)
		# Sanity prints
		if DEBUG:
			for n in self.nodeMap:
				print(n.id, " : ", n.neighbors)

	def idToRC(self, id):
		r = id // self.columns
		c = id - (self.columns * r)
		return r, c

	def updateMap(self, agentQueue):
		# Create current warehouse map
		whMap = []
		for r in range(0, self.rows):
			row = []
			for c in range(0, self.columns):
				# Determine what color this node should be
				id = r * self.columns + c
				if self.nodeMap[id].type == EMPTY or self.nodeMap[id].type == UP or self.nodeMap[id].type == DOWN or \
						self.nodeMap[id].type == LEFT or self.nodeMap[id].type == RIGHT:
					row.append(WHITE)
				elif self.nodeMap[id].type == SHELF:
					row.append(BLACK)
				elif self.nodeMap[id].type == START:
					row.append(BLUE)
				elif self.nodeMap[id].type == GOAL:
					row.append(YELLOW)
				else:
					print("No color detected")
			whMap.append(row)
			
			
		self.updateBoard(whMap, self.rows, self.columns, agentQueue)



	def initBoard(self, numRows, numColumns):
		# initialize board
		self.img = plt.figure(figsize=[10, 10])
		self.img.patch.set_facecolor((1, 1, 1))
		board = self.img.add_subplot(111)

		return board


	def updateBoard(self, whMap, numRows, numColumns, agentQueue):
		artists = [[None]*numColumns]*numRows
		self.board.clear()

		# draw grid on board
		for x in range(numColumns+1):
			self.board.plot([x, x], [0, numRows], 'k')

		for y in range(numRows+1):
			self.board.plot([0, numColumns], [y, y], 'k')

		# turn board axis off
		self.board.set_axis_off()

		# scale board to fit in window
		self.board.set_xlim(0, numColumns)
		self.board.set_ylim(0, numRows)

		for x in range(numRows):
			for y in range(numColumns):
				tileColorUnscaled = whMap[x][y]
				tileColor = tuple(ti/255 for ti in tileColorUnscaled)

				# print("TILE COLOR" + str(tileColor))
				artists[x][y] = mpatches.Rectangle((y, (numRows-1)-x), 1, 1, color=tileColor)
				
				self.board.add_artist(artists[x][y])

		if len(agentQueue) > 0:
			lowIndex = agentQueue[0].ID
			highIndex = agentQueue[len(agentQueue) - 1].ID
			length = max(highIndex - lowIndex, 1)
		else:
			lowIndex = 0
			highIndex = 0
			length = 1

		# Add robots to map
		for agent in agentQueue:
			

			R, C = self.idToRC(agent.nodeLocationID)

			# Set color
			robotColor = ((agent.ID - lowIndex) / length, 0.3, 1 - (agent.ID - lowIndex) / length)
			# print("Robot ID: " + str(agent.ID) + ", Robot color: " + str(robotColor))
			
			# Draw robot to board
			self.board.add_artist(mpatches.Circle((C + 0.5, (numRows-1)-R + 0.5), radius=0.3, color=(1,0,0)))

			# Add robot ID number to circle
			self.board.add_artist(plt.text(C + 0.4, (numRows-1)-R + 0.4, str(agent.ID), color=(1,1,1)))

		plt.pause(0.1)
		
		if defines.MAKE_GIF:
			# Record file
			fileName = f'img/{self.counter}.png'
			self.filenames.append(fileName)
			# Save frame
			plt.savefig(fileName)
			plt.close()
			self.counter = self.counter + 1


	def printGIF(self):
		if defines.MAKE_GIF:
			with imageio.get_writer('mygif.gif', mode='I') as writer:
				for filename in self.filenames:
					image = imageio.imread(filename)
					writer.append_data(image)
			# Remove files
			for filename in set(self.filenames):
				os.remove(filename)

	def biDir_BFS(self, startID, endID, ignoreOccupied=False):
		# print("Find path: ", startID, endID)
		root = [None] * self.rows * self.columns
		for r in range(0, len(root)):
			root[r] = -1

		queue = []
		root[startID] = startID
		queue.append(startID)

		while queue:
			n = queue.pop(0)
			# print(n, ":")

			for nbr in self.nodeMap[n].neighbors:
				# print(nbr, end=" ")
				if root[nbr] == -1:
					if ignoreOccupied:
						if not self.nodeMap[nbr].occupied:
							root[nbr] = n
							queue.append(nbr)
					else:
						root[nbr] = n
						queue.append(nbr)
					if nbr == endID:
						# Found node!
						# print("Found node!")
						queue = []
						break
			# print("")

		# Determine resulting tour
		result = []
		crNode = endID
		result.append(crNode)
		# print("Resulting tour:")
		# print(" ", crNode, end=" ")
		while not crNode == startID:
			crNode = root[crNode]
			if crNode == -1:
				# print(" Failed to find path!")
				return []
			result.insert(0, crNode)
			# print(crNode, end=" ")

		# print("")
		# print(result)
		return result

import random
import defines


class Agent:
	# Class constructor. id is agent ID, x,y are agents initial position on grid
	def __init__(self, id, nMap, nID=0, targetID=0, goalID=0):
		self.ID = id
		self.nMap = nMap
		# Starting position of agent
		self.nodeLocationID = nID
		# Target location
		self.targetID = targetID
		# Goal location
		self.goalID = goalID
		frntTour = self.nMap.biDir_BFS(nID, targetID)
		bckTour = self.nMap.biDir_BFS(targetID, goalID)
		self.tour = frntTour + bckTour
		self.waiting = False
		self.foundTarget = False
		self.backTracking = defines.BACK_TRACKING
		self.dynReplan = defines.DYNAMIC_REPLAN
		self.contReplan = defines.CONTINUOUS_REPLAN
		self.lifeTime = 0
		# print(self.tour)

	# Well-defined position update
	def updatePosition(self, dx, dy):
		if self.X + dx >= 0:
			self.X += dx
		if self.Y + dy >= 0:
			self.Y += dy

	# Find a path
	def replanPath(self):
		backTracking = False
		# Try to find a path
		if not self.foundTarget:
			segment1 = self.nMap.biDir_BFS(self.nodeLocationID, self.targetID, True)
			segment2 = self.nMap.biDir_BFS(self.targetID, self.goalID, True)
			if not segment1 == [] and not segment2 == []:
				segment1.pop(0)
				self.tour = segment1 + segment2
			else:
				backTracking = True
		else:
			seg = self.nMap.biDir_BFS(self.nodeLocationID, self.goalID, True)
			if not seg == []:
				seg.pop(0)
				self.tour = seg
			else:
				backTracking = True
		if backTracking:
			# Rows/columns
			curR, curC = self.nMap.idToRC(self.nodeLocationID)
			rows = []
			columns = []
			for i in range(5):
				rows.append(curR-2+i)
				columns.append(curC-2+i)
			# Pick a random row
			rndRow = random.choice(rows)
			# Verify that we have a valid row
			if rndRow < 0:
				rndRow = 0
			elif rndRow > self.nMap.rows-1:
				rndRow = self.nMap.rows-1
			# Pick a random column
			rndColumn = random.choice(columns)
			# Verify that we have a valid column
			if rndColumn < 0:
				rndColumn = 0
			elif rndColumn > self.nMap.columns-1:
				rndColumn = self.nMap.columns-1
			rndNode = self.nMap.RCToID(rndRow, rndColumn)
			print("Random node:", rndNode)

			if not self.foundTarget:
				# Route to target
				frntTour = self.nMap.biDir_BFS(self.nodeLocationID, rndNode)
				bckTour = self.nMap.biDir_BFS(rndNode, self.targetID)
				segment1 = frntTour + bckTour
				# route to goal
				segment2 = self.nMap.biDir_BFS(self.targetID, self.goalID)
			else:
				# Route to goal
				segment1 = self.nMap.biDir_BFS(self.nodeLocationID, rndNode)
				segment2 = self.nMap.biDir_BFS(rndNode, self.goalID)
			self.tour = segment1 + segment2


	def update(self):
		# print("Updating agent position!")
		self.lifeTime = self.lifeTime + 1
		if self.nodeLocationID == self.goalID:
			self.nMap.nodeMap[self.nodeLocationID].occupied = False
			return True
		# Are we running continuous replanning?
		if defines.CONTINUOUS_REPLAN and self.lifeTime % 3 == 0:
			# Replan again
			self.replanPath()
		if self.tour:
			nextNode = self.tour[0]
			if nextNode == self.nodeLocationID:
				# We are already at this location...
				self.tour.pop(0)
			elif not self.nMap.nodeMap[nextNode].occupied:
				# More to the next cell
				self.nMap.nodeMap[self.nodeLocationID].occupied = False
				self.nodeLocationID = nextNode
				self.nMap.nodeMap[nextNode].occupied = True
				self.tour.pop(0)
				self.waiting = False
				if self.nodeLocationID == self.targetID:
					self.foundTarget = True
			elif self.nMap.nodeMap[nextNode].occupied and defines.DYNAMIC_REPLAN:
				if not self.waiting:
					self.waiting = True
				else:
					rndNum = random.random()
					if rndNum <= 0.5:
						# Got tired of waiting... Plan a new route
						self.replanPath()
		else:
			# We lost the tour...
			print("No tour!")
			if not self.foundTarget:
				frntTour = self.nMap.biDir_BFS(self.nodeLocationID, self.targetID)
				bckTour = self.nMap.biDir_BFS(self.targetID, self.goalID)
				self.tour = frntTour + bckTour
			else:
				self.tour = self.nMap.biDir_BFS(self.nodeLocationID, self.goalID)

		return False

from Map import WHMap
import Agent
import random
import time
import defines
import sys
from collections import deque


if __name__ == '__main__':
	print("hello world!")
	agentQueue = []
	agentIDs = 0
	task_queue = deque()
	tasksComplete = 0
	longestStuck = 0
	runningTime = 0
	algorithm = 0
	file = "inputs/chat_input_1.csv"

	# Input format: algorithm-flag, random-seed, map-file
	if len(sys.argv) > 3:
		file = sys.argv[3]
		random.seed(sys.argv[2])
		algorithm = int(sys.argv[1])
	elif len(sys.argv) > 2:
		random.seed(sys.argv[2])
		algorithm = int(sys.argv[1])
	elif len(sys.argv) > 1:
		algorithm = int(sys.argv[1])
	
	defines.set_algo(algorithm)
	whMap = WHMap(file)

	# Generate a list of random numbers so that every run is the same
	rands = []
	all_tasks = []
	print("Generating rands")
	for i in range(0, defines.TIME_STEPS + 1):
		rands.append(random.random())
		task = [random.choice(whMap.startNodes), random.choice(whMap.targetNodes), random.choice(whMap.goalNodes)]
		all_tasks.append(task)

	# Main simulation loop, runs once per time-step
	for i in range(0, defines.TIME_STEPS):
		print("Running Time-Step Updates")

		# Randomly generate new agents
		rnd = rands[i]
		if rnd < 0.25:
			# Create a new task
			task = all_tasks.pop()
			task_queue.append(task)
		if len(agentQueue) < defines.MAX_ROBOTS and len(task_queue) > 0:
			task = task_queue.popleft()
			print(task)
			# Create a new agent
			print("Creating new agent ", agentIDs)
			agentQueue.append(Agent.Agent(agentIDs, whMap, task[0],task[1],task[2]))
			agentIDs += 1

		# Run updates on each agent
		for agent in agentQueue:
			if agent.update():
				tasksComplete = tasksComplete + 1
				runningTime = runningTime + agent.lifeTime
				if longestStuck < agent.maxStepsStuck:
					longestStuck = agent.maxStepsStuck
				agentQueue.remove(agent)

		if defines.SHOW_MAP:
			# Update grid-world display
			whMap.updateMap(agentQueue)

		print("Competed step: ", i)
		time.sleep(0.1)
	
	# Hit the end... check all remaining agents to see how long they were stuck
	for agent in agentQueue:
		if longestStuck < agent.maxStepsStuck:
			longestStuck = agent.maxStepsStuck


	# Set standard out to print to file
	if tasksComplete == 0:
		avg_time = float('inf')
	else:
		avg_time = runningTime/tasksComplete

	# Report results
	if defines.FILE_PRINT:
		# Save current standard out setting
		original_stdout = sys.stdout
		# Open a file
		with open('results.txt', 'a') as f:
			sys.stdout = f
			print(algorithm, tasksComplete, avg_time, longestStuck, file)
			# Reset standard out
			sys.stdout = original_stdout

	print("")
	print("Tasks complete: ", tasksComplete)
	print("Average time: ", avg_time)
	print("Max Wait: ", longestStuck)

	if defines.MAKE_GIF:
		whMap.printGIF()

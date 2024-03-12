from Map import WHMap
import Agent
import random
import time
import defines
import sys


if __name__ == '__main__':
	print("hello world!")
	agentQueue = []
	agentIDs = 0
	whMap = WHMap()
	tasksComplete = 0
	runningTime = 0
	if len(sys.argv) > 1:
		random.seed(sys.argv[1])

	# Main simulation loop, runs once per time-step
	for i in range(0, defines.TIME_STEPS):
		# agentQueue, agentIDs = runTSUpdates(agentQueue, agentIDs, whMap)
		print("Running Time-Step Updates")

		# Randomly generate new agents
		rnd = random.random()
		if rnd < 0.25:
			if not defines.BACK_TRACKING or len(agentQueue) < 10:
				# Create a new agent
				print("Creating new agent ", agentIDs)
				agentQueue.append(Agent.Agent(agentIDs, whMap, random.choice(whMap.startNodes),
				                         random.choice(whMap.targetNodes),
				                         random.choice(whMap.goalNodes)))
				agentIDs += 1

		# Run updates on each agent
		for agent in agentQueue:
			if agent.update():
				tasksComplete = tasksComplete + 1
				runningTime = runningTime + agent.lifeTime
				agentQueue.remove(agent)

		if defines.SHOW_MAP:
			# Update grid-world display
			whMap.updateMap(agentQueue)

		print("Competed step: ", i)
		time.sleep(0.1)

	# Report results
	if defines.FILE_PRINT:
		# Save current standard out setting
		original_stdout = sys.stdout
		# Open a file
		with open('results.txt', 'a') as f:
			# Set standard out to print to file
			sys.stdout = f
			print(tasksComplete, ", ", runningTime, ", ", runningTime/tasksComplete)
			# Reset standard out
			sys.stdout = original_stdout

	print("")
	print("Tasks complete: ", tasksComplete)
	print("Total robot time: ", runningTime)
	print("Average time: ", runningTime/tasksComplete)

	if defines.MAKE_GIF:
		whMap.printGIF()

DYNAMIC_REPLAN = False
CONTINUOUS_REPLAN = False
LOWER_BOUND = False

ASTAR = True

TIME_STEPS = 500
MAX_ROBOTS = 10
SHOW_MAP = False
FILE_PRINT = True

# Does not work
MAKE_GIF = False

def set_algo(algorithm):
	global DYNAMIC_REPLAN
	global CONTINUOUS_REPLAN
	global LOWER_BOUND
	if algorithm == 0:
		# Continuous replanning
		DYNAMIC_REPLAN = False
		CONTINUOUS_REPLAN = True
		LOWER_BOUND = False
	elif algorithm == 1:
		# Dynamic replanning
		DYNAMIC_REPLAN = True
		CONTINUOUS_REPLAN = False
		LOWER_BOUND = False
	elif algorithm == 2:
		# Assume traffic patterns will save you...
		DYNAMIC_REPLAN = False
		CONTINUOUS_REPLAN = False
		LOWER_BOUND = False
	elif algorithm == 3:
		# Lower-bound
		DYNAMIC_REPLAN = False
		CONTINUOUS_REPLAN = False
		LOWER_BOUND = True
	else:
		print("Bad algorithm!")
		exit(0)
BACK_TRACKING = False
DYNAMIC_REPLAN = False
CONTINUOUS_REPLAN = False

TIME_STEPS = 500
SHOW_MAP = True
FILE_PRINT = True

# Does not work
MAKE_GIF = False

def set_algo(algorithm):
	global BACK_TRACKING
	global DYNAMIC_REPLAN
	global CONTINUOUS_REPLAN
	if algorithm == 0:
		# Continuous replanning
		BACK_TRACKING= False
		DYNAMIC_REPLAN = False
		CONTINUOUS_REPLAN = True
	elif algorithm == 1:
		# Dynamic replanning
		BACK_TRACKING = False
		DYNAMIC_REPLAN = True
		CONTINUOUS_REPLAN = False
	elif algorithm == 2:
		# Assume traffic patterns will save you...
		BACK_TRACKING = False
		DYNAMIC_REPLAN = False
		CONTINUOUS_REPLAN = False
	elif algorithm == 3:
		# Lower-bound
		BACK_TRACKING = False
		DYNAMIC_REPLAN = False
		CONTINUOUS_REPLAN = False
	else:
		print("Bad algorithm!")
		exit(0)
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

numRows = 6
numColumns = 4

# initialize board
img = plt.figure(figsize=[10, 10])
img.patch.set_facecolor((1, 1, 1))
board = img.add_subplot(111)

# draw grid on board
for x in range(numColumns + 1):
    board.plot([x, x], [0, numRows], 'k')

for y in range(numRows + 1):
    board.plot([0, numColumns], [y, y], 'k')

# turn board axis off
board.set_axis_off()

# scale board to fit in window
board.set_xlim(0, numColumns)
board.set_ylim(0, numRows)

# 2d array of artists
artists = [[None]*numRows]*numColumns

print("\n--------\n")


# create artists and assign colors
for x in range(numColumns):
    for y in range(numRows):
        tileColor = (0.5 + 0.5*(x / numColumns), y / numRows, 0.5)
        
        artists[x][y] = mpatches.Rectangle((x, y), 1, 1, color=tileColor)
        
        board.add_artist(artists[x][y])
        
        print("Added rectangle at " + str(x) + ", " + str(y))
        print("Artist data: " + str(artists[x][y]))
        plt.pause(0.05)

for x in range(numColumns):
    for y in range(numRows):
        tileColor = (0.5 - 0.5*(x / numColumns), 1 - y / numRows, 0.5)
        
        artists[x][y] = mpatches.Rectangle((x, y), 1, 1, color=tileColor)
        
        board.add_artist(artists[x][y])
        
        print("Added rectangle at " + str(x) + ", " + str(y))
        print("Artist data: " + str(artists[x][y]))
        plt.pause(0.05)

plt.pause(10)
import csv
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np

class WarehouseEditor:
	def __init__(self, warehouse_layout):
		self.warehouse_layout = warehouse_layout
		self.rows = len(warehouse_layout)
		self.cols = len(warehouse_layout[0])

		self.color_map = {'S': 'blue', 'G': 'yellow', 'X': 'black', 'E': 'white'}

		self.fig, self.ax = plt.subplots(figsize=(self.cols, self.rows))
		self.ax.set_aspect('equal')
		self.ax.axis('off')

		self.cell_width = 1.0 / self.cols
		self.cell_height = 1.0 / self.rows

		# Draw the map
		self.draw_map()

		self.selected_cell = None
		self.fig.canvas.mpl_connect('button_press_event', self.on_click)

		self.save_button = Button(plt.axes([0.8, 0.05, 0.1, 0.05]), 'Save')
		self.save_button.on_clicked(self.save_warehouse)
	
	def draw_map(self):
		self.cells = np.zeros((self.rows, self.cols), dtype='object')
		for row_idx, row in enumerate(warehouse_layout):
			for col_idx, cell in enumerate(row):
				self.cells[row_idx, col_idx] = plt.Rectangle((col_idx * self.cell_width, 1.0 - (row_idx + 1) * self.cell_height), self.cell_width, self.cell_height, color=self.color_map[cell], edgecolor='black')
				self.ax.add_patch(self.cells[row_idx, col_idx])
		# Draw vertical gridlines
		for i in range(self.cols + 1):
			self.ax.plot([i * self.cell_width, i * self.cell_width], [0, 1], color='black')
		# Draw horizontal gridlines
		for i in range(self.rows + 1):
			self.ax.plot([0, 1], [i * self.cell_height, i * self.cell_height], color='black')

	def on_click(self, event):
		if event.inaxes == self.ax:
			col_idx = int(event.xdata / self.cell_width)
			row_idx = self.rows - int(event.ydata / self.cell_height) - 1
			self.selected_cell = self.cells[row_idx, col_idx]
			if self.selected_cell:
				# Toggle black and white
				if self.warehouse_layout[row_idx][col_idx] == 'X':
					new_value = 'E'
				elif self.warehouse_layout[row_idx][col_idx] == 'E':
					new_value = 'X'
				else:
					# Dont change anything...
					new_value = self.warehouse_layout[row_idx][col_idx]
				# Update the cell
				self.warehouse_layout[row_idx][col_idx] = new_value
				self.selected_cell.set_color(self.color_map[new_value])
				self.fig.canvas.draw()  # Update the plot immediately

	def save_warehouse(self, event):
		file_path = input("Enter the path to save the CSV file: ")
		with open(file_path, 'w', newline='') as file:
			csv_writer = csv.writer(file)
			for row in self.warehouse_layout:
				csv_writer.writerow(row)

if __name__ == "__main__":
	file_path = input("Enter the path to the CSV file: ")
	warehouse_layout = []
	with open(file_path, 'r') as file:
		csv_reader = csv.reader(file)
		for row in csv_reader:
			warehouse_layout.append(row)

	warehouse_editor = WarehouseEditor(warehouse_layout)
	plt.show()


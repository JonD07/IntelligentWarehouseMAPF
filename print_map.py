import csv
import matplotlib.pyplot as plt
import numpy as np

def read_csv_file(file_path):
    warehouse_layout = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            warehouse_layout.append(row)
    return warehouse_layout

def plot_warehouse(warehouse_layout):
    rows = len(warehouse_layout)
    cols = len(warehouse_layout[0])

    color_map = {'S': 'blue', 'G': 'yellow', 'X': 'black', 'E': 'white'}

    # Create a grid of appropriate size
    plt.figure(figsize=(cols, rows))

    for row_idx, row in enumerate(warehouse_layout):
        for col_idx, cell in enumerate(row):
            color = color_map.get(cell, 'white')
            plt.fill([col_idx, col_idx + 1, col_idx + 1, col_idx], [rows - row_idx, rows - row_idx, rows - (row_idx + 1), rows - (row_idx + 1)], color)

    # Adding lines between cells
    for i in range(cols + 1):
        plt.plot([i, i], [0, rows], color='black', linewidth=2)
    for i in range(rows + 1):
        plt.plot([0, cols], [i, i], color='black', linewidth=2)

    plt.gca().set_aspect('equal', adjustable='box')
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    file_path = input("Enter the path to the CSV file: ")
    warehouse_layout = read_csv_file(file_path)
    plot_warehouse(warehouse_layout)


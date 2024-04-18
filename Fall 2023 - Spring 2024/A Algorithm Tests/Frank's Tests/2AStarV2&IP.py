from PIL import Image
import numpy as np
from queue import PriorityQueue
from math import sqrt

def image_to_binary_grid(image_path):
    """Convert an image to the matix of a 100x100 binary grid (Note:need to standardize size)."""
    img = Image.open(image_path).convert('L')  # Convert B&W
    img = img.resize((100, 100))
    threshold = 200  # 200-220
    bw = np.array(img) < threshold
    return bw.astype(int)  #0 is obstacle, 1 is schematic

def h(p1, p2):
    """Heuristic mathod used Manhattan distance."""
    return max(abs(p1[0] - p2[0]), abs(p1[1] - p2[1]))

def get_neighbors(grid, node):
    """Finds all neighbors of a such that A is surrounded (including diagonal that are not obstacles)."""
    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),  # Straight |
        (-1, -1), (-1, 1), (1, -1), (1, 1)  # \
    ]
    neighbors = []
    for d in directions:
        neighbor = (node[0] + d[0], node[1] + d[1])
        if 0 <= neighbor[0] < grid.shape[0] and 0 <= neighbor[1] < grid.shape[1] and grid[neighbor[0]][neighbor[1]] == 0:
            neighbors.append(neighbor)
    return neighbors

def a_star(grid, start, end):
    """A* pathfinding."""
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    g_score = {node: float('inf') for node in np.ndindex(grid.shape)}
    g_score[start] = 0
    f_score = {node: float('inf') for node in np.ndindex(grid.shape)}
    f_score[start] = h(start, end)

    while not open_set.empty():
        current = open_set.get()[1]

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]  # reversed path

        for neighbor in get_neighbors(grid, current):
            if abs(neighbor[0] - current[0]) == 1 and abs(neighbor[1] - current[1]) == 1:
                tentative_g_score = g_score[current] + sqrt(2)  # / move
            else:
                tentative_g_score = g_score[current] + 1  # | move

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + h(neighbor, end)
                if neighbor not in [i[1] for i in open_set.queue]:
                    open_set.put((f_score[neighbor], neighbor))

    return None  # Return None if no path is found

def save_path_to_file(path, file_name=r'C:\Users\frank\OneDrive\Documents\College\Spring 2024\Capstone\Harness Project Scripts\Path.txt'):
    """Saves path to text file, one coordinate per line [ex. y, x] (top left is origin)"""
    try:
        with open(file_name, 'w') as file:
            for x, y in path:
                file.write(f"{x},{y}\n")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")

def print_grid(grid):
    """show grid in console."""
    for row in grid:
        print("".join(['1' if cell == 1 else '0' for cell in row]))

def read_end_points(file_name=r'C:\Users\frank\OneDrive\Documents\College\Spring 2024\Capstone\Harness Project Scripts\EndPoints.txt'):
    """Reads end points from a file and attaches their variable names to the specificed coordinates in txt file."""
    end_points = {}
    with open(file_name, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) == 2:
                var_name = parts[0]
                coordinates = eval(parts[1])  # string 2 tuple
                end_points[var_name] = coordinates
    return end_points


def main():
    image_path = r'C:\Users\frank\OneDrive\Pictures\A1.png'
    binary_grid = image_to_binary_grid(image_path)
    print("Initial Grid:")
    print_grid(binary_grid)  # Print the initial grid

    # Read end points from file
    end_points = read_end_points()

    # User input start & end points with variable (Nodes)
    start_var = input("Enter start variable (e.g., A): ").strip()
    end_var = input("Enter end variable (e.g., B): ").strip()

    if start_var in end_points and end_var in end_points:
        start = end_points[start_var]
        end = end_points[end_var]

        path = a_star(binary_grid, start, end)

        if path:
            print("Path found. Saving to file...")
            save_path_to_file(path)
            print("Path saved to path.txt.")
        else:
            print("No path found.")
    else:
        print("Invalid variable names entered.")

if __name__ == "__main__":
    main()

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import numpy as np
import heapq

# Define the Cell class
class Cell:
    def __init__(self):
        self.parent_i = 0  # Parent cell's row index
        self.parent_j = 0  # Parent cell's column index
        self.f = float('inf')  # Total cost of the cell (g + h)
        self.g = float('inf')  # Cost from start to this cell
        self.h = 0  # Heuristic cost from this cell to destination

ROW = 1000
COL = 1000

def is_valid(row, col):
    return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL)

def is_unblocked(grid, row, col):
    return grid[row][col] == 1

def is_destination(row, col, dest):
    return row == dest[0] and col == dest[1]

def calculate_h_value(row, col, dest):
    return ((row - dest[0]) ** 2 + (col - dest[1]) ** 2) ** 0.5

def process_pixel(pixel):
    # Threshold the pixel value to convert it to binary
    threshold = 200
    return 1 if pixel < threshold else 0

def analyze_image(image_path):
    # Open the image file
    with Image.open(image_path) as img:
        # Convert the image to grayscale
        img = img.convert("L")
        # Get the pixel values as a NumPy array
        pixel_values = np.array(img)
        # Process each pixel to get the final binary grid
        grid = np.array([[process_pixel(pixel) for pixel in row] for row in pixel_values])
        return grid

def read_coordinates_from_file(file_path):
    coordinates = {}
    with open(file_path, 'r') as file:
        for line in file:
            letter, x, y = line.split()
            coordinates[letter] = (int(x), int(y))
    return coordinates

def a_star_search(grid, src, dest):
    # Check if the source and destination are valid
    if not is_valid(src[0], src[1]) or not is_valid(dest[0], dest[1]):
        print("Source or destination is invalid")
        return []

    # Check if the source and destination are unblocked
    if not is_unblocked(grid, src[0], src[1]) or not is_unblocked(grid, dest[0], dest[1]):
        print("Source or the destination is blocked")
        return []

    # Check if we are already at the destination
    if is_destination(src[0], src[1], dest):
        print("We are already at the destination")
        return []

    # Initialize the closed list (visited cells)
    closed_list = [[False for _ in range(COL)] for _ in range(ROW)]
    # Initialize the details of each cell
    cell_details = [[Cell() for _ in range(COL)] for _ in range(ROW)]

    # Initialize the start cell details
    i = src[0]
    j = src[1]
    cell_details[i][j].f = 0
    cell_details[i][j].g = 0
    cell_details[i][j].h = 0
    cell_details[i][j].parent_i = i
    cell_details[i][j].parent_j = j

    # Initialize the open list (cells to be visited) with the start cell
    open_list = []
    heapq.heappush(open_list, (0.0, i, j))

    # Initialize the flag for whether destination is found
    found_dest = False

    # Main loop of A* search algorithm
    while len(open_list) > 0:
        # Pop the cell with the smallest f value from the open list
        p = heapq.heappop(open_list)

        # Mark the cell as visited
        i = p[1]
        j = p[2]
        closed_list[i][j] = True

        # For each direction, check the successors
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for dir in directions:
            new_i = i + dir[0]
            new_j = j + dir[1]

            # If the successor is valid, unblocked, and not visited
            if is_valid(new_i, new_j) and is_unblocked(grid, new_i, new_j) and not closed_list[new_i][new_j]:
                # If the successor is the destination
                if is_destination(new_i, new_j, dest):
                    # Set the parent of the destination cell
                    cell_details[new_i][new_j].parent_i = i
                    cell_details[new_i][new_j].parent_j = j
                    print("The destination cell is found")
                    # Trace and return the path from source to destination
                    found_dest = True
                    return trace_path(cell_details, dest)
                else:
                    # Calculate the new f, g, and h values
                    g_new = cell_details[i][j].g + 1.0
                    h_new = calculate_h_value(new_i, new_j, dest)
                    f_new = g_new + h_new

                    # If the cell is not in the open list or the new f value is smaller
                    if cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new:
                        # Add the cell to the open list
                        heapq.heappush(open_list, (f_new, new_i, new_j))
                        # Update the cell details
                        cell_details[new_i][new_j].f = f_new
                        cell_details[new_i][new_j].g = g_new
                        cell_details[new_i][new_j].h = h_new
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j

    # If the destination is not found after visiting all cells
    if not found_dest:
        print("Failed to find the destination cell")
        return []


def trace_path(cell_details, dest):
    path_coords = []
    row = dest[0]
    col = dest[1]

    # Trace the path from destination to source using parent cells
    while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
        path_coords.append((row, col))
        temp_row = cell_details[row][col].parent_i
        temp_col = cell_details[row][col].parent_j
        row = temp_row
        col = temp_col

    # Add the source cell to the path
    path_coords.append((row, col))
    # Reverse the path to get the path from source to destination
    path_coords.reverse()

    return path_coords


def main():
    # Define the grid (1 for unblocked, 0 for blocked)
    image_path = "aircraft.jpg"
    result = analyze_image(image_path)

    # Read coordinates from file
    coordinates_file_path = "coordinates.txt"
    letter_coordinates = read_coordinates_from_file(coordinates_file_path)

    # Prompt the user to input source and destination letters
    src_letter = input("Enter the source letter (A to W): ").upper()  # Convert to uppercase for consistency
    dest_letter = input("Enter the destination letter (A to W): ").upper()

    # Get the source and destination coordinates
    src = letter_coordinates.get(src_letter)
    dest = letter_coordinates.get(dest_letter)

    if src is None or dest is None:
        print("Invalid source or destination letter.")
        return


    # Run the A* search algorithm and save the path coordinates
    path_coords = a_star_search(result, src, dest)

    # Check if the path_coords list is empty
    if not path_coords:
        print("No path found between source and destination.")
        return

    # Print the path coordinates
    # print("Path coordinates:", path_coords)

    img = mpimg.imread('aircraft.jpg')

    plt.imshow(img)

    # Unpack the coordinates only if the list is not empty
    if path_coords:
        x_coords, y_coords = zip(*path_coords)
        plt.plot(y_coords, x_coords, color='red', linewidth=2)

    plt.show()


if __name__ == "__main__":
    main()

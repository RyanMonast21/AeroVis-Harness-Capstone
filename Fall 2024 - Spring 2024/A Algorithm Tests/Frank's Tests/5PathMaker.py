def read_path_from_file(file_name=r'C:\Users\frank\OneDrive\Documents\College\Spring 2024\Capstone\path txt\path.txt'):
    """Reads Variables and their coordinates from a file and returns a list."""
    path = []
    with open(file_name, 'r') as file:
        for line in file:
            x, y = map(int, line.strip().split(','))
            path.append((x, y))
    return path


def create_matrix_with_path(path, size=(100, 100)):
    """Creates a matrix. path marked as 0s."""
    # Initialize the matrix with 1s
    matrix = [[1 for _ in range(size[0])] for _ in range(size[1])]

    # Mark the path in the matrix with 0s
    for x, y in path:
        matrix[x][y] = 0

    return matrix


def print_matrix(matrix):
    """Prints the matrix 'Schematic')."""
    for row in matrix:
        print(''.join(str(cell) for cell in row))


def main():
    file_path = r'C:\Users\frank\OneDrive\Documents\College\Spring 2024\Capstone\Harness Project Scripts\Path.txt'
    try:
        # Read the path from the file
        path = read_path_from_file(file_path)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return

    # Create new the matrix with the path
    matrix = create_matrix_with_path(path)

    # Print the matrix (only for visuals)
    print_matrix(matrix)

if __name__ == "__main__":
    main()

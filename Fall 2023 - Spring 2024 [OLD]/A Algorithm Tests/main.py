import pygame as pg
from heapq import *

def get_start_goal_from_input():
    valid_positions = {
        'a': (10, 0),
        'b': (13, 9),
        'c': (10, 5),
        'd': (0, 14),
        'e': (9, 0),
        'f': (20, 11),
    }
    print("Select a position (a, b, c, d, e, f): ")
    while True:
        user_input = input().lower()
        if user_input in valid_positions:
            return valid_positions[user_input]
        else:
            print("Invalid input. Please select a valid position.")
def get_circle(x, y, size):
    return (x * size + size // 2, y * size + size // 2), size // 4

def get_rect(x, y, size):
    return x * size + 1, y * size + 1, size - 2, size - 2


def get_next_nodes(x, y):
    check_next_node = lambda x, y: True if 0 <= x < cols and 0 <= y < rows else False
    ways = [-1, 0], [0, -1], [1, 0], [0, 1]
    return [(grid[y + dy][x + dx], (x + dx, y + dy)) for dx, dy in ways if check_next_node(x + dx, y + dy)]


def heuristic(a, b):
   return abs(a[0] - b[0]) + abs(a[1] - b[1])


cols, rows = 21, 29
TILE_SIZE = 20

pg.init()
sc = pg.display.set_mode([cols * TILE_SIZE, rows * TILE_SIZE])
clock = pg.time.Clock()
# do vectors instead - problem is mapping - .json - instructions making points through the image
# grid - module class - guey - scanner class and then call calls another class that creates a model - creating a 2d matrix to get a color from a point
grid = ['810000003100014000000',
        '811000003100014000000',
        '001000003100011111111',
        '001110011100000000001',
        '002210010000000000001',
        '002210010011110000001',
        '002210010033010001111',
        '001110010000010001770',
        '001000010000011111770',
        '061000011100010001770',
        '061000088100000001111',
        '061000088100000001000',
        '061000088100011111000',
        '061111111100010000000',
        '000091000000010000000',
        '000091000000011111110',
        '000091000000000000010',
        '000091000000000000010',
        '000091000000000000010',
        '000001000000000000015',
        '000001000000000000015',
        '000001111111110000015',
        '000000000000011111115',
        '000000000000010000000',
        '000000000000010000000',
        '000000000000010000000',
        '000000000000010000000',
        '111111111111110000000',
        '000000000000000000000',]

grid = [[int(char) for char in string ] for string in grid]
# dict of adjacency lists
graph = {}
for y, row in enumerate(grid):
    for x, col in enumerate(row):
        graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(x, y)

start = (0, 27)
goal = get_start_goal_from_input()
queue = []
heappush(queue, (0, start))
cost_visited = {start: 0}
visited = {start: None}

bg = pg.image.load('test.png').convert()
bg = pg.transform.scale(bg, (cols * TILE_SIZE, rows * TILE_SIZE))

# Define a dictionary to map grid values to colors
color_mapping = {
    0: pg.Color('white'),
    1: pg.Color('black'),
    2: pg.Color('red'),
    3: pg.Color('orange'),
    4: pg.Color('limegreen'),
    5: pg.Color('green'),
    6: pg.Color('teal'),
    7: pg.Color('blue'),
    8: pg.Color('lightblue'),
    9: pg.Color('purple')
}
while True:
    # Draw grid based on color mapping
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            pg.draw.rect(sc, color_mapping[col], get_rect(x, y, TILE_SIZE))

        # Dijkstra logic
        if queue:
            cur_cost, cur_node = heappop(queue)
            if cur_node == goal:
                queue = []
                continue

            next_nodes = [(cost, node) for cost, node in get_next_nodes(*cur_node) if grid[node[1]][node[0]] == 1]
            for next_node in next_nodes:
                neigh_cost, neigh_node = next_node
                new_cost = cost_visited[cur_node] + neigh_cost

                if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                    priority = new_cost + heuristic(neigh_node, goal)
                    heappush(queue, (priority, neigh_node))
                    cost_visited[neigh_node] = new_cost
                    visited[neigh_node] = cur_node

        # Draw path restricted to black tiles
        path_head, path_segment = cur_node, cur_node
        while path_segment:
            x, y = path_segment
            if grid[y][x] == 1:  # Check if the tile is black
                pg.draw.circle(sc, pg.Color('grey'), *get_circle(x, y, TILE_SIZE))
            path_segment = visited[path_segment]

    # draw path
    path_head, path_segment = cur_node, cur_node
    while path_segment:
        pg.draw.circle(sc, pg.Color('gray'), *get_circle(x, y, TILE_SIZE))
        path_segment = visited[path_segment]
        # Draw start and goal circles
        pg.draw.circle(sc, pg.Color('red'), *get_circle(*start, TILE_SIZE))
        pg.draw.circle(sc, pg.Color('green'), *get_circle(*path_head, TILE_SIZE))

    # pygame necessary lines
    [exit() for event in pg.event.get() if event.type == pg.QUIT]
    pg.display.flip()
    clock.tick(7)

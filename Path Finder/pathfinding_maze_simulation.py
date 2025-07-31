
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import time
import random

# Maze dimensions
rows, cols = 10, 10

# Generate a random grid maze (0 = path, 1 = wall)
np.random.seed(42)
maze = np.random.choice([0, 1], size=(rows, cols), p=[0.7, 0.3])
maze[0, 0] = 0  # start
maze[rows-1, cols-1] = 0  # end

# Create a graph from the maze
def maze_to_graph(maze):
    G = nx.DiGraph()
    for r in range(rows):
        for c in range(cols):
            if maze[r, c] == 0:
                for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and maze[nr, nc] == 0:
                        G.add_edge((r, c), (nr, nc), weight=1)
    return G

G = maze_to_graph(maze)
start, end = (0, 0), (rows-1, cols-1)

# Pathfinding functions
def run_algorithm(algorithm, G, start, end, heuristic=None):
    try:
        t0 = time.time()
        if algorithm == 'dijkstra':
            path = nx.dijkstra_path(G, start, end)
        elif algorithm == 'astar':
            path = nx.astar_path(G, start, end, heuristic=heuristic)
        elif algorithm == 'bellman-ford':
            path = nx.bellman_ford_path(G, start, end)
        else:
            path = []
        t1 = time.time()
        return path, t1 - t0
    except nx.NetworkXNoPath:
        return [], float('inf')

# Heuristic for A* (Manhattan distance)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Run and collect results
results = {}
for algo in ['dijkstra', 'astar', 'bellman-ford']:
    path, duration = run_algorithm(algo, G, start, end, heuristic if algo == 'astar' else None)
    results[algo] = {'path': path, 'time': duration}

# Plotting
def draw_maze(maze, paths):
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    algorithms = ['dijkstra', 'astar', 'bellman-ford']
    for i, algo in enumerate(algorithms):
        ax = axs[i]
        ax.imshow(maze, cmap='binary')
        ax.set_title(f"{algo.title()} - Time: {results[algo]['time']:.5f}s")
        for (r, c) in results[algo]['path']:
            ax.plot(c, r, 'ro')
        ax.plot(0, 0, 'gs')  # start
        ax.plot(cols-1, rows-1, 'bs')  # end
    plt.tight_layout()
    plt.show()

draw_maze(maze, results)

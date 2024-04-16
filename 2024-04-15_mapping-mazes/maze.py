"""Code to generate and solve mazes"""

from queue import PriorityQueue
import random
import networkx as nx

class Maze:
    """Grid maze in the form of a random spanning tree"""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.start = (0, 0)
        self.end = (width - 1, height - 1)
        grid = nx.grid_2d_graph(self.width, self.height)
        self.tree = nx.random_spanning_tree(grid)

    def save(self, filename):
        """Save maze to a text file"""
        with open(filename, "w") as file:
            file.write("n1x\tn1y\tn2x\tn2y\n")
            for edge in self.tree.edges:
                file.write(f"{edge[0][0]}\t{edge[0][1]}\t{edge[1][0]}\t{edge[1][1]}\n")

    def solve(self, method, searchfile=None, solutionfile=None):
        """Solve maze using DFS, BFS, or heuristic search"""
        if method == "heuristic":
            to_check = PriorityQueue()
            dist_from_end = abs(self.start[0] - self.end[0]) + abs(self.start[1] - self.end[1])
            dist_from_end += 0.01 * random.random() # Break ties randomly
            to_check.put((dist_from_end, [self.start]))
        else:
            to_check = [[self.start]] # Keep track of each potential shortest path
        visited = set()
        history = [] # Keep track of the entire search move-by-move
        while True:
            if method == "DFS":
                path = to_check.pop()
            elif method == "BFS":
                path = to_check.pop(0)
            else:
                assert method == "heuristic"
                _, path = to_check.get()
            node = path[-1]
            visited.add(node)
            if len(history) > 0:
                # Record full search path, no jumps
                for n in nx.shortest_path(self.tree, history[-1], node)[1:]:
                    history.append(n)
            else:
                history.append(node)
            if node == self.end:
                if searchfile:
                    self.save_path(history, searchfile)
                    assert solutionfile
                    self.save_path(path, solutionfile)
                    break
                else:
                    return history, path
            neighbors = list(self.tree.neighbors(node))
            random.shuffle(neighbors)
            for neighbor in neighbors:
                if neighbor not in visited:
                    if method == "heuristic":
                        dist_from_end = abs(neighbor[0] - self.end[0]) + abs(neighbor[1] - self.end[1])
                        dist_from_end += len(path) + 0.01 * random.random()
                        to_check.put((dist_from_end, path + [neighbor]))
                    else:
                        to_check.append(path + [neighbor])

    def save_path(self, path, filename):
        """Save maze path to a text file"""
        with open(filename, "w") as file:
            file.write("x\ty\n")
            for node in path:
                file.write(f"{node[0]}\t{node[1]}\n")

mazes = [Maze(30, 20) for _ in range(6)]
mazes[0].solve("BFS", f"solve_BFS/search_0_0.txt", f"solve_BFS/solution_0_0.txt")
mazes[0].solve("heuristic", f"solve_heuristic/search_0_0.txt", f"solve_heuristic/solution_0_0.txt")
for i, maze in enumerate(mazes):
    maze.save(f"mazes/maze_{i}.txt")
    for j in range(20):
        maze.solve("DFS", f"solve_DFS/search_{i}_{j}.txt", f"solve_DFS/solution_{i}_{j}.txt")

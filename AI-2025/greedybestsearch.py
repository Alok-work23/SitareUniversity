import heapq

class Maze:
    def __init__(self, grid):
        self.grid = grid
        self.start, self.goal = self._find_positions()

    def _find_positions(self):
        start = goal = None
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if cell == 'A':
                    start = (i, j)
                elif cell == 'B':
                    goal = (i, j)
        return start, goal

    def get_neighbors(self, position):
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        neighbors = []
        rows, cols = len(self.grid), len(self.grid[0])
        for dx, dy in directions:
            nx, ny = position[0] + dx, position[1] + dy
            if 0 <= nx < rows and 0 <= ny < cols and self.grid[nx][ny] != 1:
                neighbors.append((nx, ny))
        return neighbors

    def display(self):
        for row in self.grid:
            print(' '.join(str(cell) for cell in row))
        print()

    def visualize_path(self, path):
        for r, c in path:
            if (r, c) != self.start and (r, c) != self.goal:
                self.grid[r][c] = '*'
        self.display()


class GreedyBestFirstSearch:
    def __init__(self, maze: Maze):
        self.maze = maze
        self.start = maze.start
        self.goal = maze.goal

    @staticmethod
    def manhattan(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def find_path(self):
        heap = []
        visited = set()
        came_from = {}

        heapq.heappush(heap, (self.manhattan(self.start, self.goal), self.start))

        while heap:
            _, current = heapq.heappop(heap)

            if current == self.goal:
                break

            if current in visited:
                continue

            visited.add(current)

            for neighbor in self.maze.get_neighbors(current):
                if neighbor not in visited:
                    heapq.heappush(heap, (self.manhattan(neighbor, self.goal), neighbor))
                    if neighbor not in came_from:
                        came_from[neighbor] = current

        return self._reconstruct_path(came_from)

    def _reconstruct_path(self, came_from):
        path = []
        current = self.goal
        while current != self.start:
            path.append(current)
            current = came_from.get(current)
            if current is None:
                print("No path found.")
                return []
        path.append(self.start)
        path.reverse()
        return path


# Example usage
if __name__ == "__main__":
    maze_grid = [
        ['A', 0,  1,  0,  0,  0, 1, 0, 0, 1, 0, 0],
        [0,   0,  1,  0,  1,  0, 1, 0, 1, 0, 0, 0],
        [1,   0,  0,  0,  1,  0, 0, 0, 1, 1, 1, 0],
        [0,   1,  1,  0,  0,  1, 1, 0, 0, 0, 1, 0],
        [0,   0,  0,  0,  1,  0, 1, 1, 1, 0, 0, 0],
        [1,   1,  1,  0,  1,  0, 0, 0, 1, 1, 1, 0],
        [0,   0,  1,  0,  0,  0, 1, 0, 0, 0, 1, 0],
        [0,   1,  0,  1,  1,  0, 1, 1, 1, 0, 1, 0],
        [0,   0,  0,  0,  0,  0, 0, 0, 1, 0, 0, 0],
        [1,   1,  1,  1,  1,  1, 0, 1, 0, 1, 1, 0],
        [0,   0,  0,  0,  0,  0, 0, 1, 0, 0, 0, 0],
        [0,   1,  1,  1,  1,  1, 1, 1, 1, 1, 1,'B'],
    ]

    maze = Maze(maze_grid)
    solver = GreedyBestFirstSearch(maze)

    path = solver.find_path()
    print("Path from A to B:", path)
    maze.visualize_path(path)

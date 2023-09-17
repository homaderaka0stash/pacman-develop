from typing import Protocol, Dict, List, Iterator, Tuple, TypeVar, Optional
import heapq
import collections

T = TypeVar('T')

Location = TypeVar('Location')


class Graph(Protocol):
    def neighbors(self, id: Location) -> List[Location]: pass




class Queue:
    def __init__(self):
        self.elements = collections.deque()

    def empty(self) -> bool:
        return len(self.elements) == 0

    def put(self, x: T):
        self.elements.append(x)

    def get(self) -> T:
        return self.elements.popleft()



GridLocation = Tuple[int, int]


class SquareGrid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.walls: List[GridLocation] = []

    def in_bounds(self, id: GridLocation) -> bool:
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id: GridLocation) -> bool:
        return id not in self.walls

    def neighbors(self, id: GridLocation) -> Iterator[GridLocation]:
        (x, y) = id
        neighbors = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]  # E W N S
        # see "Ugly paths" section for an explanation:
        if (x + y) % 2 == 0: neighbors.reverse()  # S N W E
        results = filter(self.in_bounds, neighbors)
        results = filter(self.passable, results)
        return results


class WeightedGraph(Graph):
    def cost(self, from_id: Location, to_id: Location) -> float: pass


class GridWithWeights(SquareGrid):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.weights: Dict[GridLocation, float] = {}

    def cost(self, from_node: GridLocation, to_node: GridLocation) -> float:
        return self.weights.get(to_node, 1)

class PriorityQueue:
    def __init__(self):
        self.elements: List[Tuple[float, T]] = []

    def empty(self) -> bool:
        return len(self.elements) == 0

    def put(self, item: T, priority: float):
        heapq.heappush(self.elements, (priority, item))

    def get(self) -> T:
        return heapq.heappop(self.elements)[1]


def dijkstra_search(graph: WeightedGraph, start: Location, goal: Location):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from: Dict[Location, Optional[Location]] = {}
    cost_so_far: Dict[Location, float] = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current: Location = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far


def reconstruct_path(came_from: Dict[Location, Location],
                     start: Location, goal: Location) -> List[Location]:
    current: Location = goal
    path: List[Location] = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)  # optional
    path.reverse()  # optional
    return path



class SquareGridNeighborOrder(SquareGrid):
    def neighbors(self, id):
        (x, y) = id
        neighbors = [(x + dx, y + dy) for (dx, dy) in self.NEIGHBOR_ORDER]
        results = filter(self.in_bounds, neighbors)
        results = filter(self.passable, results)
        return list(results)



class GridWithAdjustedWeights(GridWithWeights):
    def cost(self, from_node, to_node):
        prev_cost = super().cost(from_node, to_node)
        nudge = 0
        (x1, y1) = from_node
        (x2, y2) = to_node
        if (x1 + y1) % 2 == 0 and x2 != x1: nudge = 1
        if (x1 + y1) % 2 == 1 and y2 != y1: nudge = 1
        return prev_cost + 0.001 * nudge


g = GridWithWeights(30, 31)
g.walls = [(1, 0),(2, 0),(3, 0),(4, 0),(5, 0),(6, 0),(7, 0),(8, 0),(9, 0),(10, 0),(11, 0),(12, 0),(13, 0),(14, 0),(15, 0),(16, 0),(17, 0),(18, 0),(19, 0),(20, 0),(21, 0),(22, 0),(23, 0),(24, 0),(25, 0),(26, 0),(27, 0),(28, 0),
           (1, 1),(14, 1),(15, 1),(28, 1),
           (1, 2),(3, 2),(4, 2),(5, 2),(6, 2),(8, 2),(9, 2),(10, 2),(11, 2),(12, 2),(14, 2),(15, 2),(17, 2),(18, 2),(19, 2),(20, 2),(21, 2),(23, 2),(24, 2),(25, 2),(26, 2),(28, 2),
           (1, 3),(3, 3),(4, 3),(5, 3),(6, 3),(8, 3),(9, 3),(10, 3),(11, 3),(12, 3),(14, 3),(15, 3),(17, 3),(18, 3),(19, 3),(20, 3),(21, 3),(23, 3),(24, 3),(25, 3),(26, 3),(28, 3),
           (1, 4),(3, 4),(4, 4),(5, 4),(6, 4),(8, 4),(9, 4),(10, 4),(11, 4),(12, 4),(14, 4),(15, 4),(17, 4),(18, 4),(19, 4),(20, 4),(21, 4),(23, 4),(24, 4),(25, 4),(26, 4),(28, 4),
           (1, 5),(28, 5),
           (1, 6),(3, 6),(4, 6),(5, 6),(6, 6),(8, 6),(9, 6),(11, 6),(12, 6),(13, 6),(14, 6),(15, 6),(16, 6),(17, 6),(18, 6),(20, 6),(21, 6),(23, 6),(24, 6),(25, 6),(26, 6),(28, 6),
           (1, 7),(3, 7),(4, 7),(5, 7),(6, 7),(8, 7),(9, 7),(11, 7),(12, 7),(13, 7),(14, 7),(15, 7),(16, 7),(17, 7),(18, 7),(20, 7),(21, 7),(23, 7),(24, 7),(25, 7),(26, 7),(28, 7),
           (1, 8),(8, 8),(9, 8),(14, 8),(15, 8),(20, 8),(21, 8),(28, 8),
           (1, 9),(2, 9),(3, 9),(4, 9),(5, 9),(6, 9),(8, 9),(9, 9),(10, 9),(11, 9),(12, 9),(14, 9),(15, 9),(17, 9),(18, 9),(19, 9),(20, 9),(21, 9),(23, 9),(24, 9),(25, 9),(26, 9),(27, 9),(28, 9),
           (6, 10),(8, 10),(9, 10),(10, 10),(11, 10),(12, 10),(14, 10),(15, 10),(17, 10),(18, 10),(19, 10),(20, 10),(21, 10),(23, 10),
           (6, 11),(8, 11),(9, 11),(20, 11),(21, 11),(23, 11),
           (6, 12),(8, 12),(9, 12),(11, 12),(12, 12),(13, 12),(16, 12),(17, 12),(18, 12),(20, 12),(21, 12),(23, 12),
           (1, 13),(2, 13),(3, 13),(4, 13),(5, 13),(6, 13),(8, 13),(9, 13),(11, 13),(18, 13),(20, 13),(21, 13),(23, 13),(24, 13),(25, 13),(26, 13),(27, 13),(28, 13),
           (11, 14),(18, 14),
           (1, 15),(2, 15),(3, 15),(4, 15),(5, 15),(6, 15),(8, 15),(9, 15),(11, 15),(18, 15),(20, 15),(21, 15),(23, 15),(24, 15),(25, 15),(26, 15),(27, 15),(28, 15),
           (6, 16),(8, 16),(9, 16),(11, 16),(12, 16),(13, 16),(14, 16),(15, 16),(16, 16),(17, 16),(18, 16),(20, 16),(21, 16),(23, 16),
           (6, 17),(8, 17),(9, 17),(20, 17),(21, 17),(23, 17),
           (6, 18),(8, 18),(9, 18),(11, 18),(12, 18),(13, 18),(14, 18),(15, 18),(16, 18),(17, 18),(18, 18),(20, 18),(21, 18),(23, 18),
           (1, 19),(2, 19),(3, 19),(4, 19),(5, 19),(6, 19),(8, 19),(9, 19),(11, 19),(12, 19),(13, 19),(14, 19),(15, 19),(16, 19),(17, 19),(18, 19),(20, 19),(21, 19),(23, 19),(24, 19),(25, 19),(26, 19),(27, 19),(28, 19),
           (1, 20),(14, 20),(15, 20),(28, 20),
           (1, 21),(3, 21),(4, 21),(5, 21),(6, 21),(8, 21),(9, 21),(10, 21),(11, 21),(12, 21),(14, 21),(15, 21),(17, 21),(18, 21),(19, 21),(20, 21),(21, 21),(23, 21),(24, 21),(25, 21),(26, 21),(28, 21),
           (1, 22),(3, 22),(4, 22),(5, 22),(6, 22),(8, 22),(9, 22),(10, 22),(11, 22),(12, 22),(14, 22),(15, 22),(17, 22),(18, 22),(19, 22),(20, 22),(21, 22),(23, 22),(24, 22),(25, 22),(26, 22),(28, 22),
           (1, 23),(5, 23),(6, 23),(23, 23),(24, 23),(28, 23),
           (1, 24),(2, 24),(3, 24),(5, 24),(6, 24),(8, 24),(9, 24),(11, 24),(12, 24),(13, 24),(14, 24),(15, 24),(16, 24),(17, 24),(18, 24),(20, 24),(21, 24),(23, 24),(24, 24),(26, 24),(27, 24),(28, 24),
           (1, 25),(2, 25),(3, 25),(5, 25),(6, 25),(8, 25),(9, 25),(11, 25),(12, 25),(13, 25),(14, 25),(15, 25),(16, 25),(17, 25),(18, 25),(20, 25),(21, 25),(23, 25),(24, 25),(26, 25),(27, 25),(28, 25),
           (1, 26),(8, 26),(9, 26),(14, 26),(15, 26),(20, 26),(21, 26),(28, 26),
           (1, 27),(3, 27),(4, 27),(5, 27),(6, 27),(7, 27),(8, 27),(9, 27),(10, 27),(11, 27),(12, 27),(14, 27),(15, 27),(17, 27),(18, 27),(19, 27),(20, 27),(21, 27),(22, 27),(23, 27),(24, 27),(25, 27),(26, 27),(28, 27),
           (1, 28),(3, 28),(4, 28),(5, 28),(6, 28),(7, 28),(8, 28),(9, 28),(10, 28),(11, 28),(12, 28),(14, 28),(15, 28),(17, 28),(18, 28),(19, 28),(20, 28),(21, 28),(22, 28),(23, 28),(24, 28),(25, 28),(26, 28),(28, 28),
           (1, 29),(28, 29),
           (1, 30),(2, 30),(3, 30),(4, 30),(5, 30),(6, 30),(7, 30),(8, 30),(9, 30),(10, 30),(11, 30),(12, 30),(13, 30),(14, 30),(15, 30),(16, 30),(17, 30),(18, 30),(19, 30),(20, 30),(21, 30),(22, 30),(23, 30),(24, 30),(25, 30),(26, 30),(27, 30),(28, 30)]




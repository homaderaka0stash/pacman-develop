from search.dijkstra import *


class GetWay:
    def __init__(self, ghost_x, ghost_y, pacman_x, pacman_y):
        self.ghost_x = ghost_x
        self.ghost_y = ghost_y
        self.pacman_x = pacman_x
        self.pacman_y = pacman_y

    def get_way(self):
        came_from, cost_so_far = dijkstra_search(g, (self.ghost_x, self.ghost_y), (self.pacman_x, self.pacman_y))
        # print(draw_grid(g, width=2, path=reconstruct_path(came_from, start=(self.ghost_x, self.ghost_y), goal=(self.pacman_x, self.pacman_y))))
        path = reconstruct_path(came_from, start=(self.ghost_x, self.ghost_y), goal=(self.pacman_x, self.pacman_y))
        path_in_dirs = []
        for i in range(len(path) - 1):
            if (path[i][1] < path[i + 1][1]):
                path_in_dirs.append("down")
            elif (path[i][1] > path[i + 1][1]):
                path_in_dirs.append("up")
            elif (path[i][0] > path[i + 1][0]):
                path_in_dirs.append("left")
            elif (path[i][0] < path[i + 1][0]):
                path_in_dirs.append("right")
        return (path_in_dirs)




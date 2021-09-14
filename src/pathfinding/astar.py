# Credit for this: ryancollingwood
# as found at https://gist.github.com/ryancollingwood/32446307e976a11a1185a5394d6657bc
from warnings import warn
import heapq

from colorama import Fore


class Node:
    """
    A node class for A* Pathfinding
    """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __repr__(self):
        return f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"

    def __lt__(self, other):
        return self.f < other.f

    def __gt__(self, other):
        return self.f > other.f


def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]


def astar(maze, start, end, allow_diagonal_movement=False):
    """
    Returns a list of tuples as a path from the given start to the given end in the given maze
    :param maze:
    :param start:
    :param end:
    :return:
    """

    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    open_list = []
    closed_list = []

    heapq.heapify(open_list)
    heapq.heappush(open_list, start_node)

    outer_iterations = 0
    max_iterations = (len(maze[0]) * len(maze))

    adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0),)
    if allow_diagonal_movement:
        adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0),
                            (-1, -1), (-1, 1), (1, -1), (1, 1),)

    while len(open_list) > 0:
        outer_iterations += 1

        if outer_iterations > max_iterations:
            return return_path(current_node)

        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        if current_node == end_node:
            return return_path(current_node)

        children = []

        for new_position in adjacent_squares:

            node_position = (
                current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue

            if maze[node_position[0]][node_position[1]] != 0:
                continue

            new_node = Node(current_node, node_position)

            children.append(new_node)

        for child in children:
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                (child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            if len([open_node for open_node in open_list if
                    child.position == open_node.position and child.g > open_node.g]) > 0:
                continue

            heapq.heappush(open_list, child)

    return None


def run(maze, start, end, game, last, draw=False):
    step_min = 5000
    best_path = astar(maze, start, end[0])
    best_end = (0, 0)
    can = True
    path_len = 0

    for i in range(1, len(end)):
        path = astar(maze, start, end[i])
        if path != None and len(path) < step_min:
            path_len = len(path) - 1
            for j in range(len(last)):
                if path[path_len] == last[j]:
                    can = False
            if can:
                step_min = len(path)
                best_path = path
                best_end = end[i]
            can = True

    last.pop()
    last.insert(0, best_end)

    if draw:
        for i in range(1, len(best_path)):
            game.matrix_add(best_path[i][1], best_path[i][0], 'C')

    print(Fore.BLUE + "-----------------------------------------------")
    print(Fore.GREEN + "> Find a path ! " + str(best_path))
    print(Fore.BLUE + "-----------------------------------------------")
    return best_path, last

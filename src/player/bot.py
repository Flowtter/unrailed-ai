import pydirectinput
import time
import random
from pathfinding import astar

from colorama import Fore

SPEED = 0.105
TIME_OFF = 0.15
BREAK_TIME = 1.8


class Bot:
    def __init__(self, l):
        self.should_stop = False
        self.l = l

    def input(self, key, t):
        print("Your time to shine", key)
        pydirectinput.keyDown(key)
        time.sleep(t)
        pydirectinput.keyUp(key)

    def movement(self, key):
        self.input(key, SPEED)
        time.sleep(TIME_OFF)

    def path(self, start, obj, g, draw, last):
        original = g.get_binary_matrix()

        if obj == "axe":
            axe = g.get_pos('A')
            return astar.run(original, start, axe, g, last)

        elif obj == "pickaxe":
            pickaxe = g.get_pos('I')
            return astar.run(original, start, pickaxe, g, last)

        elif obj == "tree":
            tree = g.get_pos('t')
            return astar.run(original, start, tree, g, last)

        elif obj == "rock":
            rock = g.get_pos('k')
            return astar.run(original, start, rock, g, last)

        else:
            raise Exception("Path: not a valid object")

    def move(self, obj, game, draw, player_pos, last):
        movement, last = self.path(player_pos, obj, game, draw, last)
        if movement != None:
            for vect in movement:
                x = player_pos[0] - vect[0]
                y = player_pos[1] - vect[1]
                player_pos = vect
                if y > 0:
                    self.movement(self.l.left)
                elif y < 0:
                    self.movement(self.l.right)
                elif x < 0:
                    self.movement(self.l.down)
                elif x > 0:
                    self.movement(self.l.up)
            else:
                print(Fore.GREEN + f"> I got a path to {obj} !")

        else:
            print(Fore.RED + "E: Movement is null!")

        return player_pos, last

    def breaking(self, obj, player_pos, game):
        game.matrix[player_pos[0]][player_pos[1]] = 'M'

        if player_pos[0] - 1 > 0 and game.matrix[player_pos[0] - 1][player_pos[1]] == obj:
            self.input(self.l.up, BREAK_TIME)
            return (player_pos[0] - 1, player_pos[1])

        elif player_pos[0] + 1 < len(game.matrix) and game.matrix[player_pos[0] + 1][player_pos[1]] == obj:
            self.input(self.l.down, BREAK_TIME)
            return (player_pos[0] + 1, player_pos[1])

        elif player_pos[1] - 1 > 0 and game.matrix[player_pos[0]][player_pos[1] - 1] == obj:
            self.input(self.l.left, BREAK_TIME)
            return (player_pos[0], player_pos[1] - 1)

        elif player_pos[1] + 1 < len(game.matrix[0]) and game.matrix[player_pos[0]][player_pos[1] + 1] == obj:
            self.input(self.l.right, BREAK_TIME)
            return (player_pos[0], player_pos[1] + 1)

        print(Fore.RED + f"E: I can't reach {obj}")
        return None

    def rnd(self, r):
        for i in range(r):
            r = random.randrange(0, 4, 1)
            if r == 0:
                self.movement(self.l.left)
            elif r == 1:
                self.movement(self.l.right)
            elif r == 2:
                self.movement(self.l.down)
            elif r == 3:
                self.movement(self.l.up)

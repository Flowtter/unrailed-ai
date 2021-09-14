import numpy as np
from threading import Thread
import time
from colorama import Fore

import functions


class game_map:
    def __init__(self, height, width, cell_size_x, cell_size_y, refresh_rate):
        self.height = height
        self.width = width
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y

        self.wait_time = 1/refresh_rate

        self.should_stop = False

        self.matrix = []
        self.binary = []

        self.im = np.zeros((self.height * self.cell_size_y,
                           self.width * self.cell_size_x, 3), np.uint8)

    def start(self):
        self._thread = Thread(target=self.update,
                              name=self._thread_name, args=())
        self._thread.daemon = True
        self._thread.start()
        return self

    def update(self):
        while not self.should_stop:
            start = time.time()

            self.frame = 1

            delta = time.time() - start
            if delta < self.wait_time:
                time.sleep(self.wait_time - delta)

    def read(self):
        return self.frame

    def stop(self):
        self.should_stop = True
        self._thread.join()

    def init_matrix(self):
        matrix = []
        for i in range(self.height):
            local = []
            for j in range(self.width):
                local.append('N')
            matrix.append(local)
        self.matrix = np.array(matrix)

    def print_matrix(self):
        for j in range(len(self.matrix)):
            x = ""
            for i in range(len(self.matrix[0])):
                x += self.matrix[j][i] + " "
            print(Fore.WHITE + x)

    def get_matrix(self):
        return self.matrix

    def get_binary_matrix(self):
        binary = []
        for j in range(len(self.matrix)):
            local = []
            for i in range(len(self.matrix[0])):
                local.append('-1')
            binary.append(local)

        for j in range(len(self.matrix)):
            for i in range(len(self.matrix[0])):
                if self.matrix[j][i] == 'P' or \
                        self.matrix[j][i] == 'M' or  \
                        self.matrix[j][i] == 't' or  \
                        self.matrix[j][i] == 'k' or  \
                        self.matrix[j][i] == 'A' or \
                        self.matrix[j][i] == 'I':
                    binary[j][i] = 0
                else:
                    binary[j][i] = 1
        self.binary = binary
        return self.binary

    def print_binary(self):
        for j in range(len(self.binary)):
            x = ""
            for i in range(len(self.binary[0])):
                x += str(self.binary[j][i]) + " "
            print(Fore.WHITE + x)

    def matrix_add(self, i, j, letter):
        if i < len(self.matrix[0]) and j < len(self.matrix):
            self.matrix[j][i] = letter

    def draw_matrix(self):

        size_x = self.width * self.cell_size_x
        size_y = self.height * self.cell_size_y

        for y in range(0, size_y, self.cell_size_y):
            for x in range(0, size_x, self.cell_size_x):
                functions.set_pixel_color(self.im, x, y, (0, 255, 0))

        for j in range(len(self.matrix)):
            for i in range(len(self.matrix[0])):
                self.draw_call(self.matrix[j][i], j, i)
                self.draw_path(self.matrix[j][i], j, i)

    def draw_call(self, e, j, i):
        if e == 'M':
            self.draw(i, j, (86, 215, 156))
        elif e == 'T':
            self.draw(i, j, (109, 196, 63))
        elif e == 't':
            self.draw(i, j, (70, 156, 23))
        elif e == 'K':
            self.draw(i, j, (118, 150, 182))
        elif e == 'k':
            self.draw(i, j, (80, 100, 140))
        elif e == 'B':
            self.draw(i, j, (65, 65, 65))
        elif e == 'R':
            self.draw(i, j, (243, 255, 114))
        elif e == '0':
            self.draw(i, j, (0, 0, 0))
        elif e == 'P':
            self.draw(i, j, (0, 100, 255))
        elif e == 'A':
            self.draw(i, j, (150, 100, 200))
        elif e == 'I':
            self.draw(i, j, (200, 100, 150))
        elif e == 'D':
            self.draw(i, j, (255, 255, 255))  # Debug
        else:
            self.draw(i, j, (155, 0, 155))

    def draw_path(self, e, j, i):
        if e == 'C':
            self.draw(i, j, (255, 255, 255))
        elif e == 'U':
            self.draw(i, j, (255, 0, 0))

    def replace_letter(self, new, old, check):

        for j in range(len(self.matrix)):
            for i in range(len(self.matrix[0])):
                if self.matrix[j][i] == new:
                    self.matrix[j][i] = old

        for j in range(len(self.matrix)):
            for i in range(len(self.matrix[0])):
                if self.matrix[j][i] == old and i-1 > 0 and self.matrix[j][i-1] == check:
                    self.matrix[j][i] = new
                elif self.matrix[j][i] == old and i+1 < len(self.matrix[0]) and self.matrix[j][i+1] == check:
                    self.matrix[j][i] = new

                elif self.matrix[j][i] == old and j-1 > 0 and self.matrix[j-1][i] == check:
                    self.matrix[j][i] = new
                elif self.matrix[j][i] == old and j+1 < len(self.matrix) and self.matrix[j+1][i] == check:
                    self.matrix[j][i] = new

    def get_pos(self, e):
        result = []
        for j in range(len(self.matrix)):
            for i in range(len(self.matrix[0])):
                if self.matrix[j][i] == e:
                    result.append((j, i))
        return result

    def draw_cell(self):
        size_x = self.width * self.cell_size_x
        size_y = self.height * self.cell_size_y

        for y in range(0, size_y):
            for x in range(0, size_x):
                if x % self.cell_size_x == 0 or y % self.cell_size_y == 0:
                    functions.set_pixel_color(self.im, x, y, (0, 255, 0))
                else:
                    functions.set_pixel_color(self.im, x, y, (155, 0, 155))

    def draw(self, i, j, color):

        for y in range(1, self.cell_size_y):
            for x in range(1, self.cell_size_x):
                functions.set_pixel_color(
                    self.im, x+i*self.cell_size_x, y+j*self.cell_size_y, color)

    def draw_image(self):
        return self.im

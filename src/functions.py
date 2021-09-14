import cv2
import numpy as np

from detection import environment, from_img
from constants import *

from colorama import Fore


def test(im, p_bot, game, last, mode, change, tried, random):
    set_array_from_bin(game, im)

    if random:
        player_pos = p_bot.rnd(15)
        return 0, last

    if change == False:
        try:
            if mode == "rock":
                player_pos = game.get_pos('P')[0]
                player_pos, last = p_bot.move("rock", game, False, player_pos,
                                              last)
                p_bot.breaking('K', player_pos, game)
            else:
                player_pos = game.get_pos('P')[0]
                player_pos, last = p_bot.move("tree", game, False, player_pos,
                                              last)
                p_bot.breaking('T', player_pos, game)
            return 0, last
        except:
            print(Fore.RED + "> PLAYER NOT FOUND, TRYING TO REVERSE PATH... ")
            player_pos = p_bot.rnd(3)
            return 0, last

    else:
        try:
            player_pos = game.get_pos('P')[0]
            if mode == "tree":
                player_pos = p_bot.move("pickaxe", game, False, player_pos,
                                        last)
                print(Fore.YELLOW +
                      "> FIND THE PICKAXE, WAITING FOR CONFIRMATION...")
                return -1, last

            elif mode == "rock":
                player_pos = p_bot.move("axe", game, False, player_pos, last)
                print(Fore.YELLOW +
                      "> FIND THE AXE, WAITING FOR CONFIRMATION...")
                return -1, last
        except:
            if mode == "tree":
                print(Fore.RED + "> COULD NOT FIND THE PICKAXE, RETRYING...")
            else:
                print(Fore.RED + "> COULD NOT FIND THE AXE, RETRYING...")
            return tried + 1, last


def set_array_from_bin(game, im):
    im_hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

    bin_player = environment.get_bin(im, im_hsv, HSV_PLAYER)
    arrplayer = element(bin_player, 3)

    bin_green = environment.get_bin(im, im_hsv, HSV_MAP, (50, 0))
    bin_trees = environment.get_bin(im, im_hsv, HSV_TREES, (34, 23))
    bin_rocks = environment.get_bin(im, im_hsv, HSV_ROCK, (15, 0))
    bin_black = environment.get_bin(im, im_hsv, HSV_BROCK, (15, 0))
    bin_river = environment.get_bin(im, im_hsv, HSV_RIVER, (20, 0))
    bin_terrain = environment.get_bin(im, im_hsv, HSV_TERRAIN, (2, 0), 1)

    axe_pos = from_img.get_img_minimap(cv2.cvtColor(
        im, cv2.COLOR_BGR2GRAY), AXE_TEMPLATE, AXE_TRESH)
    pickaxe_pos = from_img.get_img_minimap(cv2.cvtColor(
        im, cv2.COLOR_BGR2GRAY), PICKAXE_TEMPLATE, PICKAXE_TEMPLATE)

    arrtree = element(bin_trees,  3)
    arrrock = element(bin_rocks,  5)
    arrblack = element(bin_black,  3)
    arrriver = element(bin_river,  3)
    arrmain = element(bin_green,  3)

    arrout = element(bin_terrain,  6)

    unpack_array(arrrock, 'K', game)
    unpack_array(arrmain, 'M', game)
    unpack_array(arrriver, 'R', game)
    unpack_array(arrblack, 'B', game)
    unpack_array(arrtree, 'T', game)
    unpack_array(arrout, '0', game)

    unpack_array(arrplayer, 'P', game, (0, -1))

    if pickaxe_pos != None:
        for i in range(len(axe_pos)):
            axe_pos[i] = (axe_pos[i][0] // 22, axe_pos[i][1] // 16)
            unpack_array(axe_pos, 'A', game, (0, -1))

    if pickaxe_pos != None:
        for i in range(len(pickaxe_pos)):
            pickaxe_pos[i] = (pickaxe_pos[i][0] // 22, pickaxe_pos[i][1] // 16)
            unpack_array(pickaxe_pos, 'I', game, (0, -1))

    game.replace_letter('t', 'M', 'T')
    game.replace_letter('k', 'M', 'K')

    for i in range(2):
        for j in range(20):
            game.matrix_add(i, j, '0')
    for j in range(20):
        game.matrix_add(35, j, '0')


def element(bin, nb):
    result = []
    for x in range(22, 810, 22):
        for y in range(0, 320, 16):
            arr0 = get_pixel_color(bin, x - 10, y)
            arr1 = get_pixel_color(bin, x - 5, y)
            arr2 = get_pixel_color(bin, x + 0, y)

            arr3 = get_pixel_color(bin, x - 10, y + 12)
            arr4 = get_pixel_color(bin, x - 5, y + 12)
            arr5 = get_pixel_color(bin, x + 0, y + 12)

            arr6 = get_pixel_color(bin, x - 10, y + 7)
            arr7 = get_pixel_color(bin, x - 5, y + 7)
            arr8 = get_pixel_color(bin, x + 0, y + 7)

            arrE = [arr0, arr1, arr2, arr3, arr4, arr5, arr6, arr7, arr8]
            somme = 0
            for i in range(len(arrE)):
                somme += (arrE[i][0] != 0 and arrE[i][1] != 0
                          and arrE[i][2] != 0)
            if somme >= nb:
                result.append([x // 22 - 1,
                               y // 16])  # minus one because magic

    return result


def unpack_array(arr, vall, game, offset=(0, 0)):
    for e in arr:
        pass
        if e[0] - offset[0] > 0 and e[0] - offset[0] < len(game.matrix[0]) \
                and e[1] - offset[1] > 0 and e[1] - offset[1] < len(game.matrix):
            game.matrix_add(e[0] - offset[0], e[1] - offset[1], vall)


def draw(im):
    im_hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

    # from_img.draw_contours(im, cv2.cvtColor(
    #    im, cv2.COLOR_BGR2GRAY), AXE_TEMPLATE, AXE_TRESH, (0, 0, 255))
    # from_img.draw_contours(im, cv2.cvtColor(
    #    im, cv2.COLOR_BGR2GRAY), PICKAXE_TEMPLATE, PICKAXE_TRESH, (0, 255, 255))

    environment.get_bin(im, im_hsv, HSV_PLAYER, (0, 0), 0, 1, (255, 0, 0))
    # environment.get_bin(im, im_hsv, HSV_MAP, (50, 0), 0, 1, (100,100,175))

    # environment.get_bin(im, im_hsv, HSV_TREES, (34, 23), 0, 1, (100,255,0))
    # environment.get_bin(im, im_hsv, HSV_ROCK, (15, 0), 0, 1, (150,150,150))
    # environment.get_bin(im, im_hsv, HSV_BROCK, (15, 0), 0, 1, (50,50,50))
    # environment.get_bin(im, im_hsv, HSV_RIVER, (20, 0), 0, 1, (255,100,0))

    # environment.get_bin(im, im_hsv, HSV_TERRAIN, (2, 0), 1, 1, (0,0,0))


def cut(im):
    im = rotate(im, -8)
    x, y = 0, 125
    h, w = 320, 800
    im = im[y:y + h, x:x + w]

    rows, cols = im.shape[:-1]

    a, b, c = [382, 52], [500, 50], [400, 200]
    offsetx = 20
    d, e, f = [382 + offsetx, 52], [500 + offsetx, 50], [400, 200]

    pts1 = np.float32([a, b, c])
    pts2 = np.float32([d, e, f])

    dst = im  # Uh Oh

    M = cv2.getAffineTransform(pts1, pts2)
    dst = cv2.warpAffine(im, M, (cols, rows))

    return dst


def grid(im):
    tiny_offset = 0

    for x in range(5, 900, 22):
        tiny_offset += 0.1
        for y in range(0, 400):
            im = set_pixel_color(im, x + int(tiny_offset), y, (100, 0, 100))

    for y in range(0, 400, 16):
        for x in range(0, 900):
            im = set_pixel_color(im, x, y, (100, 0, 100))


def rotate(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image,
                            rot_mat,
                            image.shape[1::-1],
                            flags=cv2.INTER_LINEAR)
    return result


def get_pixel_color(im, x, y):
    """get the pixel color"""
    rows, cols = im.shape[:-1]
    if x < 0 and y < 0:
        raise Exception("get pixel: coordinates need to be positive!")
    if x < cols and y < rows:
        return im[y, x]
    raise Exception("get pixel: x and y out of range!")


def set_pixel_color(im, x, y, color):
    """set the pixel color"""
    rows, cols = im.shape[:-1]
    if x < 0 and y < 0:
        raise Exception("get pixel: coordinates need to be positive!")
    if x < cols and y < rows:
        im[y, x] = color
        return im
    return im

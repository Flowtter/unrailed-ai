import cv2
import numpy as np


def __remove_all_from_bin_image(bin_image, nb_components, stats, w, h, n):
    """Sets everything but terrain to 0 in binary image"""
    for i in range(nb_components):
        if stats[i][2] < w // n[0] or (n[1] and stats[i][3] < h // n[1]):
            for y in range(stats[i][1], stats[i][1] + stats[i][3] + 1):
                for x in range(stats[i][0], stats[i][0] + stats[i][2] + 1):
                    if y >= 0 and x >= 0 and y < h and x < w:
                        bin_image[y][x] = 0


def get_bin(image, hsv_image, HSV_TABLE, remove_value=(0, 0), terrain=False, draw=False, color=(0, 0, 0)):
    """get contours of the terrain found in image"""
    h, w = image.shape[:-1]
    for i in range(len(HSV_TABLE)):
        if i == 0:
            bin_image = cv2.inRange(
                hsv_image, HSV_TABLE[0][0], HSV_TABLE[0][1])
        else:
            bin_image += cv2.inRange(hsv_image,
                                     HSV_TABLE[i][0], HSV_TABLE[i][1])

    if remove_value[0]:
        nb_components, _, stats, _ = cv2.connectedComponentsWithStats(
            bin_image, 8, cv2.CV_32S)
        __remove_all_from_bin_image(
            bin_image, nb_components, stats, w, h, remove_value)
    dilated_bin_image = cv2.dilate(bin_image, np.ones((3, 3), np.uint8))
    if terrain:  # assumption seems wrong. TODO: verify
        dilated_bin_image = cv2.bitwise_not(
            dilated_bin_image, dilated_bin_image)

    if draw:
        contours, _ = cv2.findContours(dilated_bin_image,
                                       cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(image, contours, -1, color, 3)
    return cv2.bitwise_and(image, image, mask=dilated_bin_image)

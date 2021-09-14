import cv2
import numpy as np
from colorama import Fore


def get_img_location(image_gray, template, treshold):
    """Apply template matching to gray image
       and return img location"""
    result = cv2.matchTemplate(image_gray, template, cv2.TM_CCOEFF_NORMED)
    return np.where(result >= treshold)


def draw_contours(image, image_gray, template, treshold, color):
    """Draws the contours of the object found in image"""
    height, width = template.shape
    try:
        for point in zip(*get_img_location(image_gray, template, treshold)[::-1]):
            cv2.rectangle(image, (point[0] - 2, point[1] - 2),
                          (point[0] + width + 2, point[1] + height + 2), color,
                          2)
    except:
        print(Fore.RED + "draw_contour: Could not find the object")


def get_img_minimap(image_gray, template, treshold):
    result = []
    height, width = template.shape
    try:
        for point in zip(*get_img_location(image_gray, template, treshold)[::-1]):
            result.append((point[0] + width // 2,
                          point[1] + height // 2))
        return result
    except:
        print(Fore.RED + "get_img_minimap: Could not find the object")

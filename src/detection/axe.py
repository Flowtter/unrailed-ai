import cv2
import numpy as np

template = cv2.imread("template_axe.png", cv2.IMREAD_GRAYSCALE)
height, width = template.shape


def get_axe_location(image_gray):
    """Apply template matching to gray image
       and return axe location"""

    result = cv2.matchTemplate(image_gray, template, cv2.TM_CCOEFF_NORMED)

    location = np.where(result >= 0.85)
    return location


def draw_contours(image, image_gray, color=(150, 100, 200)):
    """Draws the contours of the axes found in image"""

    cste_max = 500
    try:
        for point in zip(*get_axe_location(image_gray)[::-1]):
            cv2.rectangle(image, (point[0] - 2, point[1] - 2),
                          (point[0] + width + 2, point[1] + height + 2), color,
                          2)

    except:
        print("draw_contour: Could not find the axe")


def get_axe_minimap(image, image_gray):
    cste_max = 500
    result = []

    try:
        for point in zip(*get_axe_location(image_gray)[::-1]):
            result.append((point[0] + width // 2, point[1] + height // 2))
        return result
    except:
        print("get_axe_minimap: Could not find the axe")

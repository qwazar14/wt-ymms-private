import random

import cv2
import numpy as np
from PIL import ImageGrab




# def get_screenshot(): ### DEBUG
#     path = f'images/maps/new_map ({4}).png'
#     image = cv2.imread(path)
#     image = crop_screenshot(image)
#     image = np.uint8(image)
#     return image

def get_screenshot():
    im = ImageGrab.grab()
    im.save('temp.png')
    image = cv2.imread('temp.png')
    image = crop_screenshot(image)
    image = np.uint8(image)
    return image


def crop_screenshot(image):
    y = 620
    x = 1440
    h = image.shape[1]
    w = image.shape[0]
    cropped = image[y:y + h, x:x + w]
    cropped = cv2.rotate(cropped, cv2.ROTATE_180)
    cropped = cropped[28:28 + cropped.shape[1], 48:48 + cropped.shape[0]]
    cropped = cv2.rotate(cropped, cv2.ROTATE_180)
    return cropped

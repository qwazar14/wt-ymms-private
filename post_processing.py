import cv2

from screenshoter import get_screenshot


def gaussian_blur(image):
    return cv2.GaussianBlur(image, (5, 5), 0)


def get_mask_on_image(mask):
    return cv2.bitwise_and(get_screenshot(), get_screenshot(), mask=mask)


def sum_images(src1, src2):
    image = cv2.add(src1, src2)
    return image


def convert_from_hsv_to_rgb(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

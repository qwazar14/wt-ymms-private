import pytesseract
import cv2

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def find_text(image):
    return pytesseract.image_to_string(
        image, lang='eng',config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789')


def crop_image(image, x, y, w, h):
    return image[y:y + h, x:x + w]


def preprocess_image(image):
    prepared_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    prepared_image = cv2.bilateralFilter(prepared_image, 17, 17, 20)
    prepared_image = cv2.GaussianBlur(prepared_image, (3, 3), 0)

    prepared_image = cv2.adaptiveThreshold(prepared_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 33, 6)
    return prepared_image

def get_scale(image):
    # image = cv2.imread('images/map1.png')
    cropped = crop_image(image, 330, 412, image.shape[1], image.shape[0])

    prep = preprocess_image(cropped)
    print('scale:', find_text(prep)[:3])
    cv2.imshow('prep', prep)


# print(find_text(get_screenshot()))

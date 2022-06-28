import math

import cv2
import numpy as np

import post_processing


class Mark:
    def __init__(self, yellow_mark_coordinates=0, player_mark_coordinates=0, map_number=1):
        self._yellow_mark_coordinates = yellow_mark_coordinates
        self._player_mark_coordinates = player_mark_coordinates
        self._map_number = map_number
        # self._map_scale = map_scale

    ### DEBUG
    def get_screenshot(self):  ### DEBUG
        path = f'images/maps/map ({self._map_number}).png'
        image = cv2.imread(path)
        image = crop_screenshot(image)
        image = np.uint8(image)
        return image

    # def get_screenshot():
    #     im = ImageGrab.grab()
    #     im.save('temp.png')
    #     image = cv2.imread('temp.png')
    #     image = crop_screenshot(image)
    #     image = np.uint8(image)
    #     # os.remove('temp.png')
    #     return image

    def get_yellow_mark_coordinates(self):
        return self._yellow_mark_coordinates

    def get_player_mark_coordinates(self):
        return self._player_mark_coordinates

    def set_masks(self):
        image = cv2.GaussianBlur(self.get_screenshot(), (5, 5), 0)  # блюрим изображение
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)  # переводим в HSV

        lower_yellow = np.array([50, 200, 100])  # тут HSV (0-179, 0-255, 0-255)
        upper_yellow = np.array([95, 255, 200])

        lower_player = np.array([22, 50, 230])
        upper_player = np.array([100, 255, 255])

        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)  # берем канал желтого
        mask_player = cv2.inRange(hsv, lower_player, upper_player)  # берем канал игрока
        self._yellow_mark_coordinates = get_mean_value(mask_yellow)  # Получаем среднее значение по маске
        self._player_mark_coordinates = get_mean_value(mask_player)  # Получаем среднее значение по маске

    def calc_distance(self, scale):
        yellow_mark = self._yellow_mark_coordinates  # координаты желтой метки
        player_mark = self._player_mark_coordinates  # координаты игрока
        try:
            #  Class 'int' does not define '__getitem__', so the '[]' operator cannot be used on its instances
            #  Я не ебу чего оно ругается. Пашет и на том - спасибо
            length_x = abs(yellow_mark[0] - player_mark[0])  # находим дистанцию по х
            length_y = abs(yellow_mark[1] - player_mark[1])  # находим дистанцию по у
            result = math.sqrt(length_x ** 2 + length_y ** 2)  # находим дистанцию по координатам
            # SQUARE_SIZE = 58  # Размер квадрата в пикселях

            # return int(result * scale / SQUARE_SIZE)   # 25/23
            return int(result * scale / 100 * 1.67)  # 30/18
            # return int(result * scale / 60 + scale / 100)   # 29/19

        except TypeError:
            return


def get_mean_value(mask):
    found_contours = cv2.findContours(mask.copy(), cv2.RETR_TREE,
                                      cv2.CHAIN_APPROX_SIMPLE)  # находим контуры
    try:
        contours = np.array(found_contours[0][0], dtype=object)  # преобразуем в массив
        contours = contours.mean(axis=0, keepdims=True)  # находим среднее значение
        int_counters = contours.astype(int)  # преобразуем в int
        return int_counters[0][0]  # возвращаем координаты
    except IndexError:
        return "No mark found"


def crop_screenshot(image):
    y = 620  # координаты области для обрезки
    x = 1440  # координаты области для обрезки
    h = image.shape[1]  # высота изображения
    w = image.shape[0]  # ширина изображения
    cropped = image[y:y + h, x:x + w]  # обрезаем изображение
    cropped = cv2.rotate(cropped, cv2.ROTATE_180)  # поворачиваем изображение
    cropped = cropped[28:28 + cropped.shape[1], 48:48 + cropped.shape[0]]  # обрезаем изображение
    cropped = cv2.rotate(cropped, cv2.ROTATE_180)  # поворачиваем изображение
    return cropped  # возвращаем обрезанное изображение

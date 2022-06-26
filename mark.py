import math

import cv2
import numpy as np

import post_processing
import screenshoter


class Mark:
    def __init__(self, yellow_mark_coordinates=0, player_mark_coordinates=0, map_scale=0):
        self._yellow_mark_coordinates = yellow_mark_coordinates
        self._player_mark_coordinates = player_mark_coordinates
        self._map_scale = map_scale

    def get_yellow_mark_coordinates(self):
        return self._yellow_mark_coordinates

    def get_player_mark_coordinates(self):
        return self._player_mark_coordinates

    def set_map_scale(self, map_scale):
        self._map_scale = map_scale

    def get_map_scale(self):
        return self._map_scale

    def set_masks(self):
        image = post_processing.gaussian_blur(screenshoter.get_screenshot())  # убираем мелкий мусор
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

        lower_yellow = np.array([50, 200, 100])  # тут HSV (0-179, 0-255, 0-255)
        upper_yellow = np.array([95, 255, 200])

        lower_player = np.array([22, 50, 230])
        upper_player = np.array([100, 255, 255])

        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
        mask_player = cv2.inRange(hsv, lower_player, upper_player)
        self._yellow_mark_coordinates = get_mean_value(mask_yellow)  # Вносим значения
        self._player_mark_coordinates = get_mean_value(mask_player)

    def calc_distance(self):
        yellow_mark = self._yellow_mark_coordinates
        player_mark = self._player_mark_coordinates
        try:
            #  Class 'int' does not define '__getitem__', so the '[]' operator cannot be used on its instances
            #  Я не ебу чего оно ругается. Пашет и на том - спасибо
            length_x = abs(yellow_mark[0] - player_mark[0])  # находим дистанцию по х
            length_y = abs(yellow_mark[1] - player_mark[1])  # находим дистанцию по у

            # print('length_x: ', length_x, 'length_y: ', length_y)

            result = pow(length_x, 2) + pow(length_y, 2)  # пифагор
            scale = self._map_scale

            # корень суммы квадратов катетов умножаем на 417(ТАК НАДА) деленное на масштаб и умножаем на 2
            return int(math.sqrt(result) * (417 / scale) * 2)
        except TypeError:
            return


def get_mean_value(mask):
    found_contours = cv2.findContours(mask.copy(), cv2.RETR_TREE,
                                      cv2.CHAIN_APPROX_SIMPLE)
    try:
        contours = np.array(found_contours[0][0], dtype=object)
        contours = contours.mean(axis=0, keepdims=True)  # Находим среднее значение массива по вертикали
        int_counters = contours.astype(int)
        return int_counters[0][0]
    except IndexError:
        return "No mark found"

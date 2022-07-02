import json
import math
import os

import cv2
import numpy as np


class Mark:
    def __init__(self, yellow_mark_coordinates=0, player_mark_coordinates=0, map_number=6, map_scale=200,
                 square_size=58):
        self._yellow_mark_coordinates = yellow_mark_coordinates
        self._player_mark_coordinates = player_mark_coordinates
        self._map_number = map_number
        self._map_scale = map_scale
        self._square_size = square_size
        self._path = 'D:\Steam\steamapps\common\War Thunder\Screenshots'

    # ### DEBUG
    # def get_screenshot(self):  ### DEBUG
    #     path = f'images/maps/map ({self._map_number}).png'
    #     image = cv2.imread(path)
    #     image = crop_screenshot(image)
    #     image = np.uint8(image)
    #     return image

    # def get_screenshot(self):
    #     im = ImageGrab.grab()
    #     im.save('temp.png')
    #     image = cv2.imread('temp.png')
    #     image = crop_screenshot(image)
    #     image = np.uint8(image)
    #     # os.remove('temp.png')
    #     return image

    def __get_map_name(self):
        path = get_last_created_file(path=self._path,
                                     file_format='.blk')
        with open(path, 'r') as fp:
            # read line 8
            name = fp.readlines()[34]
            return name[45:-6]

    def get_screenshot(self):
        path = get_last_created_file(path=self._path,
                                     file_format='.png')
        path = self._path + '\\' + str(path)[11:-2]
        # print('path', path)
        image = cv2.imread(path)
        # print(type(image))
        image = crop_screenshot(image)
        image = np.uint8(image)

        return image

    def __parse_json(self):
        with open('maps.json', 'r') as fp:
            maps = json.load(fp)
        return maps

    def __parse_scale(self):
        return self.__parse_json()[self.__get_map_name()]['map_scale']

    def __parse_pixels(self):
        return self.__parse_json()[self.__get_map_name()]['pixel_per_side']+3

    def set_mask_for_borders(self):
        image = self.get_screenshot()
        # hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HLS_FULL)

        lower_border = np.array([0, 0, 0])
        upper_border = np.array([100, 100, 100])

        binary = cv2.inRange(image, lower_border, upper_border)

        cv2.imshow('image', binary)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def set_masks(self):
        image = cv2.GaussianBlur(self.get_screenshot(), (5, 5), 0)  # блюрим изображение
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)  # переводим в HSV

        lower_yellow = np.array([50, 200, 100])  # тут HSV (0-179, 0-255, 0-255)
        upper_yellow = np.array([95, 255, 200])

        lower_player = np.array([22, 50, 230])
        upper_player = np.array([100, 255, 255])
        # lower_player = np.array([109, 142, 142])
        # upper_player = np.array([255, 255, 255])
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)  # берем канал желтого
        mask_player = cv2.inRange(hsv, lower_player, upper_player)  # берем канал игрока
        self._yellow_mark_coordinates = get_mean_value(mask_yellow)  # Получаем среднее значение по маске
        self._player_mark_coordinates = get_mean_value(mask_player)  # Получаем среднее значение по маске

    def calc_distance(self):
        yellow_mark = self._yellow_mark_coordinates  # координаты желтой метки
        player_mark = self._player_mark_coordinates  # координаты игрока
        try:
            length_x = abs(yellow_mark[0] - player_mark[0])  # находим дистанцию по х
            length_y = abs(yellow_mark[1] - player_mark[1])  # находим дистанцию по у
            result = math.sqrt(length_x ** 2 + length_y ** 2)  # находим дистанцию по координатам
            # return int(result * int(self._map_scale) / int(self._square_size))  # 25/23
            return int(result * int(self.__parse_scale()) / int(self.__parse_pixels()))  # 25/23

        except Exception:
            return
        # return int(result * scale / 100 * 1.67)  # 30/18
        # return int(result * scale / 60 + scale / 100)   # 29/19


def get_mean_value(mask):
    found_contours = cv2.findContours(mask.copy(), cv2.RETR_TREE,
                                      cv2.CHAIN_APPROX_SIMPLE)  # находим контуры
    try:
        contours = np.array(found_contours[0][0], dtype=object)  # преобразуем в массив
        contours = contours.mean(axis=0, keepdims=True)  # находим среднее значение
        int_counters = contours.astype(int)  # преобразуем в int
        return int_counters[0][0]  # возвращаем координаты
    except IndexError:
        return


def crop_screenshot(image):
    y = 620  # координаты области для обрезки
    x = 1440  # координаты области для обрезки
    h = 1920  # высота изображения
    w = 1080  # ширина изображения
    cropped = image[y:y + h, x:x + w]  # обрезаем изображение
    cropped = cv2.rotate(cropped, cv2.ROTATE_180)  # поворачиваем изображение
    cropped = cropped[28:28 + cropped.shape[1], 48:48 + cropped.shape[0]]  # обрезаем изображение
    cropped = cv2.rotate(cropped, cv2.ROTATE_180)  # поворачиваем изображение
    return cropped  # возвращаем обрезанное изображение


def get_last_created_file(path: str = '.', file_format: str = '.blk') -> os.DirEntry or None:
    """ Возвращает последний созданный файл в папке нужного формата.
    :param path: Path to directory (default - '.')
    :param file_format: File format (default - '.png')
    :return: Last created file in directory or None
    """

    dir_iter = os.scandir(path)
    dir_list = list(dir_iter)
    for file in sorted(dir_list, key=lambda x: x.stat().st_ctime, reverse=True):
        if file.name.endswith(file_format):
            # print(file)
            return file

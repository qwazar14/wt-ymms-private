import configparser
import json
import math
import os
import sys

import cv2
import numpy as np
import requests


def get_game_path_from_config():
    """
    Получаем путь к игре из конфига
    :return: Путь к игре
    """
    config = configparser.ConfigParser()
    config.read("config.ini")
    path = config["DEFAULT"]["game_path"]
    path.replace("/", "\\")
    path = path + "/Screenshots"

    return path


def resource_path(relative_path):
    """
    Получаем путь к ресурсам
    :param relative_path: Путь к ресурсам
    :return: Путь к ресурсам
    """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class Mark:
    def __init__(
            self, yellow_mark_coordinates: int = 0, player_mark_coordinates: int = 0
    ):
        self._yellow_mark_coordinates = yellow_mark_coordinates
        self._player_mark_coordinates = player_mark_coordinates
        self._path = resource_path(get_game_path_from_config())

    def __get_map_name(self):
        """
        Получаем название карты
        :return: map_name
        """
        path = get_last_created_file(path=self._path, file_format=".blk")
        with open(path, "r") as fp:
            name = fp.readlines()[34]
            return name[45:-6]

    def __get_screenshot(self):
        """
        Получаем скриншот
        :return: screenshot
        """
        path = get_last_created_file(path=self._path, file_format=".png")
        path = self._path + "\\" + str(path)[11:-2]
        image = cv2.imread(path)
        image = crop_screenshot(image)
        image = np.uint8(image)
        return image

    def parse_json(self):
        """
        Получаем данные из json файла
        :return: json
        """
        r = requests.get("https://api.npoint.io/3c42d75c578515e52589")
        json.loads(r.text)
        maps = json.loads(r.text)

        # with open("maps.json", "r") as fp:
        #     maps = json.load(fp)
        return maps

    def parse_scale(self):
        """
        Получаем масштаб карты
        :return: scale
        """
        return self.parse_json()[self.__get_map_name()]["map_scale"]

    def parse_pixels(self):
        """
        Получаем количество пикселей в карте
        :return: pixels
        """
        return self.parse_json()[self.__get_map_name()]["pixel_per_side"] + 3

    def set_masks(self):
        """
        Устанавливаем маски для меток
        :return: Nothing
        """
        image = cv2.GaussianBlur(self.__get_screenshot(), (5, 5), 0)
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

        lower_yellow = np.array([50, 200, 100])  # тут HSV (0-179, 0-255, 0-255)
        upper_yellow = np.array([95, 255, 200])

        lower_player = np.array([22, 50, 230])
        upper_player = np.array([100, 255, 255])

        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
        mask_player = cv2.inRange(hsv, lower_player, upper_player)
        self._yellow_mark_coordinates = get_mean_value(mask_yellow)
        self._player_mark_coordinates = get_mean_value(mask_player)

    def calc_distance(self):
        """
        Получаем расстояние между метками
        :return: distance
        """
        yellow_mark = self._yellow_mark_coordinates
        player_mark = self._player_mark_coordinates
        try:
            length_x = abs(yellow_mark[0] - player_mark[0])
            length_y = abs(yellow_mark[1] - player_mark[1])
            result = math.sqrt(length_x ** 2 + length_y ** 2)
            print(result)
            return int(result * int(self.parse_scale()) / int(self.parse_pixels()))
        except Exception as e:
            print(e)
            return


def get_mean_value(mask):
    """
    Получаем среднее значение по маске
    :param mask: Маска в виде массива
    :return: Среднее значение по маске
    """
    found_contours = cv2.findContours(
        mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )
    try:
        contours = np.array(found_contours[0][0], dtype=object)
        contours = contours.mean(axis=0, keepdims=True)
        int_counters = contours.astype(int)
        return int_counters[0][0]
    except IndexError:
        return


def crop_screenshot(image):
    """
    Обрезаем изображение по координатам
    :param image: Изображение
    :return: Обрезанное изображение
    """
    y = 620  # координаты области для обрезки
    x = 1440  # координаты области для обрезки
    h = 1920  # высота изображения
    w = 1080  # ширина изображения
    cropped = image[y: y + h, x: x + w]
    cropped = cv2.rotate(cropped, cv2.ROTATE_180)
    cropped = cropped[28: 28 + cropped.shape[1], 48: 48 + cropped.shape[0]]
    cropped = cv2.rotate(cropped, cv2.ROTATE_180)
    return cropped


def get_last_created_file(
        path: str = ".", file_format: str = ".blk"
) -> os.DirEntry or None:
    """Возвращает последний созданный файл в папке нужного формата.
    :param path: Path to directory (default - '.')
    :param file_format: File format (default - '.png')
    :return: Last created file in directory or None
    """
    try:
        dir_iter = os.scandir(path)
        dir_list = list(dir_iter)
        for file in sorted(dir_list, key=lambda x: x.stat().st_ctime, reverse=True):
            if file.name.endswith(file_format):
                return file
    except:
        pass

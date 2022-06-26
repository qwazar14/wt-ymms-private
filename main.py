from time import sleep

from screenshoter import *
from mark import Mark

try:
    scale = input(
        "Масштабування мапи?: ")  # Отказался от OCR, для standalone-приложения гемморно и много ресов лишних жрёт
    marker = Mark()
    # marker.set_map_scale(scale)

    while True:
        marker.set_masks()  # Создаём маски

        # marker.get_yellow_mark_coordinates()  # Получаем средние координаты точек
        # marker.get_player_mark_coordinates()

        # print('player:', player)
        # print('yellow:', yellow)

        res = marker.calc_distance(scale)  # Считаем дистанцию
        print('result:', res)

        rand = random.random()  # На всякий случай
        sleep(rand)
except KeyboardInterrupt:
    exit(0)

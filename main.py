from time import sleep

from screenshoter import *
from mark import Mark

try:
    scale = input(
        "Масштабування мапи?: ")  # Отказался от OCR, для standalone-приложения гемморно и много ресов лишних жрёт
    marker = Mark(map_scale=scale)

    while True:
        marker.set_masks()  # Создаём маски

        yellow = marker.get_yellow_mark_coordinates()  # Получаем средние координаты точек
        player = marker.get_player_mark_coordinates()

        # print('player:', player)
        # print('yellow:', yellow)

        res = marker.calc_distance()  # Считаем дистанцию
        print('result:', res)

        rand = random.random()  # На всякий случай
        sleep(rand)
except KeyboardInterrupt:
    exit(0)

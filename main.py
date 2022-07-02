from time import sleep
import keyboard

from mark import Mark
from datetime import datetime

start = datetime.now()


class Main:
    def __init__(self):
        self.good = 0
        self.bad = 0

    def run(self, map_number, scale):
        mark = Mark(map_number=map_number)  # Создаем объект маркировки
        mark.set_masks()  # Получаем координаты меток
        res = mark.calc_distance(scale)  # Получаем расстояние между метками игрока и желтой меткой
        return map_number, res  # Возвращаем номер карты и расстояние


def main():
    marker = Mark()
    marker.set_masks()
    res = marker.calc_distance()
    if res is not None:
        print('result:', res)


while True:
    if keyboard.is_pressed('f12'):
        sleep(1.5)
        try:
            main()
        except Exception:
            sleep(0.5)
            main()

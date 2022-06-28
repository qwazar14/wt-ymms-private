from time import sleep

from mark import Mark
from datetime import datetime
start=datetime.now()

class Main:
    def __init__(self):
        self.good = 0
        self.bad = 0

    def run(self, map_number, scale):
        mark = Mark(map_number=map_number)  # Создаем объект маркировки
        mark.set_masks()  # Получаем координаты меток
        res = mark.calc_distance(scale)  # Получаем расстояние между метками игрока и желтой меткой
        return map_number, res  # Возвращаем номер карты и расстояние

    def test(self, map_number, scale, real_distance):
        res = self.run(map_number, scale)
        distance_range = 10
        if abs(res[1] - real_distance) >= distance_range:
            print(f'Ошибка в карте {map_number}')
            print(f'Результат: {res[1]}, должно быть: от {real_distance-distance_range} до {real_distance+distance_range}')
            print(f'Масштаб: {scale}')
            print('-' * 20)
            self.bad += 1
        else:
            # print(f'Карта {map_number} проверена')
            # print(f'Результат: {res[1]}, должно быть: от {real_distance-distance_range} до {real_distance+distance_range}')
            # print('-' * 20)
            self.good += 1

    # try:
    #     # scale = input(
    #     #     "Масштабування мапи?: ")  # Отказался от OCR, для standalone-приложения гемморно и много ресов лишних жрёт
    #     scale = 180
    #     marker = Mark()
    #     # marker.set_map_scale(scale)
    #
    #     # while True:
    #     marker.set_masks()  # Создаём маски
    #
    #     # marker.get_yellow_mark_coordinates()  # Получаем средние координаты точек
    #     # marker.get_player_mark_coordinates()
    #
    #     # print('player:', player)
    #     # print('yellow:', yellow)
    #
    #     res = marker.calc_distance(scale)  # Считаем дистанцию
    #     print('result:', res)
    #
    #         # rand = random.random()  # На всякий случай
    #         # sleep(rand)
    # except KeyboardInterrupt:
    #     exit(0)


main = Main()

main.test(map_number=1, scale=200, real_distance=1109)
main.test(map_number=2, scale=200, real_distance=551)
main.test(map_number=3, scale=250, real_distance=241)
main.test(map_number=4, scale=225, real_distance=80)
main.test(map_number=5, scale=225, real_distance=331)
main.test(map_number=6, scale=225, real_distance=224)
main.test(map_number=7, scale=225, real_distance=438)
main.test(map_number=8, scale=225, real_distance=155)
main.test(map_number=9, scale=225, real_distance=565)
main.test(map_number=10, scale=250, real_distance=82)
main.test(map_number=11, scale=140, real_distance=404)
main.test(map_number=12, scale=140, real_distance=148)
main.test(map_number=13, scale=225, real_distance=232)
main.test(map_number=14, scale=180, real_distance=140)
main.test(map_number=15, scale=225, real_distance=390)
main.test(map_number=16, scale=225, real_distance=300)
main.test(map_number=17, scale=200, real_distance=352)
main.test(map_number=18, scale=225, real_distance=84)
main.test(map_number=19, scale=250, real_distance=614)
main.test(map_number=20, scale=250, real_distance=912)
main.test(map_number=21, scale=250, real_distance=20)
main.test(map_number=22, scale=250, real_distance=778)
main.test(map_number=23, scale=250, real_distance=529)
main.test(map_number=24, scale=200, real_distance=1073)
main.test(map_number=25, scale=250, real_distance=800)
main.test(map_number=26, scale=225, real_distance=39)
main.test(map_number=27, scale=225, real_distance=560)
main.test(map_number=28, scale=180, real_distance=199)
main.test(map_number=29, scale=200, real_distance=831)
main.test(map_number=30, scale=170, real_distance=306)
main.test(map_number=31, scale=170, real_distance=365)
main.test(map_number=32, scale=225, real_distance=199)
main.test(map_number=33, scale=225, real_distance=239)
main.test(map_number=34, scale=200, real_distance=155)
# main.test(map_number=35, scale=275, real_distance=672)
main.test(map_number=36, scale=200, real_distance=198)
main.test(map_number=37, scale=200, real_distance=166)
main.test(map_number=38, scale=200, real_distance=132)
main.test(map_number=39, scale=225, real_distance=267)
main.test(map_number=40, scale=225, real_distance=176)
main.test(map_number=41, scale=200, real_distance=656)
main.test(map_number=42, scale=300, real_distance=146)
main.test(map_number=43, scale=300, real_distance=197)
main.test(map_number=44, scale=300, real_distance=501)
main.test(map_number=45, scale=275, real_distance=411)
main.test(map_number=46, scale=200, real_distance=552)
main.test(map_number=47, scale=200, real_distance=182)
main.test(map_number=48, scale=190, real_distance=213)
main.test(map_number=49, scale=190, real_distance=145)
print(f'Всего проверено: {main.good + main.bad}')
print(f'Проверено правильно: {main.good}')
print(f'Проверено неправильно: {main.bad}')
print (datetime.now()-start)

from time import sleep

from mark import Mark


def run(map_number, scale):
    mark = Mark(map_number=map_number)  # Создаем объект маркировки
    mark.set_masks()  # Получаем координаты меток
    res = mark.calc_distance(scale)  # Получаем расстояние между метками игрока и желтой меткой
    return map_number, res  # Возвращаем номер карты и расстояние


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

print('distance:', run(1, 140), 'real: 148')  # Проверка на правильное значение дистанции
print('distance:', run(2, 225), 'real: 232')
print('distance:', run(3, 180), 'real: 140')
print('distance:', run(4, 225), 'real: 390')
print('distance:', run(5, 180), 'real: 300')
print('distance:', run(6, 225), 'real: 352')
print('distance:', run(7, 225), 'real: 84')
print('distance:', run(8, 250), 'real: 614')
print('distance:', run(9, 250), 'real: 912')
print('distance:', run(10, 250), 'real: 20')
print('distance:', run(11, 250), 'real: 778')
print('distance:', run(12, 250), 'real: 529')
print('distance:', run(13, 200), 'real: 1073')
print('distance:', run(14, 200), 'real: 1109')
print('distance:', run(15, 200), 'real: 551')
print('distance:', run(16, 250), 'real: 241')
print('distance:', run(17, 225), 'real: 80')
print('distance:', run(18, 225), 'real: 331')
print('distance:', run(19, 225), 'real: 224')
print('distance:', run(20, 225), 'real: 438')
print('distance:', run(21, 225), 'real: 155')
print('distance:', run(22, 225), 'real: 565')
print('distance:', run(23, 250), 'real: 82')
print('distance:', run(24, 140), 'real: 404')

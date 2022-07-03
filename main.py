from time import sleep

from mark import Mark


def main():
    """
    Основная функция
    :return: Результат
    """
    sleep(1.2)
    marker = Mark()
    marker.set_masks()
    res = marker.calc_distance()
    if res is not None:
        print("result:", res)
        return res

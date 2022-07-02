from time import sleep
import keyboard

from mark import Mark


def main():
    """
    Основная функция
    :return:
    """
    marker = Mark()
    marker.set_masks()
    res = marker.calc_distance()
    if res is not None:
        print('result:', res)


print('Start')
while True:
    if keyboard.is_pressed('f12'):
        sleep(1.5)
        try:
            main()
        except Exception as e:
            print(e)
            sleep(0.5)
            main()

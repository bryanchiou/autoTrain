import keyboard
import random
import time
import ctypes
import sys


class KeyController:
    @staticmethod
    def doCombo(combo, times=1):
        for i in range(times):
            for each in combo:
                keyboard.press(each)
                time.sleep(round(random.uniform(0.03, 0.05), 2))
            for each in combo:
                keyboard.release(each)
                time.sleep(round(random.uniform(0.03, 0.05), 2))

    @staticmethod
    def loot(combo, times=3):
        for i in range(times):
            time.sleep(0.7)
            for each in combo:
                keyboard.press(each)
                time.sleep(round(random.uniform(0.07, 0.1), 2))
                keyboard.release(each)
                if each == 'space':
                    time.sleep(round(random.uniform(0.08, 0.1), 2))
        # down alt
        time.sleep(1)
        keyboard.press('down')
        time.sleep(round(random.uniform(0.03, 0.05), 2))
        keyboard.press('alt')
        time.sleep(round(random.uniform(0.03, 0.05), 2))
        keyboard.release('down')
        time.sleep(round(random.uniform(0.03, 0.05), 2))
        keyboard.release('alt')

import os
import json
import keyboard
import time
import random


class Buff:
    def __init__(self, character):
        self.buffCycle = 0
        self.buffs = dict()
        self.character = character

    def setup(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, './utils/buffs.json')
        f = open(filename)
        data = json.load(f)
        buffInfo = data[self.character]
        self.buffCycle = buffInfo["time"]
        self.buffs = buffInfo["buffs"]

    def getBuffCycle(self):
        return self.buffCycle

    def buffUp(self):
        for each in self.buffs:
            waitTime = self.buffs[each]
            keyboard.press(each)
            time.sleep(round(random.uniform(0.03, 0.05), 2))
            keyboard.release(each)
            time.sleep(waitTime)

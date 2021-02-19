from mapBuilder import MapBuilder
from locator import Locator
from trainingCycle import TrainingCycle
from lootCycle import LootCycle
from keyController import KeyController
from buff import Buff
import ctypes
import time
import sys
import random
import keyboard


class AutoAttacker:
    mapBuilder: MapBuilder
    locator: Locator
    trainingCycle: TrainingCycle
    lootCycle: LootCycle
    buff: Buff
    startTime: float
    curTime: float

    def __init__(self, mapName, character):
        self.mapBuilder = MapBuilder(mapName)
        self.locator = Locator(mapName)
        self.trainingCycle = TrainingCycle(character, mapName)
        self.lootCycle = LootCycle(character, mapName)
        self.buff = Buff(character)
        self.startTime = time.time()

    # !!! IMPORTANT TO USE 1080p RESOLUTION !!!
    def start(self):
        self.curTime = int(round(time.time() - self.startTime))
        buffTime = self.curTime
        pickupTime = self.curTime
        time.sleep(2)
        plat = None
        while True:
            try:
                res = self.locator.findChar()
            except:
                print('locator could not find character')
                continue
            plat = self.mapBuilder.onWhichPlatform(
                res[1], res[2], res[3], res[4])
            if not plat:
                continue
            buff = pickup = False
            if self.curTime - buffTime > 185:
                buff = True
                buffTime += 185
            if self.curTime - pickupTime > 90:
                pickup = True
                pickupTime += 90
            if buff:
                self.buff.buffUp()
            if pickup:
                self.pickup()
            action = self.trainingCycle.cycle[tuple(plat)]
            KeyController.doCombo(action, 1)
            time.sleep(round(random.uniform(0.8, 0.6), 2))
            self.curTime = int(round(time.time() - self.startTime))

    def pickup(self):
        count = 0
        while count < 2:
            try:
                res = self.locator.findChar()
            except:
                print('locator could not find character in pickup')
                continue
            temp = self.mapBuilder.onWhichPlatform(
                res[1], res[2], res[3], res[4])
            if not temp:
                count -= 1
                continue
            combo = self.lootCycle.cycle[tuple(temp)]
            KeyController.loot(combo, 3)
            count += 1


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if is_admin():
    a = AutoAttacker("Nath", "Fighter")
    time.sleep(1)
    a.locator.setup()
    time.sleep(1)
    a.buff.setup()
    time.sleep(1)
    a.start()
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1)

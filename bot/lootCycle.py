import json
import os


class LootCycle:
    def __init__(self, character, trainingMap) -> None:
        self.cycle = dict()
        self.character = character
        self.setUp(trainingMap)

    def setUp(self, trainingMap="Arcana"):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, './utils/lootCycle.json')
        f = open(filename)
        data = json.load(f)
        self.mapInfo = data[self.character][trainingMap]
        for group in self.mapInfo["platforms"]:
            dimensions = group["dimension"]
            keypress = group["cycle"]
            for each in dimensions:
                self.cycle[tuple(each)] = keypress

    def getCycle(self):
        return self.cycle

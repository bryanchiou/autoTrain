
from pathlib import Path
from PIL import Image, ImageDraw, ImageGrab
import json
import os
import ctypes
import time
import sys


class MapBuilder:
    def __init__(self, mapName):
        self.minimapSize: tuple()
        self.miniMap: list(list(int))
        self.platforms: list(list(int))
        self.importMinimap(trainingMap=mapName)
        self.buildMap()

    def importMinimap(self, trainingMap):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, './utils/minimaps.json')
        f = open(filename)
        data = json.load(f)
        self.minimapSize = (data[trainingMap]["width"],
                            data[trainingMap]["height"])
        self.platforms = data[trainingMap]["platforms"]

    def buildMap(self):
        w, h = self.minimapSize
        self.miniMap = [[0 for i in range(w)] for j in range(h)]
        for x, y, x1, y1 in self.platforms:
            for j in range(y, y1+1):
                for i in range(x, x1+1):
                    self.miniMap[j][i] = 1

    def onWhichPlatform(self, x, y, x1, y1):
        midX = x + ((x1 - x) // 2)
        platform = None
        for i in range(y1 + 1, len(self.miniMap)):
            if self.miniMap[i][midX]:
                # found plat
                for each in self.platforms:
                    if each[1] <= i and i <= each[3] and each[0] <= midX and midX <= each[2]:
                        platform = each
                        break
                break
        # if not platform:
        #     raise Exception('Could not find platform character is on')
        return platform

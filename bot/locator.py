import sys
from PIL import Image, ImageDraw, ImageGrab
import math
from pathlib import Path
import heapq
import os
import json
import time
import win32gui

# Screen shot will only capture correctly on 1920x1080p resolution


class Locator:
    THRESHOLD: int = 1500
    WINDOW_NAME: str = "MapleStory"

    def __init__(self, mapName):
        self.image: Image
        self.mapName = mapName
        self.minimapSize: tuple
        self.hwnd = None

    def setup(self):
        self.minimapSize = self.getMiniMapSize()
        self.hwnd = self.setMapleWindowHandle()

    def getMiniMapSize(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, './utils/minimaps.json')
        f = open(filename)
        data = json.load(f)
        return (data[self.mapName]["width"], data[self.mapName]["height"])

    def setMapleWindowHandle(self):
        winlist = []

        def enum_cb(hwnd, results):
            winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
        win32gui.EnumWindows(enum_cb, None)
        mapleWindow = None
        for hwnd, title in winlist:
            if title == self.WINDOW_NAME:
                mapleWindow = (hwnd, title)
                break
        if mapleWindow:
            hwnd = mapleWindow[0]
            win32gui.SetForegroundWindow(hwnd)
            return hwnd
        else:
            err = self.WINDOW_NAME + " window not found"
            raise Exception(err)

    def screenshot(self, full=True):
        rect = win32gui.GetWindowRect(self.hwnd)
        if full:
            im = ImageGrab.grab(rect)
        else:
            im = ImageGrab.grab(bbox=(rect[0], rect[1]+30, rect[0] +
                                      self.minimapSize[0], rect[1]+30+self.minimapSize[1]))
        return im

    def findChar(self):
        self.image = self.screenshot(False)
        res = self.search()
        if not res:
            raise Exception("No character found")
        return res[0]

    def search(self):
        imageSizeX = self.image.size[0]
        imageSizeY = self.image.size[1]
        i = 0
        res = []
        visited = set()
        while i < imageSizeX:
            j = (imageSizeY // 4)
            while j < imageSizeY and (i, j) not in visited:
                pixel = self.image.getpixel((i, j))
                d = self.euclid(pixel, (255, 221, 68, 255))
                if d < self.THRESHOLD:
                    # could hardcode if area around 37ish pixels, then found the char
                    # since some maps could have a lot of yellow
                    heapq.heappush(res, self.getCharArea((i, j), visited))
                else:
                    visited.add((i, j))
                j += 1
            i += 1
        return res

    def getCharArea(self, point, visited):
        bfs = [point]
        xRange = [math.inf, 0]
        yRange = [math.inf, 0]
        area = 0
        while bfs:
            x, y = bfs.pop()
            if (x, y) in visited:
                continue
            area += 1
            visited.add((x, y))
            d = self.euclid(self.image.getpixel((x, y)), (255, 221, 68))
            if d < self.THRESHOLD:
                xRange[0] = min(xRange[0], x)
                xRange[1] = max(xRange[1], x)
                yRange[0] = min(yRange[0], y)
                yRange[1] = max(yRange[1], y)
                if x > 0:
                    bfs.append((x-1, y))
                if x < self.image.size[0]:
                    bfs.append((x+1, y))
                if y > 0:
                    bfs.append((x, y-1))
                if y < self.image.size[1]:
                    bfs.append((x, y+1))

        res = [-area, xRange[0], yRange[0], xRange[1], yRange[1]]
        return res

    def euclid(self, a, b):
        return sum((a - b) ** 2 for a, b in zip(a, b))

    def drawRect(self, ranges):
        draw = ImageDraw.Draw(self.image)
        x, y, x1, y1 = ranges
        draw.rectangle((x, y, x + (x1 - x), y + (y1-y)), outline='red')
        dirname = os.path.dirname(__file__)
        p = Path(dirname + '/out.png')
        self.image.save(p)

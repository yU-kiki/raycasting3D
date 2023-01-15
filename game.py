import pyxel
import math

class Map:
    def __init__(self):
        self.mapX = 8
        self.mapY = 8
        self.mapS = 64
        self.worldMap = [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
        ]

    def draw2dMap(self):
        for y in range(self.mapY):
            for x in range(self.mapX):
                color1 = 0
                color2 = 0
                if self.worldMap[x][y] == 0:
                    color1 = 7
                    color2 = 0
                elif self.worldMap[x][y] == 1:
                    color1 = 0
                    color2 = 7
                xo = self.mapS * x
                yo = self.mapS * y
                pyxel.rect(xo, yo, self.mapS, 1, color1)
                pyxel.rect(xo, yo, 1, self.mapS, color1)
                pyxel.rect(xo + 1, yo + 1, self.mapS - 2, self.mapS - 2, color2)
                x += 1
            y += 1
        

class App:
    def __init__(self):
        pyxel.init(1024,512)
        self.map = Map()
        self.px = 300
        self.py = 300
        self.pa = 0
        self.pdx = math.cos(self.pa) * 5
        self.pdy = math.sin(self.pa) * 5

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_A):
            self.pa -= 0.1
            if self.pa < 0:
                self.pa += 2 * math.pi
            self.pdx = math.cos(self.pa) * 5
            self.pdy = math.sin(self.pa) * 5
        if pyxel.btn(pyxel.KEY_D):
            self.pa += 0.1
            if self.pa > 2 * math.pi:
                self.a -= 2 * math.pi
            self.pdx = math.cos(self.pa) * 5
            self.pdy = math.sin(self.pa) * 5
        if pyxel.btn(pyxel.KEY_W):
            self.px += self.pdx
            self.py += self.pdy
        if pyxel.btn(pyxel.KEY_S):
            self.px -= self.pdx
            self.py -= self.pdy

    def draw(self):
        pyxel.cls(13)
        self.map.draw2dMap()
        pyxel.circ(self.px, self.py, 5, 10)
        pyxel.line(self.px, self.py, self.px + self.pdx * 5, self.py + self.pdy * 5, 10)

App()
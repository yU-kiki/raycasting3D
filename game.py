import pyxel
import math
PI = 3.1415926535
P2 = PI / 2
P3 = 3 * PI / 2
class App:
    def __init__(self):
        pyxel.init(1024,512)
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
        self.px = 300
        self.py = 300
        self.pa = 0.0001
        self.pdx = math.cos(self.pa) * 5
        self.pdy = math.sin(self.pa) * 5

        self.ra = self.pa
        self.rx = 0
        self.ry = 0

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_A):
            self.pa -= 0.1
            if self.pa < 0:
                self.pa += 2 * PI
            self.pdx = math.cos(self.pa) * 5
            self.pdy = math.sin(self.pa) * 5
        if pyxel.btn(pyxel.KEY_D):
            self.pa += 0.1
            if self.pa > 2 * PI:
                self.pa -= 2 * PI
            self.pdx = math.cos(self.pa) * 5
            self.pdy = math.sin(self.pa) * 5
        if pyxel.btn(pyxel.KEY_W):
            self.px += self.pdx
            self.py += self.pdy
        if pyxel.btn(pyxel.KEY_S):
            self.px -= self.pdx
            self.py -= self.pdy

        self.update_rays()

    def update_rays(self):
        r = 0
        self.ra = self.pa
        while r < 1:
            # check Horizontal lines
            dof = 0
            aTan = -1 / math.tan(self.ra)
            if self.ra > PI:
                self.ry = ((int(self.py) >> 6) << 6) - 0.0001
                self.rx = (self.py - self.ry) * aTan + self.px
                yo = -64
                xo = -yo  * aTan
            if self.ra < PI:
                self.ry = ((int(self.py) >> 6) << 6) + 64
                self.rx = (self.py - self.ry) * aTan + self.px
                yo = 64
                xo = -yo  * aTan
            if self.ra == 0 or self.ra == PI:
                self.rx = self.px
                self.ry = self.py
                dof = 8
            while dof < 8:
                mx = int(self.rx) >> 6
                my = int(self.ry) >> 6
                if 0 <= mx < self.mapX and 0 <= my < self.mapY and self.worldMap[mx][my] == 1:
                    dof = 8
                else:
                    self.rx += xo
                    self.ry += yo
                    dof += 1
            # pyxel.line(self.px, self.py, self.rx, self.ry, 9)

            # check Vertical lines
            dof = 0
            nTan = -math.tan(self.ra)
            if self.ra > P2 and self.ra < P3:
                self.rx = ((int(self.px) >> 6) << 6) - 0.0001
                self.ry = (self.px - self.rx) * nTan + self.py
                xo = -64
                yo = -xo  * nTan
            if self.ra < P2 or self.ra > P3:
                self.rx = ((int(self.px) >> 6) << 6) + 64
                self.ry = (self.px - self.rx) * nTan + self.py
                xo = 64
                yo = -xo  * nTan
            if self.ra == 0 or self.ra == PI:
                self.rx = self.px
                self.ry = self.py
                dof = 8
            while dof < 8:
                mx = int(self.rx) >> 6
                my = int(self.ry) >> 6
                if 0 <= mx < self.mapX and 0 <= my < self.mapY and self.worldMap[mx][my] == 1:
                    dof = 8
                else:
                    self.rx += xo
                    self.ry += yo
                    dof += 1
            # pyxel.line(self.px, self.py, self.rx, self.ry, 9)
            r += 1

    def draw(self):
        pyxel.cls(13)
        self.draw_2dMap()
        pyxel.circ(self.px, self.py, 5, 10)
        pyxel.line(self.px, self.py, self.px + self.pdx * 5, self.py + self.pdy * 5, 10)
        pyxel.line(self.px, self.py, self.rx, self.ry, 11)

    def draw_2dMap(self):
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
App()
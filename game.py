import pyxel
import math
PI = 3.1415926535
P2 = PI / 2
P3 = 3 * PI / 2
DR = 0.0174533 # one degree to radius
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

        self.rx = 0
        self.ry = 0

        self.rayList = []
        for _ in range(60):
            self.rayList.append(None)

        pyxel.run(self.update, self.draw)
    
    def dist(self, x1, y1, x2, y2, ang):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.pa -= 0.1
            if self.pa < 0:
                self.pa += 2 * PI
            self.pdx = math.cos(self.pa) * 5
            self.pdy = math.sin(self.pa) * 5
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.pa += 0.1
            if self.pa > 2 * PI:
                self.pa -= 2 * PI
            self.pdx = math.cos(self.pa) * 5
            self.pdy = math.sin(self.pa) * 5
        
        xo = -20 if self.pdx < 0 else 20
        yo = -20 if self.pdy < 0 else 20
        ipx = self.px / 64.0
        ipx_add_xo = (self.px + xo) / 64.0
        ipx_sub_xo = (self.px - xo) / 64.0
        ipy = self.py / 64.0
        ipy_add_yo = (self.py + yo) / 64.0
        ipy_sub_yo = (self.py - yo) / 64.0

        if pyxel.btn(pyxel.KEY_UP):
            if self.worldMap[int(ipx_add_xo)][int(ipy)] == 0:
                self.px += self.pdx
            if self.worldMap[int(ipx)][int(ipy_add_yo)] == 0:
                self.py += self.pdy
        if pyxel.btn(pyxel.KEY_DOWN):
            if self.worldMap[int(ipx_sub_xo)][int(ipy)] == 0:
                self.px -= self.pdx
            if self.worldMap[int(ipx)][int(ipy_sub_yo)] == 0:
                self.py -= self.pdy

        self.update_rays()

    def update_rays(self):
        ra = self.pa - DR * 30
        if ra < 0:
            ra += 2 * PI
        if ra > 2 * PI:
            ra -= 2 * PI 
        for i in range(60):
            # check Horizontal lines
            dof = 0
            disH = 1000000
            hx = self.px
            hy = self.py
            aTan = -1 / math.tan(ra)
            if ra > PI:
                self.ry = ((int(self.py) >> 6) << 6) - 0.0001
                self.rx = (self.py - self.ry) * aTan + self.px
                yo = -64
                xo = -yo  * aTan
            if ra < PI:
                self.ry = ((int(self.py) >> 6) << 6) + 64
                self.rx = (self.py - self.ry) * aTan + self.px
                yo = 64
                xo = -yo  * aTan
            if ra == 0 or ra == PI:
                self.rx = self.px
                self.ry = self.py
                dof = 8
            while dof < 8:
                mx = int(self.rx) >> 6
                my = int(self.ry) >> 6
                if 0 <= mx < self.mapX and 0 <= my < self.mapY and self.worldMap[mx][my] == 1:
                    hx = self.rx
                    hy = self.ry
                    disH = self.dist(self.px, self.py, hx, hy, ra)
                    dof = 8
                else:
                    self.rx += xo
                    self.ry += yo
                    dof += 1

            # check Vertical lines
            dof = 0
            disV = 1000000
            vx = self.px
            vy = self.py
            nTan = -math.tan(ra)
            if ra > P2 and ra < P3:
                self.rx = ((int(self.px) >> 6) << 6) - 0.0001
                self.ry = (self.px - self.rx) * nTan + self.py
                xo = -64
                yo = -xo  * nTan
            if ra < P2 or ra > P3:
                self.rx = ((int(self.px) >> 6) << 6) + 64
                self.ry = (self.px - self.rx) * nTan + self.py
                xo = 64
                yo = -xo  * nTan
            if ra == 0 or ra == PI:
                self.rx = self.px
                self.ry = self.py
                dof = 8
            while dof < 8:
                mx = int(self.rx) >> 6
                my = int(self.ry) >> 6
                if 0 <= mx < self.mapX and 0 <= my < self.mapY and self.worldMap[mx][my] == 1:
                    vx = self.rx
                    vy = self.ry
                    disV = self.dist(self.px, self.py, vx, vy, ra)
                    dof = 8
                else:
                    self.rx += xo
                    self.ry += yo
                    dof += 1

            disT = 0
            hit = 0
            if disV < disH:
                self.rx = vx
                self.ry = vy
                disT = disV
                hit = 0
            if disH < disV:
                self.rx = hx
                self.ry = hy
                disT = disH
                hit = 1

            ca = self.pa - ra
            if ca < 0:
                ca += 2 * PI
            if ca > 2 * PI:
                ca -= 2 * PI
            disT = disT * math.cos(ca)
            lineH = (self.mapS * 320) / disT
            if lineH > 320:
                lineH = 320
            lineO = 160 - lineH / 2
            
            self.rayList[i] = [self.rx, self.ry, lineH, lineO, hit]

            ra += DR
            if ra < 0:
                ra += 2 * PI
            if ra > 2 * PI:
                ra -= 2 * PI

    def draw(self):
        pyxel.cls(13)
        self.draw_2dMap()
        pyxel.circ(self.px, self.py, 5, 10)
        pyxel.line(self.px, self.py, self.px + self.pdx * 5, self.py + self.pdy * 5, 10)
        for i, v in enumerate(self.rayList):
            pyxel.line(self.px, self.py, v[0], v[1], 11)
            if v[4] == 0:
                col = 3
            elif v[4] == 1:
                col = 11
            pyxel.rect(i * 8 + 530, v[3], 8, v[2], col)

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
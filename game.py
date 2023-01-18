import pyxel
import math
PI = 3.1415926535
P2 = PI / 2
P3 = 3 * PI / 2
DR = 0.0174533 # one degree to radius
class App:
    def __init__(self):
        self.worldMap = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]
        self.mapX = len(self.worldMap[0])
        self.mapY = len(self.worldMap)
        self.maxLen = self.mapX if self.mapX >= self.mapY else self.mapY
        self.map2DSec = 32
        self.scale = 64 / self.map2DSec

        pyxel.init(self.mapX * self.map2DSec + 480 + 24, 480)
        self.px = 300
        self.py = 300
        self.pa = 0.0001
        self.pdx = math.cos(self.pa) * 5
        self.pdy = math.sin(self.pa) * 5

        self.rx = 0
        self.ry = 0
        self.ra = 0

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
            if self.worldMap[int(ipy)][int(ipx_add_xo)] == 0:
                self.px += self.pdx
            if self.worldMap[int(ipy_add_yo)][int(ipx)] == 0:
                self.py += self.pdy
        if pyxel.btn(pyxel.KEY_DOWN):
            if self.worldMap[int(ipy)][int(ipx_sub_xo)] == 0:
                self.px -= self.pdx
            if self.worldMap[int(ipy_sub_yo)][int(ipx)] == 0:
                self.py -= self.pdy

        self.update_rays()

    def update_rays(self):
        self.ra = self.pa - DR * 30
        if self.ra < 0:
            self.ra += 2 * PI
        if self.ra > 2 * PI:
            self.ra -= 2 * PI 
        for i in range(60):
            # check Horizontal lines
            dof = 0
            disH = 1000000
            hx = self.px
            hy = self.py
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
                dof = self.maxLen
            while dof < self.maxLen:
                mx = int(self.rx) >> 6
                my = int(self.ry) >> 6
                if 0 <= mx < self.mapX and 0 <= my < self.mapY and self.worldMap[my][mx] == 1:
                    hx = self.rx
                    hy = self.ry
                    disH = self.dist(self.px, self.py, hx, hy, self.ra)
                    dof = self.maxLen
                else:
                    self.rx += xo
                    self.ry += yo
                    dof += 1

            # check Vertical lines
            dof = 0
            disV = 1000000
            vx = self.px
            vy = self.py
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
                dof = self.maxLen
            while dof < self.maxLen:
                mx = int(self.rx) >> 6
                my = int(self.ry) >> 6
                if 0 <= mx < self.mapX and 0 <= my < self.mapY and self.worldMap[my][mx] == 1:
                    vx = self.rx
                    vy = self.ry
                    disV = self.dist(self.px, self.py, vx, vy, self.ra)
                    dof = self.maxLen
                else:
                    self.rx += xo
                    self.ry += yo
                    dof += 1

            disT = 0
            hit = 0
            if disV <= disH:
                self.rx = vx
                self.ry = vy
                disT = disV
                hit = 0
            if disH < disV:
                self.rx = hx
                self.ry = hy
                disT = disH
                hit = 1

            ca = self.pa - self.ra
            if ca < 0:
                ca += 2 * PI
            if ca > 2 * PI:
                ca -= 2 * PI
            disT = disT * math.cos(ca)
            lineH = (64 * 320) / disT
            if lineH > 320:
                lineH = 320
            lineO = 160 - lineH / 2
            
            self.rayList[i] = [self.rx, self.ry, lineH, lineO, hit]

            self.ra += DR
            if self.ra < 0:
                self.ra += 2 * PI
            if self.ra > 2 * PI:
                self.ra -= 2 * PI

    def draw(self):
        pyxel.cls(13)
        self.draw_2dMap()
        # 現在地の描画
        pyxel.circ(self.px / self.scale, self.py / self.scale, 5 / math.sqrt(self.scale), 10)
        # 方向
        pyxel.line(self.px / self.scale, self.py / self.scale, (self.px + self.pdx * 5) / self.scale, (self.py + self.pdy * 5) / self.scale, 10)
        for i, v in enumerate(self.rayList):
            # ray部分の描画
            pyxel.line(self.px / self.scale, self.py / self.scale, v[0] / self.scale, v[1] / self.scale, 11)
            # 3D部分の描画
            if v[4] == 0:
                col = 3
            elif v[4] == 1:
                col = 11
            pyxel.rect(i * 8 + self.mapX * self.map2DSec + 12, 0, 8, v[3], 12)
            pyxel.rect(i * 8 + self.mapX * self.map2DSec + 12, v[3], 8, v[2], col)
            pyxel.rect(i * 8 + self.mapX * self.map2DSec + 12, v[2] + v[3], 8, 480 - v[2] - v[3], 7)

    def draw_2dMap(self):
        for y in range(self.mapY):
            for x in range(self.mapX):
                col = 0
                if self.worldMap[y][x] == 0:
                    col = 7
                elif self.worldMap[y][x] == 1:
                    col = 0
                xo = self.map2DSec * x
                yo = self.map2DSec * y
                pyxel.rect(xo, yo, self.map2DSec, self.map2DSec, col)
                if x > 0:
                    pyxel.line(xo, 0, xo, self.mapY * self.map2DSec, 13)
                x += 1
            if y > 0:
                pyxel.line(0, yo, self.mapX * self.map2DSec, yo, 13)
            y += 1
            
App()
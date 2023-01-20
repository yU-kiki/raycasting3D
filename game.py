import pyxel
import math
PI = 3.1415926535
P2 = PI / 2
P3 = 3 * PI / 2
DR = 0.0174533 # one degree to radius
class App:
    def __init__(self):
        # 0: 開発　1: 発表
        self.mode = 1
        # 表示関連
        self.shiftX = 6 if self.mode == 1 else 0
        self.shiftY = 8 if self.mode == 1 else 0
        self.map2DSec = 24 if self.mode == 1 else 64
        self.scale = 64 / self.map2DSec

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
        self.maxLen = max(self.mapX, self.mapY)

        pyxel.init(self.mapX * self.map2DSec + 480 + 24, max(480, self.mapY * self.map2DSec))
        self.px = 300
        self.py = 300
        self.pa = 0.0001
        self.pdx = math.cos(self.pa) * 5
        self.pdy = math.sin(self.pa) * 5
        self.rx = 0
        self.ry = 0
        self.ra = 0

        # 使用色を設定する
        colorList = [0xFEFEFE, 0x0c0c0c, 0xF5BAA4, 0xECEB7D, 0x273256, 0xE55D5B, 0x64C8E3, 0xF3AC69, 0xE5ACC6, 0x804137, 0x804137, 0x3e2731, 0x85483f, 0x794641, 0x462f39, 0x7cfc00]
        for i in range(len(colorList)):
            pyxel.colors[i] = colorList[i]

        self.texture1 = [
            9, 9, 9, 11, 9, 9, 9, 9, 9, 9, 9, 11, 9, 9, 9, 9,
            10, 10, 9, 11, 10, 10, 10, 10, 10, 10, 9, 11, 10, 10, 10, 10,
            10, 10, 9, 11, 10, 10, 10, 10, 10, 10, 9, 11, 10, 10, 10, 10,
            11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
            11, 9, 9, 9, 9, 9, 9, 9, 11, 9, 9, 9, 9, 9, 9, 9,
            11, 10, 10, 10, 10, 10, 10, 9, 11, 10, 10, 10, 10, 10, 10, 9,
            11, 10, 10, 10, 10, 10, 10, 9, 11, 10, 10, 10, 10, 10, 10, 9,
            11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
            9, 9, 9, 11, 9, 9, 9, 9, 9, 9, 9, 11, 9, 9, 9, 9,
            10, 10, 9, 11, 10, 10, 10, 10, 10, 10, 9, 11, 10, 10, 10, 10,
            10, 10, 9, 11, 10, 10, 10, 10, 10, 10, 9, 11, 10, 10, 10, 10,
            11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
            11, 9, 9, 9, 9, 9, 9, 9, 11, 9, 9, 9, 9, 9, 9, 9,
            11, 10, 10, 10, 10, 10, 10, 9, 11, 10, 10, 10, 10, 10, 10, 9,
            11, 10, 10, 10, 10, 10, 10, 9, 11, 10, 10, 10, 10, 10, 10, 9,
            11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11
        ]

        self.rayList = []
        for _ in range(480):
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
        for i in range(len(self.rayList)):
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

            # 壁の色変更に必要
            if hit == 0:
                rowNum = round(self.ry % 64 / 4) % 16
            if hit == 1:
                rowNum = round(self.rx % 64 / 4) % 16
            # print(f'i: {i} mx: {mx} my: {my} rx: {self.rx} ry: {self.ry} hit: {hit} lineH: {lineH}')
            self.rayList[i] = [self.rx, self.ry, lineH, lineO, hit, rowNum]

            self.ra += DR / 8
            if self.ra < 0:
                self.ra += 2 * PI
            if self.ra > 2 * PI:
                self.ra -= 2 * PI

    def draw(self):
        pyxel.cls(10)
        self.draw_2dMap()
        # 現在地の描画
        pyxel.circ(self.px / self.scale + self.shiftX, self.py / self.scale + self.shiftY, 5 / math.sqrt(self.scale), 3)
        # 方向
        pyxel.line(self.px / self.scale + self.shiftX, self.py / self.scale + self.shiftY, (self.px + self.pdx * 5) / self.scale + self.shiftX, (self.py + self.pdy * 5) / self.scale + self.shiftY, 15)
        for i, v in enumerate(self.rayList):
            # ray部分の描画
            if i % 8 == 0:
                pyxel.line(self.px / self.scale  + self.shiftX, self.py / self.scale + self.shiftY, v[0] / self.scale + self.shiftX, v[1] / self.scale + self.shiftY, 15)
            # 3D部分の描画
            pyxel.rect(i + self.mapX * self.map2DSec + 12 + self.shiftX, 0, 8, v[3], 1)
            for columnNum in range(16):
                hd = v[2] / 16
                col = self.texture1[columnNum * 16 + v[5]]
                # より立体感を出す
                if v[4] == 0:
                    col += 3
                pyxel.rect(i + self.mapX * self.map2DSec + 12 + self.shiftX, v[3] + hd * columnNum, 8, hd, col)
            pyxel.rect(i + self.mapX * self.map2DSec + 12 + self.shiftX, v[2] + v[3], 8, 480 - v[2] - v[3], 1)

    def draw_2dMap(self):
        for y in range(self.mapY):
            for x in range(self.mapX):
                col = 0
                if self.worldMap[y][x] == 0:
                    col = 0
                elif self.worldMap[y][x] == 1:
                    col = 1
                xo = self.map2DSec * x
                yo = self.map2DSec * y
                pyxel.rect(xo + self.shiftX, yo + self.shiftY, self.map2DSec, self.map2DSec, col)
                if x > 0:
                    pyxel.line(xo + self.shiftX, 0 + self.shiftY, xo + self.shiftX, self.mapY * self.map2DSec + self.shiftY, 2)
                x += 1
            if y > 0:
                pyxel.line(0 + self.shiftX, yo + self.shiftY, self.mapX * self.map2DSec + self.shiftX, yo + self.shiftY, 2)
            y += 1
            
App()
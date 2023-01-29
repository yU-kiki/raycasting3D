import pyxel
import math

PI = 3.1415926535
P2 = PI / 2
P3 = 3 * PI / 2
DR = 0.0174533 # one degree to radius
class App:
    def __init__(self):

        # 0: 開発　1: ゲーム
        self.mode = 1

        # 表示関連(0:開発用)
        self.shiftX = 6 if self.mode == 0 else None
        self.shiftY = 8 if self.mode == 0 else None
        self.map2DSec = 24 if self.mode == 0 else None
        self.scale = 64 / self.map2DSec if self.mode == 0 else None

        # ２Dのマップ
        self.worldMap = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1],
            [1, 3, 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 3, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 1],
            [1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1],
            [1, 1, 1, 2, 1, 1, 0, 1, 0, 1, 1, 2, 1, 1, 1],
            [1, 1, 1, 2, 1, 0, 0, 0, 0, 0, 1, 2, 1, 1, 1],
            [1, 1, 1, 2, 1, 0, 1, 5, 1, 0, 1, 2, 1, 1, 1],
            [0, 0, 0, 2, 0, 0, 1, 0, 1, 0, 0, 2, 0, 0, 0],
            [1, 1, 1, 2, 1, 0, 1, 1, 1, 0, 1, 2, 1, 1, 1],
            [1, 1, 1, 2, 1, 0, 0, 0, 0, 0, 1, 2, 1, 1, 1],
            [1, 1, 1, 2, 1, 1, 0, 1, 0, 1, 1, 2, 1, 1, 1],
            [1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1],
            [1, 2, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 3, 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 3, 1],
            [1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        self.mapX = len(self.worldMap[0])
        self.mapY = len(self.worldMap)
        self.maxLen = max(self.mapX, self.mapY)

        # worldマップの情報からspliteのリストを作成
        self.spliteList = []
        for x in range(self.mapX):
            for y in range(self.mapY):
                if self.worldMap[y][x] == 2:
                    dict = {}
                    dict["state"] = 1
                    dict["type"] = 2
                    dict["x"] = (x + 0.5) * 64
                    dict["y"] = (y + 0.5) * 64
                    dict["z"] = 10
                    dict["ix"] = x
                    dict["iy"] = y
                    dict["size"] = 10
                    self.spliteList.append(dict)
                if self.worldMap[y][x] == 3:
                    dict = {}
                    dict["state"] = 1
                    dict["type"] = 3
                    dict["x"] = (x + 0.5) * 64
                    dict["y"] = (y + 0.5) * 64
                    dict["z"] = 10
                    dict["ix"] = x
                    dict["iy"] = y
                    dict["size"] = 30
                    self.spliteList.append(dict)

        # 壁のテクスチャー
        self.texture_wall = [
            4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 4, 1, 4, 1, 4, 1, 4, 1, 4, 1, 4, 1, 4, 1, 4,
            4, 1, 1, 1, 4, 1, 1, 1, 4, 1, 1, 1, 4, 1, 1, 1,
            1, 4, 1, 4, 1, 4, 1, 4, 1, 4, 1, 4, 1, 4, 1, 4,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
        ]
        # # 敵のテクスチャー
        # self.texture_army = [
        #     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        #     1, 1, 1, 1, 1, 1, 5, 5, 5, 5, 1, 1, 1, 1, 1, 1,
        #     1, 1, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 1, 1, 1, 1,
        #     1, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 1, 1,
        #     1, 1, 5, 0, 0, 5, 5, 5, 5, 0, 0, 5, 5, 5, 1, 1,
        #     1, 1, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 5, 5, 1, 1,
        #     1, 1, 4, 4, 0, 0, 5, 5, 4, 4, 0, 0, 5, 5, 1, 1,
        #     1, 5, 4, 4, 0, 0, 5, 5, 4, 4, 0, 0, 5, 5, 5, 1,
        #     1, 5, 5, 0, 0, 5, 5, 5, 5, 0, 0, 5, 5, 5, 5, 1,
        #     1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1,
        #     1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1,
        #     1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1,
        #     1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1,
        #     1, 5, 5, 1, 5, 5, 5, 1, 1, 5, 5, 5, 1, 5, 5, 1,
        #     1, 5, 1, 1, 1, 5, 5, 1, 1, 5, 5, 1, 1, 1, 5, 1,
        #     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        # ]

        # モードによって画面を分ける
        if self.mode == 0:
            pyxel.init(self.mapX * self.map2DSec + 480 + 24, max(480, self.mapY * self.map2DSec), title="PAC-MAN-3D", display_scale=2, quit_key=pyxel.KEY_Q)
        if self.mode == 1:
            pyxel.init(240, 160, title="PAC-MAN-3D", display_scale=3, quit_key=pyxel.KEY_Q)

        # 使用色を設定する
        colorList = [0xFEFEFE, 0x0c0c0c, 0xF5BAA4, 0xECEB7D, 0x3C36A2, 0xE55D5B, 0x64C8E3, 0xF3AC69, 0xE5ACC6, 0x804137, 0x804137, 0x3e2731, 0x85483f, 0x794641, 0x462f39, 0x7cfc00]
        for i in range(len(colorList)):
            pyxel.colors[i] = colorList[i]

        # ２Dマップの情報
        self.px = 480
        self.py = 991
        self.pa = 3.141592
        self.pdx = math.cos(self.pa) * 5
        self.pdy = math.sin(self.pa) * 5
        self.rx = 0
        self.ry = 0
        self.ra = 0

        self.rayList = []
        for _ in range(240):
            self.rayList.append(None)

        # spliteの深さの比較のため、壁の線の深さを保持する
        self.depth = []
        for _ in range(240):
            self.depth.append(None)

        # ゲーム
        self.gameState = 0
        self.score = 0
        self.startTime = 0

        if self.mode == 0:
            pyxel.run(self.update, self.draw_dev)
        if self.mode == 1:
            pyxel.run(self.update, self.draw)
    
    def dist(self, x1, y1, x2, y2, ang):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def update(self):
        if pyxel.btn(pyxel.KEY_SPACE):
            self.gameState = 1
            self.startTime = pyxel.frame_count
        if pyxel.btn(pyxel.KEY_LEFT):
            self.pa -= 0.1
            if self.pa < 0:
                self.pa += 2 * PI
            self.pdx = math.cos(self.pa) * 3
            self.pdy = math.sin(self.pa) * 3
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.pa += 0.1
            if self.pa > 2 * PI:
                self.pa -= 2 * PI
            self.pdx = math.cos(self.pa) * 3
            self.pdy = math.sin(self.pa) * 3
        
        xo = -20 if self.pdx < 0 else 20
        yo = -20 if self.pdy < 0 else 20
        ipx = self.px / 64.0
        ipx_add_xo = (self.px + xo) / 64.0
        ipx_sub_xo = (self.px - xo) / 64.0
        ipy = self.py / 64.0
        ipy_add_yo = (self.py + yo) / 64.0
        ipy_sub_yo = (self.py - yo) / 64.0

        if pyxel.btn(pyxel.KEY_UP):
            if self.worldMap[int(ipy)][int(ipx_add_xo)] in [0, 2, 3]:
                if not int(ipx) == int((self.px + self.pdx) / 64.0):
                    for splite in self.spliteList:
                        if splite["ix"] == int((self.px + self.pdx) / 64.0) and splite["iy"] == int(ipy) and splite["state"] == 1:
                            splite["state"] = 0
                            if splite["type"] == 2:
                                self.score += 10
                            if splite["type"] == 3:
                                self.score += 50
                self.px += self.pdx
            if self.worldMap[int(ipy_add_yo)][int(ipx)] in [0, 2, 3]:
                if not int(ipy) == int((self.py + self.pdy) / 64.0):
                    for splite in self.spliteList:
                        if splite["ix"] == int(ipx) and splite["iy"] == int((self.py + self.pdy) / 64.0) and splite["state"] == 1:
                            splite["state"] = 0
                            if splite["type"] == 2:
                                self.score += 10
                            if splite["type"] == 3:
                                self.score += 50
                self.py += self.pdy
        if pyxel.btn(pyxel.KEY_DOWN):
            if self.worldMap[int(ipy)][int(ipx_sub_xo)] in [0, 2, 3]:
                if not int(ipx) == int((self.px - self.pdx) / 64.0):
                    for splite in self.spliteList:
                        if splite["ix"] == int((self.px - self.pdx) / 64.0) and splite["iy"] == int(ipy) and splite["state"] == 1:
                            splite["state"] = 0
                            if splite["type"] == 2:
                                self.score += 10
                            if splite["type"] == 3:
                                self.score += 50
                self.px -= self.pdx
            if self.worldMap[int(ipy_sub_yo)][int(ipx)] in [0, 2, 3]:
                if not int(ipy) == int((self.py - self.pdy) / 64.0):
                    for splite in self.spliteList:
                        if splite["ix"] == int(ipx) and splite["iy"] == int((self.py - self.pdy) / 64.0) and splite["state"] == 1:
                            splite["state"] = 0
                            if splite["type"] == 2:
                                self.score += 10
                            if splite["type"] == 3:
                                self.score += 50
                self.py -= self.pdy

        self.update_rays()

    def update_rays(self):
        self.ra = self.pa - DR * 30
        if self.ra < 0:
            self.ra += 2 * PI
        if self.ra > 2 * PI:
            self.ra -= 2 * PI 
        for i in range(len(self.rayList)):
            # 水平方向でチェック
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

            # 垂直方向でチェック
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
            lineH = (64 * 160) / disT
            if lineH > 160:
                lineH = 160
            lineO = 80 - lineH / 2
            self.depth[i] = disT

            # 壁の色変更に必要
            if hit == 0:
                rowNum = round(self.ry % 64 / 4) % 16
            if hit == 1:
                rowNum = round(self.rx % 64 / 4) % 16
            rayDict = {}
            rayDict["rx"] = self.rx
            rayDict["ry"] = self.ry
            rayDict["lineH"] = lineH
            rayDict["lineO"] = lineO
            rayDict["hit"] = hit
            rayDict["rowNum"] = rowNum
            self.rayList[i] = rayDict

            self.ra += DR / 4
            if self.ra < 0:
                self.ra += 2 * PI
            if self.ra > 2 * PI:
                self.ra -= 2 * PI

    def draw(self):
        pyxel.cls(1)
        for i, ray in enumerate(self.rayList):
            # 3D部分の描画
            pyxel.rect(i, 0, 4, ray["lineO"], 1)
            for columnNum in range(16):
                hd = ray["lineH"] / 16
                col = self.texture_wall[columnNum * 16 + ray["rowNum"]]
                pyxel.rect(i, ray["lineO"] + hd * columnNum, 4, hd, col)
            pyxel.rect(i, ray["lineH"] + ray["lineO"], 4, 480 - ray["lineH"] - ray["lineO"], 1)
            # splite部分の描画
            self.draw_splite()
        # 点数等を表示
        pyxel.text(190, 10, 'time: ', 5)
        pyxel.text(220, 10, f'{(pyxel.frame_count - self.startTime) // 30}', 0)
        pyxel.text(190, 20, 'score: ', 5)
        pyxel.text(220, 20, f'{self.score}', 0)

    def draw_dev(self):
        pyxel.cls(1)
        self.draw_2dMap()
        # 現在地の描画
        pyxel.circ(self.px / self.scale + self.shiftX, self.py / self.scale + self.shiftY, 5 / math.sqrt(self.scale), 3)
        # 方向
        pyxel.line(self.px / self.scale + self.shiftX, self.py / self.scale + self.shiftY, (self.px + self.pdx * 5) / self.scale + self.shiftX, (self.py + self.pdy * 5) / self.scale + self.shiftY, 15)
        for i, ray in enumerate(self.rayList):
            # ray部分の描画
            if i % 8 == 0:
                pyxel.line(self.px / self.scale  + self.shiftX, self.py / self.scale + self.shiftY, ray["rx"] / self.scale + self.shiftX, ray["ry"] / self.scale + self.shiftY, 3)
            # 3D部分の描画
            pyxel.rect(i + self.mapX * self.map2DSec + 12 + self.shiftX, 0, 4, ray["lineO"], 1)
            for columnNum in range(16):
                hd = ray["lineH"] / 16
                col = self.texture_wall[columnNum * 16 + ray["rowNum"]]
                # より立体感を出す
                # if ray["hit"] == 0:
                #     col += 3
                pyxel.rect(i + self.mapX * self.map2DSec + 12 + self.shiftX, ray["lineO"] + hd * columnNum, 4, hd, col)
            pyxel.rect(i + self.mapX * self.map2DSec + 12 + self.shiftX, ray["lineH"] + ray["lineO"], 4, 480 - ray["lineH"] - ray["lineO"], 1)
            # splite部分の描画
            self.draw_splite()
        pyxel.text(800, 350, f'time: {pyxel.frame_count // 30}', 0)

    def draw_2dMap(self):
        for y in range(self.mapY):
            for x in range(self.mapX):
                col = 0
                if self.worldMap[y][x] in [0, 2, 3]:
                    col = 0
                elif self.worldMap[y][x] == 1:
                    col = 1
                xo = self.map2DSec * x
                yo = self.map2DSec * y
                pyxel.rect(xo + self.shiftX, yo + self.shiftY, self.map2DSec, self.map2DSec, col)
                if x > 0:
                    pyxel.line(xo + self.shiftX, 0 + self.shiftY, xo + self.shiftX, self.mapY * self.map2DSec + self.shiftY, 4)
                if self.worldMap[y][x] == 2:
                    pyxel.circ((x + 0.5) * self.map2DSec + self.shiftX, (y + 0.5) * self.map2DSec + self.shiftY, 5 / self.scale, 3)
                if self.worldMap[y][x] == 3:
                    pyxel.circ((x + 0.5) * self.map2DSec + self.shiftX, (y + 0.5) * self.map2DSec + self.shiftY, 15 / self.scale, 3)
                x += 1
            if y > 0:
                pyxel.line(0 + self.shiftX, yo + self.shiftY, self.mapX * self.map2DSec + self.shiftX, yo + self.shiftY, 4)
            y += 1

    def draw_splite(self):
        # 開発モード表示用
        shiftX = self.mapX * self.map2DSec + 12 if self.mode == 0 else 0
        for splite in self.spliteList:
            # 現在地とスプライトを通る直線がx軸と為す角度
            theta = math.atan2(splite["y"] - self.py, splite["x"] - self.px)
            if theta < 0:
                theta += 2 * PI
            if theta > 2 * PI:
                theta -= 2 * PI
            # spliteが視野に入っているかチェック
            if self.pa - DR * 30 < theta and theta < self.pa + DR * 30:
                sx = splite["x"] - self.px
                sy = splite["y"] - self.py
                sz = splite["z"]
                CS = math.cos(-self.pa)
                SN = math.sin(-self.pa)
                a = sy * CS + sx * SN
                b = sx * CS - sy * SN
                sx = a
                sy = b
                sx = (sx * 216.0 / sy) + (240 / 2)
                sy = (sz * 216.0 / sy) + (160 / 2)

                # # scaleに合わせてスプライトを表示
                # scale = 16 * 160 / b
                # if scale < 0:
                #     scale = 0
                # if scale > 240:
                #     scale = 240
                # x = int(sx - scale / 2)
                # for i in range(16):
                #     if x > 0 and x < 240 and b < self.depth[x]:
                #         pyxel.rect(x + i, sy, 1, 1, 5)

                if sx > 0 and sx < 240 and b < self.depth[int(sx)]:
                    if splite["state"] == 1 and not(splite["type"] == 3 and pyxel.frame_count // 15 % 2 == 0):
                        pyxel.circ(sx + shiftX, sy, splite["size"], 3)

App()
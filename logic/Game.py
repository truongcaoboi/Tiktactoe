from math import pi
import random
import numpy as np
class Game:
    def __init__(self, idGame):
        self.nrow = 30
        self.ncol = 30
        self.matrix = np.zeros((self.nrow*self.ncol,))
        self.idplayer1 = 1
        self.idplayer2 = 2
        self.idGame = idGame
        self.gameOver = False
        self.indexPlayerCurrent = 0
        self.lastWinner = 0
        self.isAuto = True
        self.playerFirst = 1

    def reset(self):
        self.matrix = np.zeros((self.nrow*self.ncol,))
        self.gameOver = False
        if(self.lastWinner != 0):
            self.indexPlayerCurrent = self.lastWinner
            self.playerFirst = self.indexPlayerCurrent
        else:
            self.playerFirst = self.idplayer1
            self.indexPlayerCurrent = self.playerFirst
        data = {}
        data["idGame"] = self.idGame
        data["idPlayer"] = self.idplayer1
        data["idBot"] = self.idplayer2
        data["row"] = self.nrow
        data["col"] = self.ncol
        data["firstturn"] = self.playerFirst
        data["indexcurrent"] = self.indexPlayerCurrent
        return data

    def step(self, action):
        mark = self.updateGame(action)
        self.gameOver, array = self.checkWin(action)
        data = {}
        data["playerId"] = self.indexPlayerCurrent
        data["mark"] = mark
        data["action"] = action
        data["win"] = self.gameOver
        data["array"] = array
        if(self.indexPlayerCurrent == self.idplayer1):
            self.indexPlayerCurrent = self.idplayer2
        else:
            self.indexPlayerCurrent = self.idplayer1
        data["indexcurrent"] = self.indexPlayerCurrent
        if(self.gameOver):
            if(self.indexPlayerCurrent == self.idplayer1):
                self.lastWinner = self.idplayer2
            else:
                self.lastWinner = self.idplayer1
        return data

    def stepAuto(self):
        actions = []
        for i in range(len(self.matrix)):
            if(self.matrix[i] == 0):
                actions.append(i)
        action = actions[random.randrange(0, len(actions))]

        return self.step(action)

    def updateGame(self, action):
        mark = 0
        if(self.playerFirst == self.indexPlayerCurrent):
            mark = 1
        else:
            mark = 2
        if(self.matrix[action] == 0):
            self.matrix[action] = mark
        else:
            mark = -1
        print(f"{self.playerFirst} - {self.indexPlayerCurrent} - {action}")
        return mark
        
    def checkWin(self, action):
        mark = 1
        if(self.indexPlayerCurrent == self.playerFirst):
            mark = 1
        else:
            mark = 2
        row = action // self.nrow
        col = action % self.ncol
        
        check, array = self.checkWin2(row, col, mark)
        array2 = []
        for t in array:
            array2.append(t[0] * self.ncol + t[1])
        return check, array2
    
    def checkWin2(self, row, col, mark):
        marks = []
        start_r = row
        start_c = col
        end_r = row
        end_c = col
        array_win = []
        if(row < 5):
            start_r = 0
            end_r = row + 5
        elif(row >=25):
            start_r = row - 5
            end_r = 29
        else:
            start_r = row - 5
            end_r = row + 5
        if(col < 5):
            start_c = 0
            end_c = col + 5
        elif(col > 34):
            start_c = col - 5
            end_c = 39
        else:
            start_c = col - 5
            end_c = col + 5
        #ngang
        points = []
        checkfirst = False
        win = False
        for i in range(start_r, end_r,1):
            for j in range(start_c, end_c, 1):
                if(self.matrix[i*self.ncol + j] == mark):
                    points.append((i,j))
                elif(self.matrix[i*self.ncol + j] == 0):
                    if(not checkfirst and len(points) >= 4):
                        win = True
                        break
                    else:
                        checkfirst = False
                        points = []
                else:
                    if(len(points) >= 5):
                        win = True
                        break
                    else:
                        checkfirst = True
                        points = []
            if(win):
                break 
            else:
                if(not checkfirst and len(points) >= 4):
                    win = True
                    break
                elif(len(points) >= 5):
                    win = True
                    break
                else:
                    checkfirst = False
                    points = []
        if(win):
            return win, points
        #doc
        print("doc")
        points = []
        checkfirst = False
        win = False
        for j in range(start_c, end_c,1):
            for i in range(start_r, end_r, 1):
                if(self.matrix[i*self.ncol + j] == mark):
                    points.append((i,j))
                elif(self.matrix[i*self.ncol + j] == 0):
                    if(not checkfirst and len(points) >= 4):
                        win = True
                        break
                    else:
                        checkfirst = False
                        points = []
                else:
                    if(len(points) >= 5):
                        win = True
                        break
                    else:
                        checkfirst = True
                        points = []
            if(win):
                break 
            else:
                if(not checkfirst and len(points) >= 4):
                    win = True
                    break
                elif(len(points) >= 5):
                    win = True
                    break
                else:
                    checkfirst = False
                    points = []
        #cheo
        points = []
        checkfirst = False
        win = False
        for i in range(-5, 5, 1):
            if(row + i >= 0 and row + i < self.nrow and col + i >= 0 and col + i < self.ncol):
                pv = self.matrix[(row + i) * self.ncol + (col + i)]
                if(pv == mark):
                    points.append((row + i, col + i))
                elif(pv == 0):
                    if(not checkfirst and len(points) >= 4):
                        win = True
                        break
                    else:
                        checkfirst = False
                        points = []
                else:
                    if(len(points) >= 5):
                        win = True
                        break
                    else:
                        checkfirst = True
                        points = []
                        break
        if(win):
            return win, points 
        else:
            if(not checkfirst and len(points) >= 4):
                return True, points
            elif(len(points) >= 5):
                return True, points

        points = []
        checkfirst = False
        win = False
        for i in range(-5, 5, 1):
            if(row - i >= 0 and row - i < self.nrow and col - i >= 0 and col - i < self.ncol):
                pv = self.matrix[(row - i) * self.ncol + (col - i)]
                if(pv == mark):
                    points.append((row - i, col - i))
                elif(pv == 0):
                    if(not checkfirst and len(points) >= 4):
                        win = True
                        break
                    else:
                        checkfirst = False
                        points = []
                else:
                    if(len(points) >= 5):
                        win = True
                        break
                    else:
                        checkfirst = True
                        points = []
                        break
        if(win):
            return win, points 
        else:
            if(not checkfirst and len(points) >= 4):
                return True, points
            elif(len(points) >= 5):
                return True, points
            else:
                return False, points

    def foldGame(self):
        if(self.indexPlayerCurrent == self.idplayer1):
            self.lastWinner = self.idplayer2
        else:
            self.lastWinner = self.idplayer1     
        self.gameOver= True
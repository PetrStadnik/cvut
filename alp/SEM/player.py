
import base


class Player(base.Board):
    def __init__(self, player, size, stones):
        base.Board.__init__(self, player, size, stones)
        self.usedStone = [False]*len(self.stones) #all stones are free to use now 

        self.algorithmName = "Gpeemtbrlso"
        for i in range(len(stones)):
            self.stones[i] = self.stoneCenter(self.stones[i])
        self.serad()

        self.shouldBe = [[1,1],[-1,2],[-2,1],[-1,-1],[1,-2],[2,-1]]
        self.noBe = [[0,-1],[0,1],[-1,0],[1,0],[1,-1],[-1,1]]

    def stoneRL(self, stone):
        for ka in range(len(stone)):
            stone[ka][0], stone[ka][1] = self.rotateLeft(stone[ka][0], stone[ka][1])
        return stone

    def stoneCenter(self, stone):
        dp, dq = stone[0]
        for st in range(len(stone)):
            stone[st][0] -= dp
            stone[st][1] -= dq
        return stone

    def serad(self):
        ok = True
        while ok:
            ok = False
            for i in range(len(self.stones)-1):
                if len(self.stones[i]) < len(self.stones[i+1]):
                    sto = self.stones[i]
                    self.stones[i] = self.stones[i+1]
                    self.stones[i + 1] = sto
                    ok = True

    def umisti(self, stone):
        sou = []
        done = False
        a = 0
        b = 0
        c = 0
        for bp in self.board:  # vsechny sloupce v hraci deske
            if c == len(stone) and b > 0 and a == 0:
                break
            for bq in self.board[bp]:  # vsechny radky, ktere nalezi sloupci p
                a = 0
                b = 0
                c = 0

                for d in range(len(stone)):
                    if self.inBoard(bp + stone[d][0], bq + stone[d][1]):
                        if self.board[bp + stone[d][0]][bq + stone[d][1]] == 0:
                            c += 1

                for d in range(len(stone)):
                    for j in self.shouldBe:
                        if self.inBoard(bp + stone[d][0] + j[0], bq + stone[d][1] + j[1]):
                            if self.board[bp + stone[d][0] + j[0]][bq + stone[d][1] + j[1]] == self.player:
                                b += 1

                for d in range(len(stone)):
                    for j in self.noBe:
                        if self.inBoard(bp + stone[d][0] + j[0], bq + stone[d][1] + j[1]):
                            if self.board[bp + stone[d][0] + j[0]][bq + stone[d][1] + j[1]] == self.player:
                                a += 1

                if c == len(stone) and b > 0 and a == 0:
                    for d in range(len(stone)):
                        self.board[bp + stone[d][0]][bq + stone[d][1]] = self.player
                        sou.append([bp + stone[d][0], bq + stone[d][1]])
                    done = True
                    break
        return sou

    def prvni(self, stone):
        sou = []
        done = False
        a = 0
        b = 0
        c = 0
        for bp in self.board:  # vsechny sloupce v hraci deske
            if c == len(stone) and b > 0:
                break
            for bq in self.board[bp]:  # vsechny radky, ktere nalezi sloupci p
                a = 0
                b = 0
                c = 0

                for d in range(len(stone)):
                    if self.inBoard(bp + stone[d][0], bq + stone[d][1]):
                        if self.board[bp + stone[d][0]][bq + stone[d][1]] == 0:
                            c += 1
                        if bp + stone[d][0] == self.getStartCoordinates(self.player)[0] and bq + stone[d][1] == self.getStartCoordinates(self.player)[1]:
                            b += 1

                if c == len(stone) and b > 0:
                    for d in range(len(stone)):
                        self.board[bp + stone[d][0]][bq + stone[d][1]] = self.player
                        sou.append([bp + stone[d][0], bq + stone[d][1]])
                    done = True
                    break
        return sou

    def move(self):
        startp, startq = self.getStartCoordinates(self.player)
        if self.board[startp][startq] == 0:
            toReturn = []

            for i in range(len(self.stones)):
                for ri in range(6):
                    toReturn = self.prvni(self.stones[i])
                    if toReturn != []:
                        break
                    else:
                        self.stones[i] = self.stoneRL(self.stones[i])
                # self.saveImage("deska" + str(i) + ".png")
                if toReturn != []:
                    self.stones.pop(i)
                    break

            return toReturn
        else:
            toReturn = []

            for i in range(len(self.stones)):
                for ri in range(6):
                    toReturn = self.umisti(self.stones[i])
                    if toReturn!=[]:
                        break
                    else:
                        self.stones[i] = self.stoneRL(self.stones[i])
                #self.saveImage("deska" + str(i) + ".png")
                if toReturn != []:
                    self.stones.pop(i)
                    break

            return toReturn


if __name__ == "__main__":
    #size = 11

    #stones = base.loadStones("stones.txt")

    #p1 = Player(1, size, stones)  # player no. 1
    #print(p1.move())
    #print(p1.move())
    print("player")

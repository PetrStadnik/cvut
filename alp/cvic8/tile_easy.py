import base
import sys

def variace(p, arr):
    global newlist
    if 0 < len(arr):
        p += 1
        for i in range(len(arr)):
            s[p-2] = arr[i]
            variace(p, arr[:i]+arr[i+1:])

    else:
        global x
        x += 1
        newlist.append(s.copy())

def umisti(stone, num):
    done = False
    dp, dq = stone[0]
    for st in range(len(stone)):
        stone[st][0] -= dp
        stone[st][1] -= dq
    #print(stone)
    c = 0
    for bp in board.board:  # vsechny sloupce v hraci deske
        if c == len(stone):
            break
        for bq in board.board[bp]:  # vsechny radky, ktere nalezi sloupci p
            c = 0
            for d in range(len(stone)):
                if board.inBoard(bp + stone[d][0], bq + stone[d][1]):
                    if board.board[bp + stone[d][0]][bq + stone[d][1]] == 0:
                        c += 1
            if c == len(stone):
                for d in range(len(stone)):
                    board.board[bp + stone[d][0]][bq + stone[d][1]] = num + 1
                done = True
                break
    return done


if __name__ == '__main__':
    #size = 3
    #stones = base.loadStones("stones.txt")
    #board = base.Board(size)

    size = int(sys.argv[1])
    board = base.Board(size)
    stones = base.loadStones(sys.argv[2])

    x = 0
    newlist = []
    chars = ""
    for i in range(len(stones)):
        chars += str(i)
    chars = list(chars)
    s = [""] * len(chars)
    variace(1, chars.copy())

    exist = False
    f = open(sys.argv[3], "w")
    for i in range(len(newlist)):
        um = 0
        for p in board.board:  # vsechny sloupce v hraci deske
            for q in board.board[p]:  # vsechny radky, ktere nalezi sloupci p
                board.board[p][q] = 0
        for ii in range(len(stones)):
            if umisti(stones[int(newlist[i][ii])], int(newlist[i][ii])):
                um += 1
        if um == len(stones):
            exist = True
            for p in board.board:  # vsechny sloupce v hraci deske
                for q in board.board[p]:  # vsechny radky, ktere nalezi sloupci p
                    if board.board[p][q] == 0:
                        exist = False
            #board.saveImage("deska"+str(i)+".png")
            if exist:
                for pw in board.board:
                    for qw in board.board[pw]:
                        f.write("{} {} {}\n".format(pw, qw, board.board[pw][qw]))
            break

    if not exist:
        f.write("NOSOLUTION")
    f.close()

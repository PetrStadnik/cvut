import sys


def hledej(smer, u):
    global pr
    global dd
    go(smer)
    for s in smery:

        if m[pr[1]][pr[0]] == 4:
            print("Našel")
            print(dd)
            dd = []

            break

        if u == 15:
            dd = []
            break

        dd.append(s)
        hledej(s, u + 1)

def go(smer):
    if smer == "S":
        for i in range(pr[1], 0, -1):
            if m[pr[1]-1][pr[0]] !=1:
                pr[1] -=1
    if smer == "Z":
        for i in range(pr[0], 0, -1):
            if m[pr[1]][pr[0]-1] != 1:
                pr[0] -= 1
    if smer == "J":
        for i in range(len(m)-pr[1]-1):
            if m[pr[1]+1][pr[0]] != 1:
                pr[1] += 1
    if smer == "V":
        for i in range(len(m[0])-pr[0]-1):
            if m[pr[1]][pr[0+1]] != 1:
                pr[0] += 1
    print(pr)


max = 20
smery = ["S", "J", "V", "Z"]
pr = []
m = []
dd = []
#f = open(sys.argv[1], 'r')
f = open("mat.txt", 'r')
for line in f:
    m.append(list(map(int, line.split())))
for i in range(len(m)):
    if 2 in m[i]:
        pr.append(m[i].index(2))
        pr.append(i)
print(pr)
go("J")
go("V")
hledej("Z", 1)








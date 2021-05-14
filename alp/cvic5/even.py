import sys

if __name__ == '__main__':
    pole = []
    f = open(sys.argv[1], 'r')
    for line in f:
        pole.append(list(map(int, line.split())))


    width = len(pole[0])
    height = len(pole)


    r = []
    c = []

    for h in range(height):
        r.append(0)
        for w in range(width):
            if pole[h][w] % 2 == 0:
                r[h] += 1

    for w in range(width):
        c.append(0)
        for h in range(height):
            if pole[h][w] % 2 == 0:
                c[w] += 1

    mr = max(r)
    mc = max(c)

    for i in range(len(r)):
        if r[i] == mr:
            print(i)
    for i in range(len(c)):
        if c[i] == mc:
            print(i)



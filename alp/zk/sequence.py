import sys

if __name__ == '__main__':
    m = []
    p = []
    f = open(sys.argv[1], 'r')
    #f = open("mat.txt", 'r')
    for line in f:
        m.append(list(map(int, line.split())))


    o = 0
    for r in range(len(m)):
        if o > 0:
            p[-1].append(o)
            o = 0

        for s in range(len(m[0])):
            if m[r][s] > -1 and m[r][s] % 2 == 0:
                if o == 0:

                    p.append(["r", r, s])
                    o = 1
                else:
                    o += 1
            else:
                if o > 0:
                    p[-1].append(o)
                    o = 0

    o = 0
    for s in range(len(m[0])):
        if o > 0:
            p[-1].append(o)
            o = 0

        for r in range(len(m)):
            if m[r][s] > -1 and m[r][s] % 2 == 0:
                if o == 0:

                    p.append(["s", r, s])
                    o = 1
                else:
                    o += 1
            else:
                if o > 0:
                    p[-1].append(o)
                    o = 0

    if p == []:
        print("NEEXISTUJE")

    else:
        d = 0
        di = 0
        for k in range(len(p)):
            if p[k][3] > d:
                d = p[k][3]
                di = k

        for i in p[di]:
            print(str(i) + " ", end="")



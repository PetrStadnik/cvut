tahy = []


def p(a, b):
    print(str(a)+str(b))
    int(a)
    if int(d[b]) == 0:
        d[b] = d[a]
        d[a] = 0
        tahy.append(str(a)+str(b))
        print(d)
        return True
    else:
        print("chyba")
        return False

if __name__ == '__main__':

    d = list(map(int, input().split(" ")))
    print(d)

    while True:
        if d[0] == 1 and d[1] == 2 and d[2] == 3 and d[3] == 4 and d[4] == 5:
            break

        if d[0] > d[1]:
            if p(0, 6):
                if d[1] > d[2]:
                    p(1, 5)
                    p(2, 1)
                    p(3, 2)
                    p(1, 0)
                    if d[5] < d[2]:
                        p(5, 1)
                    else:
                        p(2, 1)
                        p(3, 2)
                        if d[4] > d[6]:
                            p(6, 3)
                        else:
                            p(4, 3)
                            p(5, 4)
                else:
                    p(1, 0)
                    p(2, 1)
                    p(3, 2)
                    if d[4] > d[6]:
                        p(6, 3)
                    else:
                        p(4, 3)
    vytisk = ""
    for t in tahy:
        vytisk += str(t) + " "
    print(vytisk)



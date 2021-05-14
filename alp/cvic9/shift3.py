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


def f(a):
    if d[a] == 0:
        return True
    else:
        return False


if __name__ == '__main__':
    kol = [0,1,2,3,6]
    d = list(map(int, input().split(" ")))
    print(d)

    while True:
        if d[0] == 1 and d[1] == 2 and d[2] == 3 and d[3] == 4 and d[4] == 5:
            break

        if d[4] != 5:
            if f(5):
                p(4, 5)
            else:
                if f(6):
                    for i in range(len(kol)):
                        if kol[i] == 0:
                            s = i

    vytisk = ""
    for t in tahy:
        vytisk += str(t) + " "
    print(vytisk)



import sys





if __name__ == '__main__':
    vys = ""
    pole = []
    f = open(sys.argv[1], 'r')
    #f = open("example.txt", 'r')
    for line in f:
        pole.append(list(map(str, line.split())))
    w = len(pole[0])
    for i in range(len(pole)):
        c = 1
        z = ""
        for k in range(w):
            if z == pole[i][k]:
                c += 1
            else:
                c = 1
            z = pole[i][k]
            if c == 5 and z != ".":
                vys += z


    # -------------------------------
    for k in range(w):
        c = 1
        z = ""
        for i in range(len(pole)):
            if z == pole[i][k]:
                c += 1
            else:
                c = 1
            z = pole[i][k]
            if c == 5 and z != ".":
                vys += z

    # -------------------------------
    for k in range(1 - len(pole), w):
        c = 1
        z = ""
        for i in range(len(pole)):

            if w > k >= 0:
                if z == pole[i][k]:
                    c += 1
                else:
                    c = 1
                z = pole[i][k]
                if c == 5 and z != ".":
                    vys += z

            k += 1
        # -------------------------------
    for k in range(1 - len(pole), w):
        c = 1
        z = ""
        for i in range(len(pole)):
            i = len(pole) - 1 - i
            if w > k >= 0:
                if z == pole[i][k]:
                    c += 1
                else:
                    c = 1
                z = pole[i][k]
                if c == 5 and z != ".":
                    vys += z

            k += 1


    if "x" in vys and "o" in vys:
        print("ERROR")
    elif "x" in vys:
        print("x")
    elif "o" in vys:
        print("o")
    elif len(vys) == 0:
        print(0)
    else:
        print("ERROR")


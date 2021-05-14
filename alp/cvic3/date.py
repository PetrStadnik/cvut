def makeArr():
    arr = "prvniho, druheho, tretiho, ctvrteho, pateho, sesteho, sedmeho, osmeho, devateho, desateho, jedenacteho, dvanacteho, trinacteho, ctrnacteho, patnacteho, sestnacteho, sedmnacteho, osmnacteho, devatenacteho, dvacateho, tricateho, ledna, unora, brezna, dubna, kvetna, cervna, cervence, srpna, zari, rijna, listopadu, prosince, jedna, dva, tri, ctyri, pet, sest, sedm, osm, devet, deset, jedenact, dvanact, trinact, ctrnact, patnact, sestnact, sedmnact, osmnact, devatenact, dvacet, tricet, ctyricet, padesat, sedesat, sedmdesat, osmdesat, devadesat, sto, dveste, trista, ctyrista, petset, sestset, sedmset, osmset, devetset, tisic, tisice"
    arr = arr.replace(" ", "")
    arr = arr.split(",")
    return arr


def getD(n):
    if int(n) < 21:
        d = arr[int(n) - 1]
    elif int(n) < 30:
        d = "dvacateho" + arr[int(n) - 21]
    else:
        d = "tricateho"
        if int(n) > 30:
            d += arr[int(n) - 31]
    return d

def getM(n):

    return arr[int(n) + 20]


def getY(ys):
    y = ""
    while len(ys) < 4:
        ys = "0" + ys
    if int(ys) >= 1000:

        if ys[0] == "1":
            y += arr[69]
        else:
            y += arr[32 + int(ys[0])] + arr[70]
    if int(ys) >= 100:
        if int(ys[1]) > 0:
            y += arr[59 + int(ys[1])]
    if int(ys[2:]) > 0:
        if int(ys[2:]) < 21:
            y += arr[32 + int(ys[2:])]
        else:
            y += arr[int(ys[2]) + 50]
            if int(ys[3]) > 0:
                y += arr[int(ys[3]) + 32]
    return y


if __name__ == '__main__':
    arr = makeArr()
    di = str(input())
    if "." in di:
        try:
            di = di.split(".")
            if len(di) == 3 and int(di[0]) < 32 and int(di[1]) < 13 and int(di[2]) < 4000:
                if int(di[0]) > 29 and int(di[1]) == 2:
                    print("ERROR")
                else:
                    if (int(di[1]) == 11 or int(di[1]) == 9 or int(di[1]) == 6 or int(di[1]) == 4) and int(di[0]) == 31:
                        print("ERROR")
                    else:
                        d = getD(di[0])

                        m = getM(di[1])

                        y = getY(di[2])

                        print(d + " " + m + " " + y)
            else:
                print("ERROR")
        except:
            print("ERROR")


    else:
        di = di.split(" ")

        for iday in range(1, 33):
          if di[0] == getD(str(iday)):
              break
        for imonth in range(1, 14):
          if di[1] == getM(str(imonth)):
              break
        for iyear in range(1, 4001):
          if di[2] == getY(str(iyear)):
              break

        if iday == 32 or imonth == 13 or iyear == 4000:
            print("ERROR")
        elif imonth == 2 and iday > 29:
            print("ERROR")

        else:
            if (int(imonth) == 11 or int(imonth) == 9 or int(imonth) == 6 or int(imonth) == 4) and int(iday) == 31:
                print("ERROR")
            else:
                print(str(iday)+"."+str(imonth)+"."+str(iyear))



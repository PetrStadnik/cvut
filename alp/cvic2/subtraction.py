def prepare(x):



    return x


def output(c):
    g = 0
    befnul = 0
    for f in range(len(c)):
        if c[f] == "0":
            befnul +=1
            g -= 1
        else:
            break
    if g == 0:
        c = c[:1] + "." + c[1:]
    elif g < 0:
        c = c[befnul:]
        c = c[:1] + "." + c[1:] + "e-" + str(bin(g))[3:]
    print(c)


def odecti(a, b):
    c = ""
    la = len(a)
    for f in range(la):
        la -= 1
        if a[la] == ".":
            c = "." + c
        else:
            if a[la] == b[la]:
                c = "0" + c
            elif a[la] == "1" and b[la] == "0":
                c = "1" + c
            elif a[la] == "0" and b[la] == "1":
                c = "1" + c
                if b[la-1] == ".":
                    if b[la-2] == "0":
                        b = b[:la-2] + "1" + b[la-1:]
                    else:
                        b = b[:la-2] + "0" + b[la-1:]
                else:
                    if b[la - 1] == "0":
                        b = b[:la-1] + "1" + b[la:]
                    else:
                        b = b[:la-1] + "0" + b[la:]


    print(c)
    return c


a = str(input())
b = str(input())
odecti(a, b)
#output(a)
n = ""
#a = a.replace(".", "")
if "e" in a:
    print("Je tam e")
    i = a.index("e")
    for r in range(i+1, len(a)):
        print(a[r])
        n = n + a[r]
    n = int(n, 2)
    print(n)
    a = a[:i]
    if n < 0:
        for f in range(n):
            a = "0" + a
    else:
        for f in range(n):
            a = "0" + a

print(a)







def prover(v):
    y = 1
    for i in range(len(v)):
        if v.count(v[i]) == 2:
            if abs((v[:i] + v[i + 1:]).index(v[i]) - i) != 2:
                y = 0
            else:
                y = 1
                break
    if y == 0:
        print(v)




def variace(p):

    if p <= len(chars):
        p += 1
        for i in chars:
            s[p-2] = i
            variace(p)

    else:
        global x
        x += 1
        print(x)
        prover(s)





if __name__ == '__main__':
    x = 0
    chars = input()
    s = [""] * len(chars)
    variace(1)

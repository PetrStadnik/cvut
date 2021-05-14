def over(v):
    o = 0
    global newlist
    for l in range(len(chars)):
        a = v.index(chars[l])
        b = (v[:a] + [""] + v[a + 1:]).index(chars[l])
        w = v[a+1:b]

        if len(w) > 0:
            if len(w) % 2 != 0:
                o = 1
                break
            else:
                k = 0
                for n in chars:
                    if n in w:
                        k += 1
                if k > len(w)/2:
                    o = 1
                    break
    if v.copy() in newlist:
        o = 1

    if o == 0:
        newlist.append(v.copy())


def variace(p, arr):
    #print(str(p) + "--->" + str(arr))
    if 0 < len(arr):
        p += 1
        for i in range(len(arr)):
            s[p-2] = arr[i]
            variace(p, arr[:i]+arr[i+1:])

    else:
        global x
        x += 1
        #print(x)
        over(s)


if __name__ == '__main__':
    newlist = []
    x = 0
    chars = list(input())
    s = [""] * len(chars) * 2
    z = chars.copy() * 2
    variace(1, z.copy())
    #print(len(newlist))
    for q in newlist:
        d = ""
        for t in q:
            d += t
        print(d)


def variace(p, arr):
    global newlist
    if 0 < len(arr):
        p += 1
        for i in range(len(arr)):
            s[p-2] = arr[i]
            variace(p, arr[:i]+arr[i+1:])

    else:
        global x
        x += 1
        #s[-1] = arr[0]
        newlist.append(s.copy())





if __name__ == '__main__':
    x = 0
    newlist = []
    chars = list(input())
    s = [""] * len(chars)
    variace(1, chars.copy())
    print(newlist)


if __name__ == '__main__':
    pA = list(map(int, input().split()))
    pB = list(map(int, input().split()))

    k = 0
    a = 0
    b = 0

    if len(pA) == len(pB):
        for i in range(len(pA)):
            if pA[i] == pB[i]:
                k += 2
            elif pA[i] > pB[i]:
                a += k + 2
                k = 0
            else:
                b += k + 2
                k = 0
        print(a - b)
    else:
        print("ERROR")



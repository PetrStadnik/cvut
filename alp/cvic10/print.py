import sys

def serad(f):
    ok = True
    while ok:
        ok = False
        for i in range(len(f) - 1):
            if int(f[i][0]) < int(f[i+1][0]):
                e = f[i]
                f[i] = f[i+1]
                f[i + 1] = e
                ok = True
    return f
fronta = []

for line in sys.stdin:
    if line[:2] == "-1" or line == -1:
        print(fronta.pop(0)[1])

    else:
        fronta.append(line.split())
        if len(fronta) > 1:
            fronta = serad(fronta)

for g in range(len(fronta)):
    print(fronta[g][1])




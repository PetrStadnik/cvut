
def rek1(s, t):
    if s > 0:
        r = int(rek1(s-1, t)) + int(t)
    else:
        r = 0
    return r

print(rek1(3,4))
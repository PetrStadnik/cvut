def f(a):
    y = 10**a - x
    return y

x = float(input())

if x > 1:
    x1 = 0
    x2 = x
else:
    x1 = -1/x
    x2 = 0

while abs(x1 - x2) >=0.000000001:
    s = (x1 + x2)/2
    if f(s) < 0:
        x1 = s
    else:
        x2 = s




print(s)

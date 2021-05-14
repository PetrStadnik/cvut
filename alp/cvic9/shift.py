import copy


def make(rozmisteni):
    global vys

    if rozmisteni[0]==final:
        vys=copy.deepcopy(rozmisteni[1])
        stop=True
    else:
        tahy=mozne_tahy(rozmisteni[0])
        for i in range(len(tahy)):
            c=[]
            aktual=copy.deepcopy(rozmisteni[0])
            last=copy.deepcopy(rozmisteni[1])
            tah=tahy[i]
            w = aktual[int(tah[1])]
            aktual[int(tah[1])] = aktual[int(tah[0])]
            aktual[int(tah[0])] = w
            last[0]=last[0]+tah
            if aktual not in visited:
                visited.append(aktual)
                c.append(aktual)
                c.append(last)
                fronta.append(c)
        stop=False
    return stop


def mozne_tahy(hlavolam):
    m=[]
    for i in range(len(hlavolam)):
        if int(hlavolam[i])==0:
            if i==0:
                m.append("10")
                m.append("60")
            elif i==1:
                m.append("01")
                m.append("21")
                m.append("51")
            elif i==2:
                m.append("12")
                m.append("32")
            elif i==3:
                m.append("23")
                m.append("43")
                m.append("63")
            elif i==4:
                m.append("34")
                m.append("54")
            elif i==5:
                m.append("15")
                m.append("45")
            elif i==6:
                m.append("36")
                m.append("06")
    return m


if __name__ == '__main__':
    vys=[]
    hlavolam=[]
    hlavolam.append(list(map(str,input().strip().split())))
    hlavolam.append([""])
    final=["1","2","3","4","5","0","0"]
    stop=False
    fronta=[]
    visited=[]
    fronta.append(hlavolam)

    while not stop:
        a=fronta.pop(0)
        if a[0]not in visited:
            visited.append(a[0])
        stop = make(a)

    for i in range(0,len(vys[0]),2):
        print(vys[0][i:i+2],end="")
        print(" ",end="")


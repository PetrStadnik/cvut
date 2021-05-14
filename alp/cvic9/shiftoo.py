import copy

def mozne_tahy(hlavolam):
    moznosti=[]
    for i in range(0,len(hlavolam)):
        if int(hlavolam[i])==0:
            if i==0:
                m="10"
                n="60"
                moznosti.append(m)
                moznosti.append(n)
            elif i==1:
                m="01"
                n="51"
                b="21"
                moznosti.append(m)
                moznosti.append(n)
                moznosti.append(b)
            elif i==2:
                m="12"
                n="32"
                moznosti.append(m)
                moznosti.append(n)
            elif i==3:
                m="23"
                n="43"
                b="63"
                moznosti.append(m)
                moznosti.append(n)
                moznosti.append(b)
            elif i==4:
                m="34"
                n="54"
                moznosti.append(m)
                moznosti.append(n)
            elif i==5:
                m="15"
                n="45"
                moznosti.append(m)
                moznosti.append(n)
            elif i==6:
                m="36"
                n="06"
                moznosti.append(m)
                moznosti.append(n)
    return moznosti


def zahraj(stav, odehrano):
    global konecstav
    global fronta
    global stop
    global visited
    global tahy_arr

    if stav[0]==konecstav:
        tahy_arr=copy.deepcopy(stav[1])
        stop=True
    else:
        mt = mozne_tahy(stav)
        for i in range(len(mt)):
            minulytah=[]
            l=[]
            aktualnistav=copy.deepcopy(stav)
            print(aktualnistav)
            minulytah=copy.deepcopy(odehrano)
            tah=mt[i]

            w=aktualnistav[int(tah[1])]
            aktualnistav[int(tah[1])] = aktualnistav[int(tah[0])]
            aktualnistav[int(tah[0])]=w

            minulytah.append(tah)
            if aktualnistav not in visited:
                visited.append(aktualnistav)
                stav = aktualnistav.copy()
                odehrano.append(minulytah)
        stop=False


if __name__ == '__main__':
    hlavolam = list(map(str,input().strip().split()))
    tahy_arr=[]
    odehrano = []
    konecstav=["1","2","3","4","5","0","0"]
    stop=False
    visited=[]
    fronta=hlavolam.copy()


    while not stop:
        if fronta[0]not in visited:
            visited.append(fronta[0])
        zahraj(fronta, odehrano)



    for i in range(0,len(tahy_arr[0]),2):
        print(tahy_arr[0][i:i+2],end="")
        print(" ",end="")

    vytisk = ""
    for t in tahy_arr:
        vytisk += str(t) + " "
    print(vytisk)


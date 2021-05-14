import copy



def tahy1(hlavolam):
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


def zahraj(stav):
    global konecstav
    global fronta
    global jetokonec
    global visited
    global ok

    if stav[0]==konecstav:
        ok=copy.deepcopy(stav[1])
        jetokonec=True
    else:
        tahy=tahy1(stav[0])
        for i in range(0,len(tahy)):
            minulytah=[]
            l=[]
            aktualnistav=copy.deepcopy(stav[0])
            print(aktualnistav)
            minulytah=copy.deepcopy(stav[1])
            tah=tahy[i]
            m=int(tah[0])
            n=int(tah[1])
            vymena1=aktualnistav[m]
            vymena2=aktualnistav[n]
            aktualnistav[m]=vymena2
            aktualnistav[n]=vymena1
            minulytah[0]=minulytah[0]+tah
            if aktualnistav not in visited:
                visited.append(aktualnistav)
                l.append(aktualnistav)
                l.append(minulytah)
                fronta.append(l)
        jetokonec=False
a = list(map(str,input().strip().split()))
ok=[]
hlavolam=[]
starttah=[""]
hlavolam.append(a)
hlavolam.append(starttah)



konecstav=["1","2","3","4","5","0","0"]
jetokonec=False
fronta=[]
visited=[]
fronta.append(hlavolam)


while not jetokonec==True:
    pop=fronta.pop(0)
    if pop[0]not in visited:
        visited.append(pop[0])
    zahraj(pop)



for i in range(0,len(ok[0]),2):
    print(ok[0][i:i+2],end="")
    print(" ",end="")


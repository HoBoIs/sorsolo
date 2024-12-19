import sender
from dataclasses import dataclass
import random
@dataclass
class Person:
    email:str
    name:str
    canthave:list[str]
    choosen:str
    def canGoTo(self,o:'Person'):
        return not (self.name in o.canthave or o.name in self.canthave)

def getData(fileName="data.csv"):
    with open(fileName, "r") as f:
        lines=f.readlines()
    persons: list[Person]=[]
    for line in lines:
        s=line.split(",")
        if len(s)==1:
            s=line.split("\t")
        if len(s)==1:
            if len(line)<3:
                continue
            else:
                print("Invalid line:", line)
        persons+=[Person(s[0].strip(),s[1].strip(),s[2:],"")]
    for p in persons:
        for i in range(len(p.canthave)):
            p.canthave[i]=p.canthave[i].strip()
    return persons
def checkLegit(ps:list[Person]):
    for fr in ps:
        choosenP=None
        for p in ps:
            if p.name==fr.choosen:
                choosenP=p
        if choosenP==None or not fr.canGoTo(choosenP):
            return False
    return True
def checkLegitOrder(ps:list[Person]):
    for fr,to in zip(ps,ps[1:]+[ps[0]]):
        if not fr.canGoTo(to):
            return False
    return True
cnt=0
def makeChoosensRec(ps:list[Person]):
    random.shuffle(ps)
    if not checkLegitOrder(ps):
        global cnt
        cnt+=1
        return makeChoosensRec(ps)
    for fr,to in zip(ps,ps[1:]+[ps[0]]):
        fr.choosen=to.name
    return ps

def makeChoosensRand(ps:list[Person]):
    random.shuffle(ps)
    global cnt
    while not checkLegitOrder(ps):
        cnt+=1
        random.shuffle(ps)
    for fr,to in zip(ps,ps[1:]+[ps[0]]):
        fr.choosen=to.name
    return ps

def makeChoosensGraphCircles(ps:list[Person],headIdx:int,fst:Person,maxCircles:int) -> list[Person] | None:
    if len(ps)==0:
        print("WTF")
    if len(ps)==1:
        if not ps[0].canGoTo(fst) or ps[0].name==fst.name:
            return None
        ps[0].choosen=fst.name
        return ps
    head=ps[headIdx]
    #others=(ps[headIdx:]+ps[:headIdx-1])
    ps2=ps.copy()
    ps2.remove(head)
    for i,o in zip(range(len(ps2)),ps2):
        if not head.canGoTo(o):
            continue
        res=makeChoosensGraphCircles(ps2,i,fst,maxCircles)
        if (res!=None):
            head.choosen=res[0].name
            return [head]+res
    if (head.canGoTo(fst)) and maxCircles>0:
        res=makeChoosensGraphCircles(ps2,0,ps2[0],maxCircles-1)
        if res !=None:
            head.choosen=fst.name
            return [head]+res
    return None
def makeChoosensGraph(ps:list[Person],headIdx:int,fst:Person) -> list[Person] | None:
    if len(ps)==0:
        print("WTF")
    if len(ps)==1:
        if not ps[0].canGoTo(fst):
            return None
        ps[0].choosen=fst.name
        return ps
    head=ps[headIdx]
    #others=(ps[headIdx:]+ps[:headIdx-1])
    ps2=ps.copy()
    ps2.remove(head)
    for i,o in zip(range(len(ps2)),ps2):
        if not o.canGoTo(head):
            continue
        res=makeChoosensGraph(ps2,i,fst)
        if (res!=None):
            head.choosen=res[0].name
            return [head]+res
    return None

def getMailToAndBody()->tuple[list[str],list[str]] :
    persons=getData()
    #if (0):
    #    persons=makeChoosensRand(persons)
    #    print(cnt)
    #else:
    random.shuffle(persons)
    personsSorted=makeChoosensGraph(persons,0,persons[0])
    if personsSorted!=None:
        persons=personsSorted
        print("Sucsess")
    else:
        print("No solution with just one circle.")
        personsSorted = makeChoosensGraphCircles(persons,0,persons[0],len(persons))
        if personsSorted!=None:
            print("Sucsess")
            persons=personsSorted
        else:
            print("Invalid input, can't find solution")
            return [],[]
    tos:list[str]=[]
    bodys:list[str] =[]
    #print(checkLegit(persons))
    for p in persons:
        tos+=p.email 
        bodys+=["Szia "+p.name+"\n\nA húzottad az antis húzásban: "+p.choosen+"\n(Lehet hogy már megkaptad ez egy automata email mindenkinek)\n\nAöl.: Boti python scriptje"]
        #print(p.name,p.choosen,p.canthave)
    return tos,bodys

tos,bodys=getMailToAndBody()

#sender.send_mails("horvath.botond.istvan@gmail.com","",tos,"[szentferenc] Antis karácsonyi húzás",bodys)

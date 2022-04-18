import random 
from IPython.display import HTML
from IPython.display import clear_output


DRAGON={'name':'Dragon','index':(0,1,2),'symbols':['&#x1F004','&#x1F005','&#x1F006'],'number':4}
WIND={'name':'Wind','index':(0,1,2,3),'symbols':['&#x1F000','&#x1F001','&#x1F002','&#x1F003'],'number':4}
FLOWER={'name':'Season','index':(0,1,2,3),'symbols':['&#x1F022','&#x1F023','&#x1F024','&#x1F025'],'number':1}
SEASON={'name':'Flower','index':(0,1,2,3),'symbols':['&#x1F026','&#x1F027','&#x1F028','&#x1F029'],'number':1}
BAMBOO={'name':'Bamboo','index':(0,1,2,3,4,5,6,7,8),'symbols':['&#x1F010','&#x1F011','&#x1F012','&#x1F013','&#x1F014','&#x1F015','&#x1F016','&#x1F017','&#x1F018'],'number':4}
CIRCLES={'name':'Circle','index':(0,1,2,3,4,5,6,7,8),'symbols':['&#x1F019','&#x1F01A','&#x1F01B','&#x1F01C','&#x1F01D','&#x1F01E','&#x1F01F','&#x1F020','&#x1F021'],'number':4}
CHARACTERS={'name':'Character','index':(0,1,2,3,4,5,6,7,8),'symbols':['&#x1F007','&#x1F008','&#x1F009','&#x1F00A','&#x1F00B','&#x1F00C','&#x1F00D','&#x1F00E','&#x1F00F'],'number':4}
TYPES=('Season','Flower','Dragon','Wind','Character','Bamboo','Circle')

class Tile():
    def __init__(self,type,num,symbol=''):
        self.num=num
        self.type=type
        self.symbol=symbol
    def __eq__(self,other):
        return self.num==other.num and self.type==other.type

class tileSet():
    def __init__(self):
        self.tiles=[]
        self.treasures=[]
    def discard(self,index):
        r=self.tiles[index]
        del(self.tiles[index])
        return r
    def pick(self,tile):
        self.tiles.append(tile)
        self.check()
    def full(self):
        return len(self.tiles)==13
    def check(self):
        # separate treasures from playing tiles
        self.treasures+=[x for x in self.tiles if x.type in TYPES[:2]]
        for x in self.treasures:
            if self.tiles.count(x):
                self.tiles.remove(x)
        # sort tiles
        sortedTiles=[]
        for t in TYPES:
            y=[x for x in self.tiles if x.type==t]
            y.sort(key= lambda x: x.num)
            sortedTiles+=y
        self.tiles=sortedTiles
    def alertTiles(self):
        #single tiles in hand
        singleTiles={}
        for x in self.tiles:
            if x.symbol not in singleTiles:
                singleTiles[x.symbol]=1
            else:
                singleTiles[x.symbol]+=1
        print (singleTiles)
    def isMahjong(self):
        def seqRemover(seq):
            a=seq.copy()
            i=0
            while len(a) and i<len(a)-2:
                x=a[i]
                if a.count(x+1) and a.count(x+2):
                    chowindex=[]
                    #print ('chow:',x,x+1,x+2)
                    chowindex.append(x)
                    chowindex.append(x+1)
                    chowindex.append(x+2)
                    for m in chowindex:
                        a.remove(m)
                else:
                    i+=1
            i=0
            while len(a) and i<len(a)-3:
                if a[i]==a[i+1]==a[i+2]==a[i+3]:
                    #print('kong')
                    del a[i:i+4]
                else:
                    i+=1
            i=0
            while len(a) and i<len(a)-2:
                if a[i]==a[i+1]==a[i+2]:
                    #print('pung')
                    del a[i:i+3]
                else:
                    i+=1
            return a
        # check if all tiles are in order, does not recognize kongss
        #need to exclude flowers and seasons
        final=[]
        for t in TYPES[2:]:
            seq=[x.num for x in self.tiles if x.type==t]    
            if len(seq):
                final+=seqRemover(seq)
        if len(final)==2:
            if final[0]==final[1]:
                return True
            else:
                return False
        else:
            return False
                    
    def show(self):
        tileDisplay=''
        for x in self.treasures:
            tileDisplay+=x.symbol+' '
        display (HTML(f'<span style="font-size: 40px;">{tileDisplay}</span>'))
        tileDisplay=''
        for x in self.tiles:
            tileDisplay+=x.symbol+' '
        display (HTML(f'<span style="font-size: 40px;">{tileDisplay}</span>'))
        
class heap():
    def __init__(self):
        lis=[]
        self.dis=[]
        for t in (DRAGON,WIND,CHARACTERS,BAMBOO,CIRCLES,SEASON,FLOWER): #,WIND,SEASON,FLOWER,CIRCLES,BAMBOO,CHARACTERS): 
            for i in range(t['number']):
                for k in t['index']:
                    a=Tile(t['name'],k,t["symbols"][k])
                    lis.append(a)
        random.shuffle(lis)
        self.lis=lis
    def extract(self):
        x=self.lis[0]
        del self.lis[0]
        return x
    def discard(self,tile):
        self.dis.append(tile)
    def remaining(self):
        return len(self.lis)
    def showDiscarded(self):
        tileDisplay=''
        for x in self.dis:
            tileDisplay+=x.symbol+' '
        display (HTML(f'<span style="font-size: 40px;">{tileDisplay}</span>'))
        
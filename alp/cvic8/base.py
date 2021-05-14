import copy
import math
from PIL import Image, ImageDraw
 
 
def loadStones(filename):
    f = open(filename,"r")
    stones = []
    for line in f:
        coords = list(map(int, line.rstrip().split()))
        if len(coords) > 0:
            stones.append( [] )
            for i in range(len(coords)//2):
                x = coords[2*i]
                y = coords[2*i+1]
                stones[-1].append([ x,y ] )
    return stones;
 
 
class Board:
    def __init__(self, size):
        self.size = size
        self.board = {}
 
        #create empty board as a dictionary
        self.b2 = {}
        for p in range(-self.size,self.size):
            for q in range(-self.size, self.size):
                if self.inBoard(p,q):
                    if not p in self.board:
                        self.board[p] = {}
                    self.board[p][q] = 0
 
                    if not q in self.b2:
                        self.b2[q] = {}
                    self.b2[q][p] = 0
 
        #this is for visualization and to synchronize colors between png/js
        self._colors = {}
        self._colors[-1] = "#fdca40" #sunglow
        self._colors[0] = "#ffffff" #white
        self._colors[1] = "#947bd3" #medium purple
        self._colors[2] = "#ff0000" #red
        self._colors[3] = "#00ff00" #green
        self._colors[4] = "#0000ff" #blue
        self._colors[5] = "#566246" #ebony
        self._colors[6] = "#a7c4c2" #opan
        self._colors[7] = "#ADACB5" #silver metalic
        self._colors[8] = "#8C705F" #liver chestnut
        self._colors[9] = "#FA7921" #pumpkin
        self._colors[10] = "#566E3D" #dark olive green
 
 
 
    def inBoard(self,p,q):
        """ return True if (p,q) is valid coordinate """
        return (q>= 0) and (q < self.size) and (p >= -(q//2)) and (p < (self.size - q//2))
 
 
    def rotateRight(self,p,q):
        pp = -q
        qq = p+q
        return pp,qq
 
    def rotateLeft(self, p,q):
        pp = p+q
        qq = -p
        return pp, qq
 
 
 
    def saveImage(self, filename):
        """ draw actual board to png
        """
 
        cellRadius = 25
        cellWidth = int(cellRadius*(3**0.5))
        cellHeight = 2*cellRadius
 
        width = cellWidth*self.size + cellRadius*3
        height = cellHeight*self.size
 
        img = Image.new('RGB',(width,height),"white")
 
        draw = ImageDraw.Draw(img)
 
        lineColor = (50,50,50)
 
 
        for p in self.board:
            for q in self.board[p]:
                cx = cellRadius*(math.sqrt(3)*p + math.sqrt(3)/2*q) + cellRadius
                cy = cellRadius*(0*p + 3/2*q) + cellRadius
 
                pts = []
                for a in [30,90,150,210,270,330]:
                    nx = cx + cellRadius * math.cos(a*math.pi/180)
                    ny = cy + cellRadius * math.sin(a*math.pi/180)
                    pts.append(nx)
                    pts.append(ny)
                color = "#ff00ff" #pink is for values out of range -1,..10
                if self.board[p][q] in self._colors:
                    color = self._colors[self.board[p][q]]
 
                draw.polygon(pts,fill=color)
                pts.append(pts[0])
                pts.append(pts[1])
                draw.line(pts,fill="black", width=1)
                draw.text([cx-3,cy-3], "{} {}".format(p,q), fill="black", anchor="m")
        img.save(filename)

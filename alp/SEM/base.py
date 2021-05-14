
import copy
import math
from PIL import Image, ImageDraw


"""
This is the base class for Gemblo game. 

Note that this base.py is different from base.py for HW08. Use only this file for Gemblo.

DO NOT MODIFY THIS FILE !!!!

Brute ALWAYS replaces base.py by it's own version to ensure that both players use the same base.py


For python experts: If you need to extend the Board class, make your own class (in player.py):

class Board2(base.Board):
    def __init__(self, plater, size, stones):
        base.Board.__init__(self, player, size, stones)

    def yourfunctions():
        pass

and update the Player class like this:

class Player(Board2):
    def __init__(self, player, size, stones):
        Board2.__init__(self, player, size ,stones)
        self.usedStone = [False]*len(self.stones) #all stones are free to use now 


"""


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
           

def updatePlayers(board, stones, value):
    """ fill the board by the stones with given value
        board: object of base.Board
        stones: [ [p1,q1], .... [pn,qn] ] - list of absolut coordinates of cells in the board
        value: color/value to be written to the board
    """
    try:
        for i in range(len(stones)):
            p,q = stones[i]
            board.board[p][q] = value #we write directly without checking if (p,q) is in the board
                                      #we assume that player/brute handle it
    except:
        print("Error when writing stones to the board. The player.move() returned invalid stones")
        return False
    return True
  

class Board:
    def __init__(self, player, size, stones):
        self.size = size
        self.board = {}
        self.stones = copy.deepcopy(stones)
        self.player = player #1 or -1
        self.algorithmName = "name of your method";
        self._playerName = "default"


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

    def getStartCoordinates(self, player):
        if player == 1: 
            return 0,0
        else:
            return (self.size)//2, self.size-1
        


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
        """ draw actual board to png. Empty cells are white, -1 = red, 1 = green, other values according to
            this list 
            -1 red, 0 = white, 1 = green 
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
     

    def a2c(self,p,q):
        x = p
        z = q
        y = -x -z
        return x,y,z

    def c2a(self, x,y,z):
        p = x
        q = z
        return p,q

    def distance(self,p1,q1,p2,q2):
        """ return distance between two cells (p1,q1) and (p2,q2) """
        x1,y1,z1 = self.a2c(p1,q1)
        x2,y2,z2 = self.a2c(p2,q2)
        dist = (  abs(x1-x2) + abs(y1-y2) + abs(z1-z2) ) // 2
        return dist

    def getScore(self, whichPlayer):
        """ return number of cells for given player """
        count = 0
        for p in self.board:
            for q in self.board[p]:
                if self.board[p][q] == whichPlayer:
                    count += 1
        return count

    def move(self):
        """ this method will be called by Brute. Return one of these:
            None -> if you CANNOT place any stone
            [ [p1,q1], ... [pn,qn] ] list of absolut (p,q) coordinates where you want to place a stone.
            
            For example, if you want to place one-cell stone to position p=1, q=-2:
            return [ [1,-2 ] ]

            If you want to place '3-cell-I-stone' at (1,1), (2,1) and (3,1):
            return [ [1,1] , [2,1], [3,1] ]

            If your start position is not filled, you have to start there!!
            
            startp, startq = self.getStartCoordinates(self.player)
            if self.board[startp][startq] == 0 -> you have to place first stone there!!
        """
        return None



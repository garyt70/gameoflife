"""
Thanks to http://trevorappleton.blogspot.co.uk/2013/07/python-game-of-life.html
Pre-requisite

Optional Setup a virtual env https://docs.python.org/3/library/venv.html
pip install pygame
"""

import pygame, sys, random
from pygame.locals import *

"""
UI setup variables
"""
FPS = 10 # frame refresh rate
WINDOWWIDTH=640
WINDOWHEIGHT=480
CELLSIZE = 10
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size"
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size"
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE) # number of cells wide
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE) # Number of cells high

# set up the colours
BLACK = (0,0,0)
WHITE = (255,255,255)
DARKGRAY = (40, 40, 40)
GREEN = (0,255,0)

"""
Constants for life rules
"""
CELLALIVE = 1
CELLKILL = 2
CELLOPEN = 0


"""
draw grid for game of life
"""
def drawgrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x,0),(x,WINDOWHEIGHT))
    for y in range (0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0,y), (WINDOWWIDTH, y))

"""
initiate the grid to be
"""
def blankGrid():
    gridDict = {}
    for y in range(CELLHEIGHT):
        for x in range(CELLWIDTH):
            gridDict[x,y] = 0
    return gridDict

"""
Random setup of cells.
"""
def seedLifeGrid(lifeDict):
    for item in lifeDict:
        lifeDict[item] = random.randint(0,1)
    #return lifeDict

"""
draw the correct colours on the grid based upon the lifecycle of the cell(item)
"""
def colourGrid(item, lifeDict):
    xPos = item[0] * CELLSIZE
    yPos = item[1] *CELLSIZE

    if lifeDict[item]==CELLALIVE:
        #we have life
        pygame.draw.rect(DISPLAYSURF, GREEN, (xPos, yPos, CELLSIZE, CELLSIZE))
    elif lifeDict[item]==CELLKILL:
        #we have death
        pygame.draw.rect(DISPLAYSURF, BLACK, (xPos, yPos, CELLSIZE, CELLSIZE))
    else:
        #no life or death
        pygame.draw.rect(DISPLAYSURF, WHITE, (xPos, yPos, CELLSIZE, CELLSIZE))

"""
Need to make sure the cell we are checking is within bounds of our grid
"""
def isCellInGrid(checkCell):
    isXinGrid = checkCell[0] < CELLWIDTH  and checkCell[0] >=0
    isYinGrid = checkCell [1] < CELLHEIGHT and checkCell[1]>= 0
    return isXinGrid and isYinGrid

"""
Work out if neighbour cells have an alive cell

    x - 1 | x = 0 | x + 1
    y - 1 | y - 1 | y - 1
    ------+-------+------
    x -  1 |   x   | x + 1
    y = 0 |   y   | y = 0
    ------+-------+------
    x -  1 | x = 0 | x + 1
    y + 1 | y + 1 | y + 1
"""
def countNeighbours(item, lifeDict):

    neighbourCount = 0

    for x in range(-1,2):
        for y in range(-1,2):
            if not (x==0 and y==0): #don't check self
                xloc = item[0]+x
                yloc  = item[1]+y

                #if off of gird then cyle to opposite side
                if xloc > CELLWIDTH:
                    xloc=0 #look ot start of grid
                elif xloc<0:
                    xloc = CELLWIDTH-1

                if yloc > CELLHEIGHT:
                    yloc=0
                elif yloc<0:
                    yloc = CELLHEIGHT-1

                checkCell = (xloc,yloc)

                #just to make sure
                if isCellInGrid(checkCell) :
                    if lifeDict[checkCell]==1: #cell is alive and so has affect
                        neighbourCount += 1


    #print("checkCell [%r]  count of neighbours[%s]" % (item, neighbourCount))
    return neighbourCount

"""
Remaps the grid based upon current cell state.
Creating a new grid acts as a screen buffer, which is better than modifying
single cells in a loop which would introduce line scanning effect.
"""
def tick(lifeDict):
    newTick = {}
    for item in lifeDict:
        numberNeighbours = countNeighbours(item, lifeDict)
        if lifeDict[item] == CELLALIVE: #cell is alive so check neighbourCount
            #if less than two neighbours then kill cell, not enough population
            #if greater than 3 then overcrowding so kill
            if numberNeighbours < 2 or numberNeighbours >3:
                newTick[item] = CELLKILL
            else:
                #keep it alive, we jabe 2 pr 3 niehbours
                newTick[item] = CELLALIVE
        else:
            #item is presently dead
            if numberNeighbours == 3:
                #reproduce
                newTick[item] = CELLALIVE
            else:
                #no change in state
                newTick[item] = CELLOPEN

    return newTick

def main():
    #initilise
    pygame.init()
    global DISPLAYSURF
    FPSCLOCK = pygame.time.Clock()

    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption('Game of Life')
    DISPLAYSURF.fill(WHITE)

    # setup our life in memory lif grid
    lifeDict=blankGrid()
    seedLifeGrid(lifeDict)

    while True: #main game loop
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
        lifeDict = tick(lifeDict)
        for item in lifeDict:
            colourGrid(item, lifeDict)
        drawgrid()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()

import pygame as pg
from pygame.locals import *
#(column, row)
pg.init()

class Cell:
    alive = (0,0,0)
    dead = (255, 255, 255)

    def __init__(self, left, top, life, pixelSize):
        self.rect = Rect(left * pixelSize, top * pixelSize, pixelSize, pixelSize)
        self.alive = life
        self.pixelSize = pixelSize

    def checkNeighbors(self, life, screenSize):
        aliveCount = 0
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dir in directions:
            thisCell = (self.rect.x // self.pixelSize + dir[0], self.rect.y // self.pixelSize + dir[1])

            if thisCell[0] < 0 or thisCell[0] > (screenSize[0] // self.pixelSize) - 1 or thisCell[1] < 0 or thisCell[1] > (screenSize[1] // self.pixelSize) - 1:
                continue

            if life[thisCell[0]][thisCell[1]].alive == True:
                aliveCount += 1

        return aliveCount

class Life:
    screenSize = (800,800)
    pixelSize = 10

    def __init__(self):
        self.width = self.screenSize[0] // self.pixelSize
        self.height = self.screenSize[1] // self.pixelSize
        self.life = [[Cell(col, row, False, self.pixelSize) for row in range(self.width)]for col in range(self.height)]
        self.screen = pg.display.set_mode(self.screenSize, RESIZABLE)

    def startGame(self):

        config = True
        while config:
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()

                if event.type == KEYDOWN:
                    if pg.key.get_pressed()[pg.K_SPACE]:
                        config = False

                if event.type == MOUSEBUTTONDOWN:
                    cursor = pg.mouse.get_pos()
                    self.life[cursor[0] // self.pixelSize][cursor[1] // self.pixelSize].alive = True

            self.drawMatrix()
            pg.display.flip()


    def drawMatrix(self):
        for row in self.life:
            for cell in row:
                if cell.alive:
                    color = cell.alive
                else:
                    color = cell.dead
                    
                pg.draw.rect(self.screen, color, cell.rect)

    def gameLoop(self):
        self.startGame()
        while True:
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()

            self.drawMatrix()

            makeAliveCells = []
            makeDeadCells = []
            for row in self.life:
                for cell in row:
                    aliveCount = cell.checkNeighbors(self.life, self.screenSize)
                    
                    if cell.alive:
                        if aliveCount < 2:
                            makeDeadCells.append(cell)
                        if aliveCount == 2 or aliveCount == 3:
                            makeAliveCells.append(cell)
                        if aliveCount > 3:
                            makeDeadCells.append(cell)
                    else:
                        if aliveCount == 3:
                            makeAliveCells.append(cell)

            for deadCell in makeAliveCells:
                deadCell.alive = True
            for aliveCell in makeDeadCells:
                aliveCell.alive = False
                  
            pg.display.flip()
            #pg.time.Clock().tick(1000)
    
life = Life()
life.gameLoop()
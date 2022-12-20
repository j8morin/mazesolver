#import
import pygame #pygame==2.4.3.dev8 version because of pyton 3.44
from sys import exit
from res import *
import random

#mazeSolver display 
displayWidth=600
displayHeight=600
mazeDimension=20   #Square of mazeDimension*mazeDimension cells
cellSize = displayWidth//mazeDimension

#Cell class
class Cell:
    def __init__(self, x, y, case, indx):
        self.x, self.y = x, y
        self.indx= indx
        if case == 0:
            self.walls = {'top':False , 'right': False, 'bottom': False, 'left': False}
        elif case == 1:
            self.walls = {'top':False , 'right': False, 'bottom': False, 'left': True}
        elif case == 2:
            self.walls = {'top':False , 'right': False, 'bottom': True, 'left': False}
        elif case == 3:
            self.walls = {'top':False , 'right': False, 'bottom': True, 'left': True}
        elif case == 4:
            self.walls = {'top':False , 'right': True, 'bottom': False, 'left': False}
        elif case == 5:
            self.walls = {'top':False , 'right': True, 'bottom': False, 'left': True}
        elif case == 6:
            self.walls = {'top':False , 'right': True, 'bottom': True, 'left': False}
        elif case == 7:
            self.walls = {'top':False , 'right': True, 'bottom': True, 'left': True}
        elif case == 8:
            self.walls = {'top':True , 'right': False, 'bottom': False, 'left': False}
        elif case == 9:
            self.walls = {'top':True , 'right': False, 'bottom': False, 'left': True}
        elif case == 10:
            self.walls = {'top':True , 'right': False, 'bottom': True, 'left': False} 
        elif case == 11:
            self.walls = {'top':True , 'right': False, 'bottom': True, 'left': True}
        elif case == 12:
            self.walls = {'top':True , 'right': True, 'bottom': False, 'left': False} 
        elif case == 13:
            self.walls = {'top':True , 'right': True, 'bottom': False, 'left': True} 
        elif case == 14:
            self.walls = {'top':True , 'right': True, 'bottom': True, 'left': False} 
        else:
            self.walls = {'top':True , 'right': True, 'bottom': True, 'left': True}

    #Draw cells:
    def drawCells(self):
        x= self.x * cellSize
        y= self.y * cellSize
        #Draw the case
        pygame.draw.line(screen, 'grey',(x,y), (x+cellSize, y),1)
        pygame.draw.line(screen, 'grey',(x+cellSize, y), (x+cellSize, y+cellSize),1)
        pygame.draw.line(screen, 'grey',(x+cellSize, y+cellSize), (x, y+cellSize),1)
        pygame.draw.line(screen, 'grey',(x,y+cellSize), (x, y),1)
        #Draw walls
        if self.walls['top']:
            pygame.draw.line(screen, 'black',(x,y), (x+cellSize, y),3)
        if self.walls['right']:
            pygame.draw.line(screen, 'black',(x+cellSize, y), (x+cellSize, y+cellSize),3)
        if self.walls['bottom']:
            pygame.draw.line(screen, 'black',(x+cellSize, y+cellSize), (x, y+cellSize),3)
        if self.walls['left']:
            pygame.draw.line(screen, 'black',(x,y+cellSize), (x, y),3)

#Individual class
class Individual:
    def __init__(self,x,y):
        self.x = x * cellSize + 15
        self.y = y * cellSize + 15
        self.cell= self.getCell()
    
    def drawIndividual(self):
        x, y = self.x, self.y
        pygame.draw.circle(screen, 'blue', (x,y), 5, width=0)

    def getCell(self):
        cell_x = (self.x-15) / cellSize
        cell_y = (self.y-15) / cellSize
        cell = cell_y*20 + cell_x
        return cell

    def move(self, direction, grid_cells):
        if direction == 'top':
            actualCell=self.getCell()
            for cell in grid_cells:
                if cell.indx==actualCell:
                    if not cell.walls['top']:
                        self.y += -cellSize
                        self.cell = self.getCell()
        if direction == 'right':
            actualCell=self.getCell()
            for cell in grid_cells:
                if cell.indx==actualCell:
                    if not cell.walls['right']:
                        self.x += cellSize
                        self.cell = self.getCell()
        if direction == 'down':
            actualCell=self.getCell()
            for cell in grid_cells:
                if cell.indx==actualCell:
                    if not cell.walls['bottom']:
                        self.y += cellSize
                        self.cell = self.getCell()  
        if direction == 'left':
            actualCell=self.getCell()
            for cell in grid_cells:
                if cell.indx==actualCell:
                    if not cell.walls['left']:
                        self.x += -cellSize
                        self.cell = self.getCell()

    def moveRandom(self):
        x=random.randint(0,3)
        if x==0:
            self.move('top',grid_cells)
        if x==1:
            self.move('right',grid_cells)
        if x==2:
            self.move('down',grid_cells)
        if x==3:
            self.move('left',grid_cells)



#Generate a grid of cells
mazeModel=[9,10,10,12,9,12,9,10,10,12,9,14,9,12,9,12,9,12,9,12,
          7,9,10,4,7,5,3,14,9,6,3,10,4,5,7,5,5,5,7,5,
          9,6,11,2,12,5,9,10,2,12,9,10,6,1,12,3,6,5,9,6,
          1,10,8,12,3,4,3,10,12,3,6,11,10,6,3,10,10,6,3,12,
          5,13,5,3,12,3,14,9,6,9,10,8,10,8,10,12,11,8,10,6,
          1,6,3,14,3,10,8,2,10,6,11,6,13,3,12,3,10,6,9,14,
          5,11,12,9,12,9,2,10,12,9,10,12,1,10,6,9,8,10,2,12,
          5,9,6,5,3,6,11,10,6,5,9,6,1,8,10,6,5,9,12,5,
          1,6,9,4,9,12,9,10,10,6,3,12,5,3,10,14,3,6,5,7,
          7,9,6,7,5,3,6,11,12,9,10,6,1,14,9,12,9,12,3,12,
          9,6,9,12,3,10,10,12,5,3,12,9,6,9,6,7,5,5,9,6,
          5,9,6,1,12,9,10,4,5,9,6,3,12,3,10,12,5,5,1,12,
          5,5,11,6,5,3,14,3,4,5,9,14,3,10,14,3,6,5,5,5,
          3,6,9,10,2,8,12,9,6,5,3,12,9,14,9,10,12,3,6,5,
          13,9,6,9,10,6,3,6,13,5,9,6,5,9,6,9,6,9,12,5,
          3,6,9,6,9,8,10,10,4,5,6,12,3,2,14,3,10,4,3,4,
          9,14,3,12,7,3,12,9,6,5,11,2,12,9,10,12,13,1,12,3,
          5,9,12,5,9,10,6,5,13,5,9,12,3,0,12,1,6,5,3,8,
          5,5,5,5,3,12,9,6,5,5,7,3,12,5,7,3,12,7,9,6,
          3,6,3,2,10,6,3,10,6,3,14,11,2,2,10,14,3,10,2,14]

#Fill a list of cell to  create a maze
x=0
y=0
grid_cells=[]
for i in range(len(mazeModel)):
    grid_cells.append(Cell(x, y, mazeModel[i], i))
    x+=1
    if x==20:
        x=0
        y+=1

#Individual
individuals=[]
#individuals.append(Individual(10,19))
individuals.append(Individual(9,13))

#Init pygame
pygame.init()
clock = pygame.time.Clock()
screen=pygame.display.set_mode((displayWidth,displayHeight))
pygame.display.set_caption('MazeSolver')

while True:
    screen.fill('white')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                for individual in individuals:
                    individual.move('top',grid_cells)
            if event.key == pygame.K_RIGHT:
               for individual in individuals:
                    individual.move('right',grid_cells)
            if event.key == pygame.K_DOWN:
                for individual in individuals:
                    individual.move('down',grid_cells)
            if event.key == pygame.K_LEFT:
                for individual in individuals:
                    individual.move('left',grid_cells)
    
    for cell in grid_cells:
        cell.drawCells()

    for individual in individuals:
        individual.moveRandom()
        individual.drawIndividual()
    

    pygame.display.update()
    clock.tick(5)
#import
import pygame #pygame==2.4.3.dev8 version because of pyton 3.44
from sys import exit

#mazeSolver display 
displayWidth=610
displayHeight=610
mazeDimension=20   #Square of mazeDimension*mazeDimension cells
cellSize = displayWidth//mazeDimension

#Cell class
class Cell:
    def __init__(self, x, y, case):
        self.x, self.y = x, y
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
        
        self.start, self.end = False, False

    #Draw cells:
    def drawCells(self):
        x= self.x * cellSize
        y= self.y * cellSize
        if self.walls['top']:
            pygame.draw.line(screen, 'black',(x,y), (x+cellSize, y),2)
        if self.walls['right']:
            pygame.draw.line(screen, 'black',(x+cellSize, y), (x+cellSize, y+cellSize),2)
        if self.walls['bottom']:
            pygame.draw.line(screen, 'black',(x+cellSize, y+cellSize), (x, y+cellSize),2)
        if self.walls['left']:
            pygame.draw.line(screen, 'black',(x,y+cellSize), (x, y),2)

#Generate a grid of cells
mazeModel=[9,10,10,12,9,12,9,10,10,4,9,14,9,12,9,12,9,12,9,12,
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
          3,6,3,2,10,6,3,10,6,3,12,11,2,2,10,14,3,10,2,14]

""" grid_cells=[]
for row in range(mazeDimension):
    for column in range(mazeDimension):
        grid_cells.append(Cell(row,column,20)) """

x=0
y=0
grid_cells=[]
for case in mazeModel:
    grid_cells.append(Cell(x, y, case))
    x+=1
    if x==20:
        x=0
        y+=1

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
    
    for cell in grid_cells:
        cell.drawCells()

    pygame.display.update()
    clock.tick(60)
#import
import pygame #pygame==2.4.3.dev8 version because of pyton 3.44
from sys import exit
from res import *
import random

#mazeSolver display 
pygame.font.init()
font=pygame.font.Font('envMaze/res/Sunflower.otf',15)

displayWidth=900
displayHeight=600
mazeDimension=20
cellSize = 600//mazeDimension


#Cell class
class Cell:
    def __init__(self, x, y, case, indx):
        self.x, self.y = x, y
        self.indx= indx
        self.start=False
        self.end=False
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

    def drawCells(self):
        x= self.x * cellSize
        y= self.y * cellSize
        #Draw the box
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
        #Change the color of the start and the end
        if self.start:
            pygame.draw.rect(screen,'red',(x,y,cellSize,cellSize),0,0)
        if self.end:
            pygame.draw.rect(screen,'red',(x,y,cellSize,cellSize),0,0)

#Individual class
class Individual:
    #x , y = column and row of the maze.
    def __init__(self,x,y):
        self.x = x * cellSize + 15
        self.y = y * cellSize + 15
        self.cell=self.getCell()
        self.history=[]
        self.fitness=0
    
    def drawIndividual(self):
        x, y = self.x, self.y
        pygame.draw.circle(screen, 'blue', (x,y), 5, width=0)

    def getCell(self):
        cell_x = (self.x-15) / cellSize
        cell_y = (self.y-15) / cellSize
        cell = cell_y*20 + cell_x
        return cell

    def move(self, direction, grid_cells):
        if direction == 0:
            self.history.append(0)
            actualCell=self.getCell()
            for cell in grid_cells:
                if cell.indx==actualCell:
                    if not cell.walls['top']:
                        self.y += -cellSize
                        self.cell = self.getCell()
        if direction == 1:
            self.history.append(1)
            actualCell=self.getCell()
            for cell in grid_cells:
                if cell.indx==actualCell:
                    if not cell.walls['right']:
                        self.x += cellSize
                        self.cell = self.getCell()
        if direction == 2:
            self.history.append(2)
            actualCell=self.getCell()
            for cell in grid_cells:
                if cell.indx==actualCell:
                    if not cell.walls['bottom']:
                        self.y += cellSize
                        self.cell = self.getCell()  
        if direction == 3:
            self.history.append(3)
            actualCell=self.getCell()
            for cell in grid_cells:
                if cell.indx==actualCell:
                    if not cell.walls['left']:
                        self.x += -cellSize
                        self.cell = self.getCell()

    def moveRandom(self):
        x=random.randint(0,3)
        self.move(x,grid_cells)
        # if x==0:
        #     self.move('top',grid_cells)
        # if x==1:
        #     self.move('right',grid_cells)
        # if x==2:
        #     self.move('down',grid_cells)
        # if x==3:
        #     self.move('left',grid_cells)

    def setFitness(self):
        #FV=(CC-SC)/(FC-CC) * 100 with SC=390 and FC=9
        SC=390
        FC=9
        CC=self.getCell()
        if (FC-CC==0):    #avoid division by zero
            self.fitness = 50000.0
        else:
            self.fitness = abs(((CC-SC)/(FC-CC))*100)

#Slider class
class Slider:
    def __init__(self, x, y,lowerValue,upperValue, description='Default:'):
        self.x, self.y = x, y
        self.description = description
        self.lowerValue = lowerValue
        self.upperValue = upperValue
        self.value = 0
        self.sliderSize = 250
        self.sliderX = self.x+10
        self.sliderY = self.y+20
        #self.sliderCursor = pygame.Rect(self.x+10,self.y+20,10,20)

    def drawSlider(self):
        #Text
        description=font.render(self.description,1,(0,0,0))
        screen.blit(description,(self.x,self.y))
        #Slider
        pygame.draw.line(screen,'grey',(self.x+10,self.y+30),(self.x+10+self.sliderSize,self.y+30),3)
        pygame.draw.rect(screen,'black',(self.sliderX,self.sliderY,10,20),0,0)
        #Value of the slider
        value =  font.render(str(self.value),1,(0,0,0))
        screen.blit(value,(self.x+self.sliderSize/2,self.y+35))
    
    def modifySlider(self):
        mouse_pos= pygame.mouse.get_pos()
        #Detect if the mouse is on the slider
        if self.sliderX-20<=mouse_pos[0]<=self.sliderX+20:
            if self.sliderY<=mouse_pos[1]<=self.sliderY+20:
                if pygame.mouse.get_pressed()[0] != 0:
                    self.sliderX = pygame.mouse.get_pos()[0]-5
                    multiplier = self.upperValue/self.sliderSize
                    self.value = int((pygame.mouse.get_pos()[0]-620)*multiplier)
                    #Minimum and Maximum
                    if self.value < self.lowerValue:
                        self.value=self.lowerValue
                        self.sliderX=self.x+10
                    if self.value > self.upperValue:
                        self.value=self.upperValue
                        self.sliderX=self.x+10+self.sliderSize
                    #Only even number
                    if self.value%2!=0:
                        self.value+=1
        return self.value

#Button class
class Button:
    def __init__(self,x,y,image,scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(int(width*scale), int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

    def drawButton(self):
        launchFunction = False
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            #On click
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked=True
                launchFunction=True
                print('START')
            #On release to make the button clickable again
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked=False
        #display the button
        screen.blit(self.image, (self.rect.x,self.rect.y))
        return launchFunction


#---------------------------------------------------------------------------------------------------------------------------
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
          9,14,3,12,7,3,12,9,6,5,11,2,12,9,10,12,13,1,12,7,
          5,9,12,5,9,10,6,5,13,5,9,12,3,0,12,1,6,5,3,12,
          5,5,5,5,3,12,9,6,5,5,7,3,12,5,7,3,12,7,9,6,
          3,6,3,2,10,6,3,10,6,3,14,11,2,2,10,14,3,10,2,14]

#Fill a list of cell to  create a maze
x=0
y=0
grid_cells=[]
for i in range(len(mazeModel)):
    c=Cell(x, y, mazeModel[i], i)
    if i==9:
        c.end=True
    if i==390:
        c.start=True
    grid_cells.append(c)
    x+=1
    if x==20:
        x=0
        y+=1
#---------------------------------------------------------------------------------------------------------------------------
#Genetic algorithm functions

def fitnessOperation(individuals):
    for individual in individuals:
        individual.setFitness()
    return individuals

def crossOverOperation(individuals):
    print("---------------------- Crossover ---------------------")
    #Delete the half of the individuals with the lowest fitness
    individuals.sort(key=lambda individual: individual.fitness, reverse= True)
    nbDelete=int(len(individuals)/2)
    print("initial len",len(individuals))
    for i in range(nbDelete):
        individuals.pop()
    print("delete half",len(individuals))
    #Create "couple" of parent
    individualCouples=[]
    for i in range(0,len(individuals),2):
        if i+1 != len(individuals):
            couple=(individuals[i],individuals[i+1])
            individualCouples.append(couple)
    #Addition operation for first child
    firstChild=Individual(10,19)
    history=[]
    for couple in individualCouples:
        for i in range(len(couple[0].history)):
            #print(couple[0].history[i],couple[1].history[i])
            history.append((couple[0].history[i]+couple[1].history[i])%4)
        firstChild.history=history
        individuals.append(firstChild)
    #Subtraction operation for the second child
    secondChild=Individual(10,19)
    history=[]
    for couple in individualCouples:
        for i in range(len(couple[0].history)):
            #print(couple[0].history[i],couple[1].history[i])
            if couple[0].history[i]>=couple[1].history[i]:
                history.append((couple[0].history[i]-couple[1].history[i])%4)
            else:
                history.append((couple[1].history[i]-couple[0].history[i])%4)
        secondChild.history=history
        individuals.append(secondChild)
    
    print ("Final len" ,len(individuals))
    return individuals

#A corriger!
def mutationOperation(individuals):
    for individual in individuals:
        n=random.randint(0,len(individuals)-1)
        x=random.randint(0,3)
        individual.history[n]=x
    return individuals
#---------------------------------------------------------------------------------------------------------------------------
#Individual
individuals=[]

#---------------------------------------------------------------------------------------------------------------------------
#Sliders
sliders=[]
maxMove=Slider(610,50,0,1000,'Maximum move per individual:')
sliders.append(maxMove)
population=Slider(610,100,0,50,'Population:')
sliders.append(population)

#---------------------------------------------------------------------------------------------------------------------------
#Buttons
start_img=pygame.image.load('envMaze/res/start.png')
start_bt = Button(700,400,start_img,0.2)

#---------------------------------------------------------------------------------------------------------------------------
#Init pygame
pygame.init()
clock = pygame.time.Clock()
screen=pygame.display.set_mode((displayWidth,displayHeight))
pygame.display.set_caption('MazeSolver')

nbMove=0
started=False
nbGeneration=0

movePerGeneration=20

#Main Loop
while True:
    clock.tick(60)
    screen.fill('white')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    for cell in grid_cells:
        cell.drawCells()

    for slider in sliders:
        slider.drawSlider()
        #For the momment sliders can only be modified to init the first generation.
        if nbGeneration==0:
            slider.value=slider.modifySlider()

    if start_bt.drawButton():
        started=True
    
    #Parameters can only be changed when it's not simulating
    if not started and nbGeneration==0:
        nbMoveMax=sliders[0].value
        nbPopulation=sliders[1].value  

    #Text
    generationTxt=font.render("Generation:"+str(nbGeneration),1,(0,0,0))
    screen.blit(generationTxt,(610,580))

    nbMoveTxt=font.render("nbMoveMax:"+str(movePerGeneration),1,(0,0,0))
    screen.blit(nbMoveTxt,(750,580))

    #Start simulation with start button!
    #Revoir cette partie pour:
    # Mouvements aléatoires*20 si generation0
    # Mouvements du genome + 20 mouvements aléatoire si generation N!=0
#Pourquoi pas if nbMove<nbMoveMax
                #if nbMove<movePerGeneration
                # du coup ca me fait 20 random move au premier et on el apsse à 40 avec un variable previousMove
                # pour le coup d'apres faire previousMove meme mouvement+ movePerGeneration radom

    if started:
        if nbGeneration==0:
            #Generate first generation
            for i in range (nbPopulation):
                if len(individuals)!=nbPopulation:
                 individuals.append(Individual(10,19))
        #Process pour gen0
        if nbGeneration==0 and nbMove<movePerGeneration:
            for individual in individuals:
                individual.moveRandom()
                individual.drawIndividual()
            nbMove+=1
        #Process
        if nbGeneration>0 and nbMove<movePerGeneration:
            for individual in individuals:
                #Premier move issu du genome
                if nbMove < movePerGeneration-20:
                    individual.move(individual.history[nbMove],grid_cells)
                    individual.drawIndividual()
                #20 mouve aléatoires
                else:
                    individual.moveRandom()
                    individual.drawIndividual()
            nbMove+=1
        #Fin de génération
        if nbMove==movePerGeneration:
            fitnessOperation(individuals)
            crossOverOperation(individuals)
            #mutationOperation(individuals)
            #put every indivual at the start (10,19)
            for individual in individuals:
                individual.x = 10 * cellSize + 15
                individual.y = 19 * cellSize + 15
                individual.cell = individual.getCell()
                individual.drawIndividual()
                #print(individual.history)

            nbGeneration+=1
            started=False  
            nbMove=0
            movePerGeneration+=20
            #print(individuals[0].fitness)




    
    
    # if started:
    #     #Useless but in case of (init)
    #     if nbMove==0:
    #         #Generate first population
    #         for i in range(nbPopulation):
    #             if len(individuals)!=nbPopulation:
    #                 individuals.append(Individual(10,19)) 
    #         nbMove+=1
    #     #Process the simulation
    #     elif nbMove<=nbMoveMax:
    #         for individual in individuals:
    #             if nbGeneration==0:
    #                 individual.moveRandom()
    #             else:
    #                 individual.move(individual.history[nbMove],grid_cells)
    #             individual.drawIndividual()
    #         nbMove+=1
    #     #End of the simulation / reset
    #     else:
    #         #Calculate Fitness of every individual
    #         fitnessOperation(individuals)
    #         crossOverOperation(individuals)
    #         mutationOperation(individuals)
    #         #put every indivual at the start (10,19)
    #         for individual in individuals:
    #             individual.x = 10 * cellSize + 15
    #             individual.y = 19 * cellSize + 15
    #             individual.cell = individual.getCell()
    #             individual.drawIndividual()

    #         nbGeneration+=1
    #         started=False  
    #         nbMove=0
    #         nbMoveMax+=20
        #     #Banc de test
        #     # print(individuals[0].history,len(individuals[0].history))

        #     # individuals.append(Individual(9,1))
        #     # individuals[0].fitness=individuals[0].getFitness()
        #     # print(individuals[0].fitness)

        #     # individuals.append(Individual(9,19))
        #     # individuals[1].fitness=individuals[1].getFitness()
        #     # print(individuals[1].fitness)
            

    pygame.display.flip()    
    pygame.display.update()
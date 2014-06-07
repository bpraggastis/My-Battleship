# B's Battle Ship 

######################### SET UP #################################

# import appropriate modules, initialize program, 
# and set initial values for parameters

import pygame
from pygame.locals import *
import random
import sys
import math

pygame.init()
pygame.font.init()
canvas_size = (1250, 750)
canv_center = [int(canvas_size[0]/2),int(canvas_size[1]/2)]
GRID_SIZE = 25 # This creates a canvas with a 50 x 30 grid, each square is 25x25 pixels

running = True

# Color calls:
GREEN = (0,128,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
col = 1
TOGGLE = (255,col*255,col*255)

message = "B's Battleship"

# Fonts
# Bf = pygame.font.SysFont("Fonts\times.ttf", 80, False, False )
# mf = pygame.font.SysFont("Fonts\times.ttf", 40, False, False )
# sf = pygame.font.SysFont("Fonts\times.ttf", 20, False, False )

Bf = pygame.font.SysFont(None, 80, False, False )
mf = pygame.font.SysFont(None, 40, False, False )
sf = pygame.font.SysFont(None, 20, False, False )

# helper functions

def text(string, font = sf, color = WHITE):
### returns surface consisting of text in the font and color specified. May then be blitted.)
    return font.render(string,0,color)

# Class Definitions 

class Ship:  
    def __init__(self,length,berth_pos, color = WHITE):
        self.berth_pos = berth_pos
        self.helm_pos = list(berth_pos)
        self.lilength = length
        self.length = length*GRID_SIZE
        self.orientation = 0 # default horizontal orientation, 1 will mean vertical
        self.color = color
        self.width = GRID_SIZE
        self.coord = set() # this is the set of coordinates on the board
        print("ship coord = ",self.coord)
        
        
        
    def rect(self):
        o = self.orientation
        g = GRID_SIZE
        return Rect(self.helm_pos,[(1-o)*self.length + o*g,o*self.length + (1-o)*g])
            
    def __str__(self):
        string = "ship's helm = [" + str(self.helm_pos[0]) + ", " + str(self.helm_pos[1]) + "]"
        return string
            
    def draw(self):
        o = self.orientation
        g = GRID_SIZE
        rect = Rect(self.helm_pos,[(1-o)*self.length + o*g,o*self.length + (1-o)*g])
        pygame.draw.rect(canvas,ship.color,rect)
        
    def flip(self):
        self.orientation = (self.orientation + 1)%2
        
    def inside(self,pos):
        ships_inside = self.rect()
        return ships_inside.collidepoint(pos[0],pos[1])
        
    def nset(self,n): # returns a list indicating position of ship with respect to a 10x10 grid
        lset = set()
        for i in range(0,self.lilength):
            lset.add(n + i*10**self.orientation) 
        return lset
        
        
        
class Board:
    def __init__(self,origin):
        self.origin = origin
        self.outline = Rect(self.origin,[10*GRID_SIZE,10*GRID_SIZE])
        self.unused = set()
        for i in range(0,100):
            self.unused.add(i)
        self.used = set()
        print("unused = ",self.unused)
        print("used = ",self.used)
        
        
    def v(self,x,y):   #pos is a integer coordinate pair indicating a vertex on game board 10x10
        return [self.origin[0] + x*GRID_SIZE, self.origin[1] + y*GRID_SIZE]
        
        
    def draw(self):
        for i in range(0,11):
            pygame.draw.line(canvas,WHITE,self.v(i,0),self.v(i,10))
            pygame.draw.line(canvas,WHITE,self.v(0,i),self.v(10,i))
            pygame.draw.rect(canvas,RED,self.outline,2)
            
    def chk_if_used(self,list):
        value = set(list) <= self.unused
        return value
            
    
    
        
            
    
    
# Event Handlers

def redraw_screen():
    global canvas, ship
    canvas.fill(BLUE)
    canvas.blit(text(message,Bf,WHITE),(50,50))
    if col == 0:
        cursor_pos = pygame.mouse.get_pos()
        for i in range(0,2):
            ship.helm_pos[i] = cursor_pos[i]-move_vector[i]
    ship.color = (255,col*255,col*255)
    ship.draw()
    my_board.draw()
    
    pygame.display.flip()
    
    
    
    
    
    
############### RUN THE PROGRAM ######################
    
canvas = pygame.display.set_mode(canvas_size,DOUBLEBUF|RESIZABLE)
pygame.display.set_caption("B's Battleship Game")
canvas.fill((255,0,0))
ship = Ship(2,[3*GRID_SIZE,6*GRID_SIZE])
my_board = Board([15*GRID_SIZE,5*GRID_SIZE])
message = "B's Battleship Game"
print (ship)

redraw_screen()
 
    
while running == True:
    redraw_screen
    pygame.event.pump()
    event=pygame.event.wait()
    if event.type==QUIT: 
        pygame.display.quit()
        running = False
        sys.exit(0)
    elif event.type==VIDEORESIZE:
        canvas=pygame.display.set_mode(event.dict['size'],DOUBLEBUF|RESIZABLE)
        canvas.fill((0,128,0))
        canvas.blit(text(message,Bf),(50,50))

    elif event.type == pygame.KEYDOWN:
        if event.key == K_SPACE and ship.color == RED:
            ship.flip()
        # elif event.key == K_RIGHT:
            # ship.helm_pos[0]+=GRID_SIZE
        # elif event.key == K_LEFT:
            # ship.helm_pos[0]-=GRID_SIZE
        # elif event.key == K_UP:
            # ship.helm_pos[1] -= GRID_SIZE
        # elif event.key == K_DOWN:
            # ship.helm_pos[1] += GRID_SIZE
            
    elif event.type == MOUSEBUTTONDOWN:
        new_pos = pygame.mouse.get_pos()
        if ship.inside(new_pos):
            if ship.coord != set():
                my_board.used.difference_update(ship.coord)
                my_board.unused.update(ship.coord)
                print("ship coord = ",ship.coord)
                print("used = ", my_board.used)
                print("unused = ",my_board.unused)
            col = (col +1)%2
            move_vector = [0,0]
            for i in range(0,2):
                move_vector[i] = new_pos[i] - ship.helm_pos[i]
    elif event.type == MOUSEBUTTONUP:
        if ship.color == RED:
            col = (col +1)%2
            if my_board.outline.contains(ship.rect()):
                x = (ship.helm_pos[0]+10 - my_board.origin[0])//GRID_SIZE
                y = (ship.helm_pos[1]+10 - my_board.origin[1])//GRID_SIZE
                pos = 10*y+x
                if my_board.chk_if_used(ship.nset(pos)): 
                # if x,y available for ship's helm then place them there
                    print(my_board.chk_if_used(ship.nset(pos)))
                    ship.helm_pos[0] = my_board.origin[0] + GRID_SIZE*x
                    ship.helm_pos[1] = my_board.origin[1] + GRID_SIZE*y
                    my_board.unused.difference_update(ship.nset(pos))
                    my_board.used.update(ship.nset(pos))
                    ship.coord = ship.nset(pos)
                    print("ship coord = ",ship.coord)
                    print("used = ", my_board.used)
                    print("unused = ",my_board.unused)
                    
                else: 
                    ship.helm_pos = list(ship.berth_pos)
                    ship.coord = set()
            else:
                ship.helm_pos = list(ship.berth_pos)
                ship.coord = set()
            
            

            
            
            
    redraw_screen()
            
        
        
        
        
        
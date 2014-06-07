# B's Battle Ship - this version creates player board and randomly generates fleet for the enemy.

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
YELLOW = (255,255,0)
GREY = (96,96,96)

ship = set() # this will hold the currently selected ship

message = "B's Battleship Game"


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
    def __init__(self,length,berth_pos, color = WHITE,orientation = 0):
        self.berth_pos = berth_pos
        self.helm_pos = list(berth_pos)
        self.lilength = length
        self.length = length*GRID_SIZE
        self.orientation = orientation # 0 = default horizontal orientation, 1 will mean vertical
        self.init_color = color
        self.color = tuple(color)
        self.width = GRID_SIZE
        self.coord = set()
         
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
        pygame.draw.rect(canvas,self.color,rect)
        
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
        
            
class Fleet:
    def __init__(self,visible = True):
        if visible == True:
            self.carrier = Ship(5,[3*GRID_SIZE,6*GRID_SIZE],GREEN) 
            self.battleship = Ship(4,[3*GRID_SIZE,8*GRID_SIZE],WHITE)
            self.destroyer = Ship(3,[3*GRID_SIZE,10*GRID_SIZE],GREY)
            self.submarine = Ship(3,[3*GRID_SIZE,12*GRID_SIZE],BLACK)
            self.patrol = Ship(2,[3*GRID_SIZE,14*GRID_SIZE],YELLOW)
                        
        else: 
            self.carrier = create_ship(5)
            self.battleship = create_ship(4)
            self.destroyer = create_ship(3)
            self.submarine = create_ship(3)
            self.patrol = create_ship(2)
            
        self.fleet = set([self.carrier,self.battleship,self.destroyer,self.submarine,self.patrol])
        for ship in self.fleet:
            print(ship)
            
        
    def draw(self):
        for boat in self.fleet:
            boat.draw()
            
    def fleet_used(self): # the set of squares used by the fleet
        lset = set()
        for boat in self.fleet:
            lset.update(boat.coord)
        return lset
            
    def select(self,pos):
        #new_pos = pygame.mouse.get_pos()
        for boat in self.fleet:
            if boat.inside(pos):
                return boat
        return set()

        
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
                
    def draw(self):
        for i in range(0,11):
            pygame.draw.line(canvas,WHITE,self.v(i,0),self.v(i,10))
            pygame.draw.line(canvas,WHITE,self.v(0,i),self.v(10,i))
            pygame.draw.rect(canvas,RED,self.outline,2)
            
    def chk_if_available(self,list):
        value = set(list) <= self.unused
        return value
        
    def grid(self,pos): # Given pixel coordinates return grid position
        return [(pos[0] - self.origin[0])//GRID_SIZE,(pos[1] - self.origin[1])//GRID_SIZE]

    def invgrid(self,pos): # Given grid position return pixel coordinates pos is a list
        return [pos[0]*GRID_SIZE + self.origin[0],pos[1]*GRID_SIZE + self.origin[1]]
        
    def v(self,x,y):   # returns pixel position given grid position given two number positions
        return [self.origin[0] + x*GRID_SIZE, self.origin[1] + y*GRID_SIZE]
    
# Event Handlers and Needed Functions

def redraw_screen():
    global canvas, ship
    canvas.fill(BLUE)
    canvas.blit(text(message,mf,WHITE),(50,50))
    if ship != set():
        cursor_pos = pygame.mouse.get_pos()
        for i in range(0,2):
            ship.helm_pos[i] = cursor_pos[i]-move_vector[i]

    friendly_board.draw()
    friendly.draw()
    enemy_board.draw()
    enemy.draw()
    
    pygame.display.flip()
    
def create_ship(n): # randomly chooses ships for the enemy board
    global enemy_board
    
    # generate a set containing all possible places a ship of size n could go
    # and then randomly choose one of these to be the position of the ship.
    # returns a list of squares from the board
    avail = []
    for y in range(0,10):
        for x in range(0,11-n):
            poss = []
            for j in range(0,n):
                poss.append(y*10 + x +j)
            if set(poss) <= enemy_board.unused:
                avail.append(poss)
    for x in range(0,10):
        for y in range(0,11-n):
            poss = []
            for j in range(0,n):
                poss.append(x + 10*(y+j))
            if set(poss) <= enemy_board.unused:
                avail.append(poss)
    lset = random.choice(avail) 
    pos = [lset[0]%10,lset[0]//10]
    
    lship = Ship(n,enemy_board.invgrid(pos),(80+lset[0],80 + lset[0],80 + lset[0]),1-(lset[1]%10 - lset[0]%10))
    lship.coord = lship.nset(lset[0])
    enemy_board.used.update(lship.coord)
    enemy_board.unused -= lship.coord
    print(lset)
    return lship
    

            
 
############### RUN THE PROGRAM ######################
    
canvas = pygame.display.set_mode(canvas_size,DOUBLEBUF|RESIZABLE)
pygame.display.set_caption("B's Battleship Game")
canvas.fill((255,0,0))
#ship = Ship(2,[3*GRID_SIZE,6*GRID_SIZE])
friendly_board = Board([9*GRID_SIZE,5*GRID_SIZE])
enemy_board = Board([24*GRID_SIZE,5*GRID_SIZE])
message = "B's Battleship Game"
#print (ship)
friendly = Fleet()
enemy = Fleet(False)


redraw_screen()
 
    
while running == True:
    #redraw_screen()
    pygame.event.pump()
    event=pygame.event.wait()
    
    if event.type==QUIT: 
        pygame.display.quit()
        running = False
        sys.exit(0)
        
    elif event.type==VIDEORESIZE:
        canvas=pygame.display.set_mode(event.dict['size'],DOUBLEBUF|RESIZABLE)
        canvas.fill((0,128,0))
        canvas.blit(text(message,mf),(25,25))

    elif event.type == pygame.KEYDOWN:
        if event.key == K_SPACE and ship != set():
            ship.flip()
            
    elif event.type == MOUSEBUTTONDOWN:
        new_pos = pygame.mouse.get_pos()
        ship = friendly.select(new_pos)
        if ship == set():
            pass
        else:
            if ship.coord != set():
                friendly_board.used.difference_update(ship.coord)
                friendly_board.unused.update(ship.coord)
                print("ship coord = ",ship.coord)
                print("used = ", friendly_board.used)
                print("unused = ",friendly_board.unused)
            ship.color = RED
            move_vector = [0,0]
            for i in range(0,2):
                move_vector[i] = new_pos[i] - ship.helm_pos[i]
                
    elif event.type == MOUSEBUTTONUP and ship != set():
    # if one of the ships is selected then deselect and determine where it should rest
        ship.color = ship.init_color
        #col = (col +1)%2
        if friendly_board.outline.contains(ship.rect()):
            x = (ship.helm_pos[0]+10 - friendly_board.origin[0])//GRID_SIZE
            y = (ship.helm_pos[1]+10 - friendly_board.origin[1])//GRID_SIZE
            pos = 10*y+x
            if friendly_board.chk_if_available(ship.nset(pos)): 
            # if x,y available for ship's helm then place them there
                print(friendly_board.chk_if_available(ship.nset(pos)))
                ship.helm_pos[0] = friendly_board.origin[0] + GRID_SIZE*x
                ship.helm_pos[1] = friendly_board.origin[1] + GRID_SIZE*y
                friendly_board.unused.difference_update(ship.nset(pos))
                friendly_board.used.update(ship.nset(pos))
                ship.coord = ship.nset(pos)
                print("ship coord = ",ship.coord)
                print("used = ", friendly_board.used)
                print("unused = ",friendly_board.unused)
                ship = set()
                move_vector = [0,0]
            else:
                ship.helm_pos = list(ship.berth_pos)
                ship.coord = set()
                ship.orientation = 0
                ship = set()
                
        else: 
            ship.helm_pos = list(ship.berth_pos)
            ship.coord = set()
            ship.orientation = 0
            ship = set()
        
    redraw_screen()
            
        
        
        
        
        
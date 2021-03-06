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
GRID_SIZE = 25 # We define the canvas in terms of a 50 x 30 grid, each square is 25x25 pixels

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
sf = pygame.font.SysFont(None, 25, False, False )

# helper functions

def text(string, font = sf, color = WHITE):
### returns surface consisting of text in the font and color specified. May then be blitted.
    return font.render(string,0,color)

# Class Definitions 

class Ship:  
    """
    Ship class defines a single ship. It requires a starting position, a color, and an orientation 0 = horizontal and 1 = vertical
    """
    
    def __init__(self,length,berth_pos, color = WHITE,orientation = 0, name = "a_ship"):
        self.berth_pos = berth_pos #location of the helm in pixels ############################### change this to reference the grid?
        self.helm_pos = list(berth_pos) 
        self.lilength = length
        self.length = length*GRID_SIZE
        self.orientation = orientation # 0 = default horizontal orientation, 1 will mean vertical
        self.init_color = color
        self.color = tuple(color)
        self.width = GRID_SIZE
        self.coord = set() #ships coordinates are the set of numbers in 0..99 that belong to the squares occupied by the ship
        self.name = name

             
    def rect(self):  # returns a rectangular representation of the ship
        o = self.orientation
        g = GRID_SIZE
        return Rect(self.helm_pos,[(1-o)*self.length + o*g,o*self.length + (1-o)*g])
            
    def __str__(self): # returns the grid position of the ship
        string = self.name + ": ship's helm = [" + str(self.helm_pos[0]) + ", " + str(self.helm_pos[1]) + "]"
        return string
            
    def draw(self): # draws a rectangle with the helm as one fixed corner using correct orientation
        o = self.orientation
        g = GRID_SIZE
        rect = Rect(self.helm_pos,[(1-o)*self.length + o*g,o*self.length + (1-o)*g])
        pygame.draw.rect(canvas,self.color,rect)
        
    def flip(self): # changes orientation
        self.orientation = (self.orientation + 1)%2
        
    def inside(self,pos): # is the pos position inside the ship?
        ships_inside = self.rect()
        return ships_inside.collidepoint(pos[0],pos[1])
        
    def nset(self,n): # returns a list indicating position of ship with respect to the 0..99 numbering of the board
        lset = set()
        for i in range(0,self.lilength):
            lset.add(n + i*10**self.orientation) 
        return lset
        
    def get_coordinates(self):
        return self.coord
        
    def update_coordinates(self, lset): #ships coordinates are the set of numbers in 0..99 that belong to the squares occupied by the ship
        self.coord.update(lset)
        
            
class Fleet:
    """
    Fleet class creates a fleet for the player berthed to the side for placement
    and for the enemy (the computer) randomly set onto the enemy board
    """
    
    def __init__(self,visible = True,name = "a_fleet"):
        if visible == True:
            self.carrier = Ship(5,[3*GRID_SIZE,8*GRID_SIZE],GREEN,0, "Air-craft carrier") 
            self.battleship = Ship(4,[3*GRID_SIZE,10*GRID_SIZE],WHITE,0, "Battleship")
            self.destroyer = Ship(3,[3*GRID_SIZE,12*GRID_SIZE],GREY,0, "Destroyer")
            self.submarine = Ship(3,[3*GRID_SIZE,14*GRID_SIZE],BLACK,0,"Submarine")
            self.patrol = Ship(2,[3*GRID_SIZE,16*GRID_SIZE],YELLOW,0,"Patrol Boat")
            self.name = name
                        
        else:

            self.carrier = create_ship(5, enemy_board, "Air-craft carrier")
            self.battleship = create_ship(4, enemy_board,"Battleship" )
            self.destroyer = create_ship(3, enemy_board,"Destroyer")
            self.submarine = create_ship(3, enemy_board,"Submarine")
            self.patrol = create_ship(2, enemy_board,"Patrol Boat")
            self.name = name
            
        self.fleet = set([self.carrier,self.battleship,self.destroyer,self.submarine,self.patrol])

    def __str__(self):
        for ship in self.fleet:
            print(ship)
        return self.name
                
        
        
    def draw(self):
        for boat in self.fleet:
            boat.draw()
            
    def fleet_used(self): # the set of squares used by the fleet
        lset = set()
        for boat in self.fleet:
            lset.update(boat.coord)
        return lset
            
    def select(self,pos): 
        # checks to see if the position given by pos is inside one of the fleet's boats and returns that boat      
        for boat in self.fleet:
            if boat.inside(pos):
                return boat
        return set()

        
class Board:
    """
    Board class defines a 10 x 10 grid using GRID_SIZE to determine the size of the squares.
    methods draw the board and keep track of which squares are occupied
    grid positions x,y lie in [0..9, 0..9]
    """
    
    def __init__(self,origin = [0,0]):
        self.origin = origin
        self.outline = Rect(self.origin,[10*GRID_SIZE,10*GRID_SIZE])
        self.unused = set()
        for i in range(0,100):
            self.unused.add(i)
        self.used = set()

                
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
        
    def get_used(self):
        return self.used
        
    def get_unused(self):
        return self.unused
        
    def update_used(self,lset):
        self.used.update(lset)
        
    def update_unused(self,lset):
        self.unused.update(lset)
        
    def remove_used(self,lset):
        self.used -= lset
        
    def remove_unused(self,lset):
        self.unused -= lset
        
    def select_square(self,pos): # return True if the square is occupied
        x = pos[0]
        y = pos[1]
        
        
        
    
###### Event Handlers and Needed Functions

def redraw_screen():
    ### blits the objects to the frame
    global canvas, ship
    canvas.fill(BLUE)
    canvas.blit(text(message,Bf,WHITE),[10*GRID_SIZE,GRID_SIZE])
    canvas.blit(text(player_header,sf,WHITE),[9*GRID_SIZE,6*GRID_SIZE])
    canvas.blit(text(player_header2,sf,WHITE),[8 *GRID_SIZE,7 * GRID_SIZE])
    canvas.blit(text(enemy_header,sf,WHITE),[27*GRID_SIZE,6*GRID_SIZE])

    if ship != set():
        cursor_pos = pygame.mouse.get_pos()
        for i in range(0,2):
            ship.helm_pos[i] = cursor_pos[i]-move_vector[i]

    friendly_board.draw()
    friendly.draw()
    enemy_board.draw()
    enemy.draw()
    canvas.blit(text(big_message,Bf,WHITE),[5*GRID_SIZE,20*GRID_SIZE])
    
    pygame.display.flip()
    
def create_ship(n, board = Board([25*GRID_SIZE,8*GRID_SIZE]), name = "a_ship"): 

    # generates a set containing all possible places a ship of size n could go
    # on the given board
    # and then randomly choose one of these to be the position of the ship.
    # It updates the used and unused squares on the board and
    # returns the helm position of the ship
    
    avail = []
    for y in range(0,10):
        for x in range(0,11-n):
            poss = []
            for j in range(0,n):
                poss.append(y*10 + x +j)
            if set(poss) <= board.unused:
                avail.append(poss)
    for x in range(0,10):
        for y in range(0,11-n):
            poss = []
            for j in range(0,n):
                poss.append(x + 10*(y+j))
            if set(poss) <= board.unused:
                avail.append(poss)
    lset = random.choice(avail) 
    pos = [lset[0]%10,lset[0]//10]

    lship = Ship(n,board.invgrid(pos),(67 + lset[0],80 + lset[0],80 + lset[0]),1-(lset[1]%10 - lset[0]%10), name) # all the fancy formulas are to get shades of grey 
        #########when we play we need to change this to blue
    lship.update_coordinates(lship.nset(lset[0])) # ships coordinates are the set of numbers in 0..99 that belong to the squares occupied by the ship
    board.update_used(lship.coord) 
    board.remove_unused(lship.coord) # this would have been better as a single function which updates and removes
    # print(name, lset)
    return lship
    

            
 
############### RUN THE PROGRAM ######################
    
canvas = pygame.display.set_mode(canvas_size,DOUBLEBUF|RESIZABLE)
pygame.display.set_caption("B's Battleship Game")
canvas.fill((255,0,0))

friendly_board = Board([10*GRID_SIZE,8*GRID_SIZE])
enemy_board = Board([25*GRID_SIZE,8*GRID_SIZE])
message = "B's Battleship Game"
player_header = "Friendly Waters - drag your boats here"
player_header2 = "Press <space> to change orientation of boat."
enemy_header = "Enemy Waters"

friendly = Fleet(True,"Friendly Fleet")
print( friendly)
print()
enemy = Fleet(False, "Enemy Fleet")
print( enemy)
ready = False
big_message = ""

redraw_screen()
 
    
while running == True:
    if len(friendly_board.get_used()) == 17:
        big_message = "Press the 'p' key to begin your sea battle."
        ready = True
    #redraw_screen()
    pygame.event.pump()
    event=pygame.event.wait()
    
    if event.type==QUIT: 
        pygame.display.quit()
        running = False
        sys.exit(0)
        
    elif event.type==VIDEORESIZE:
        canvas=pygame.display.set_mode(event.dict['size'],DOUBLEBUF|RESIZABLE)
        #redraw_screen()
        # canvas.fill((0,128,0))
        # canvas.blit(text(message,mf),(25,25))

    elif event.type == pygame.KEYDOWN:
        if event.key == K_SPACE and ship != set():
            ship.flip()
        elif event.key == K_p and ready == True:
            running = False
            big_message = ""

            
    
            
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
    
game_play = True
while game_play == True:
    pygame.event.pump()
    event=pygame.event.wait()
    
    if event.type==QUIT: 
        pygame.display.quit()
        running = game_play = False
        sys.exit(0)
    
            
        
        
        
        
        

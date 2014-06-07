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
canvas_size = (1024, 768)
canv_center = [int(canvas_size[0]/2),int(canvas_size[1]/2)]
GRID_SIZE = 30

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
        self.length = length*GRID_SIZE
        self.orientation = 0 # default horizontal orientation, 1 will mean vertical
        self.color = color
        self.width = GRID_SIZE
        
        
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
    
        
            
    
    
# Event Handlers

def redraw_screen():
    canvas, ship
    canvas.fill(BLUE)
    canvas.blit(text(message,Bf,WHITE),(50,50))
    if col == 0:
        move_pos = [0,0]
        for i in range(0,2):
            move_pos[i] = pygame.mouse.get_pos()[i] - ship.helm_pos[i]
            ship.helm_pos += pygame.mouse.get_pos()
    ship.draw()
    
    pygame.display.flip()
    
    
    
    
    
    
############### RUN THE PROGRAM ######################
    
canvas = pygame.display.set_mode(canvas_size,pygame.RESIZABLE)
pygame.display.set_caption("B's Battleship Game")
canvas.fill((255,0,0))
ship = Ship(5,canv_center)
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
        canvas=pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
        canvas.fill((0,128,0))
        canvas.blit(text(message,Bf),(50,50))

    elif event.type == pygame.KEYDOWN:
        if event.key == K_SPACE:
            ship.flip()
        elif event.key == K_RIGHT:
            ship.helm_pos[0]+=GRID_SIZE
        elif event.key == K_LEFT:
            ship.helm_pos[0]-=GRID_SIZE
        elif event.key == K_UP:
            ship.helm_pos[1] -= GRID_SIZE
        elif event.key == K_DOWN:
            ship.helm_pos[1] += GRID_SIZE
            
    elif event.type == MOUSEBUTTONDOWN:
        new_pos = pygame.mouse.get_pos()
        if ship.inside(new_pos):
            col = (col +1)%2
            ship.color = (255,col*255,col*255)
            
            
    redraw_screen()
            
        
        
        
        
        
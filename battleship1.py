# # B's Battle Ship

############################################
#This version is broken! Do not run


# Import appropriate modules , initialize program, and set constants
import pygame
from pygame.locals import *
import random
import sys
import math

pygame.init()
pygame.font.init()
canvas_size = (1024,768) # canvas will be resizable
center = [int(canvas_size[0]/2),int(canvas_size[1]/2)]

running = True
select = False
select_pos = [0,0]

# Colors for game
GREEN = (0,128,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0, 0, 255)
BLACK = (0,0,0)


# Fonts for Game
Bf = pygame.font.SysFont("Fonts\times.ttf", 80, False, False )
sf = pygame.font.SysFont("Fonts\times.ttf", 40, False, False )

# Class Definitions
class CircleShip:
    def __init__(self,pos,radius):
        self.pos = pos # center of the circle
        self.rad = radius
        self.color = WHITE
        
    def __str__(self):
        specs = "Center (" + str(self.pos[0]) + "," + str(self.pos[1]) + ")"
        return specs
        
    def draw_circle(self,color):
        pygame.draw.circle(canvas,self.color, self.pos,self.rad)
        
    def select_circle(self,pos):
        return dist(pos,self.pos) < self.rad
        
class RectShip:
    def __init__(self,pos,size):
        self.pos = pos
        self.color = WHITE
        self.size = size # dimensions of rectangle
        
    def __str__(self):
        specs = "Position (" + str(self.pos[0]) + "," + str(self.pos[1]) + ")"
        return specs
        
    def draw_rect(self,color=WHITE):
        [h,k] = self.pos
        list = [[h-150,k - 150],[h+150,k-150],[h+150,k+150],[h-150,k+150]]      
        pygame.draw.polygon(canvas,color,list,1)
        
    
# Helper Functions

def text(string, font = sf, color = WHITE):
### returns surface consisting of text in the font and color specified. May then be blitted.)
    return font.render(string,0,color)

def dist(p1,p2):
### returns distance between two points
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
    

# Event handler will receive event from queue and determine outcomes
def findevent():
    
    global canvas, running, canvas_size, center,  message, circ, select, select_pos, rect, cursor_pos
    
    new_cursor_pos = pygame.mouse.get_pos()
    
    for event in list(pygame.event.get()):
        if event.type == pygame.QUIT: # Close window or hit 'x' to quit the program
            running = False
            pygame.quit()
            sys.exit(0)
        if  event.type == pygame.KEYDOWN:
            if event.key == K_x:
                running = False
                pygame.quit()
                sys.exit(0)    
                
        if event.type==VIDEORESIZE:    # Drag to resize the screen
            canvas_size = event.dict['size']
         
        if select == False and event.type == MOUSEBUTTONDOWN and dist(new_cursor_pos,circ.pos) < circ. rad: # Turn on mouse to move circle
            select = True
            circ.color = RED
            cursor_pos = new_cursor_pos
            # move_pos = [0,0]
            # for i in range(0,2):
                # move_pos[i] = new_cursor_pos[i] - cursor_pos[i]
                # circ.pos[i] += move_pos[i]
            # cursor_pos = new_cursor_pos
            #canvas=pygame.display.set_mode(canvas_size,DOUBLEBUF|RESIZABLE)
            #canvas.fill(BLUE)
            #center = [int(canvas_size[0]/2),int(canvas_size[1]/2)]
            #[h,k] = center
            #message = "center is [" + str(h) + ", " + str(k) + "]"
            #rect = [[h-150,k - 150],[h+150,k-150],[h+150,k+150],[h-150,k+150]]      
            #pygame.draw.polygon(canvas,WHITE,rect,1)
            #circ.draw_circle(circ.color)
             
                    
        if event.type == MOUSEBUTTONUP:
            circ.color = WHITE
            select = False
            
            
            
def draw_handler():
    global circ, canvas, select, cursor_pos, canvas_size
    if select == True:    
        move_pos = [0,0]
        # cir.color = RED
        new_cursor_pos = pygame.mouse.get_pos()
        for i in range(0,2):
            move_pos[i] = new_cursor_pos[i] - cursor_pos[i]
            circ.pos[i] += move_pos[i]
        cursor_pos = new_cursor_pos
    
    canvas=pygame.display.set_mode(canvas_size,DOUBLEBUF|RESIZABLE)    
    canvas.fill(BLUE)
    center = [int(canvas_size[0]/2),int(canvas_size[1]/2)]
    [h,k] = center
    message = "center is [" + str(h) + ", " + str(k) + "]"
    rect = [[h-150,k - 150],[h+150,k-150],[h+150,k+150],[h-150,k+150]]      
    pygame.draw.polygon(canvas,WHITE,rect,1)
    circ.draw_circle(circ.color)
    canvas.blit(text(message),(50,50))   
           
    pygame.display.flip()
   
    pygame.event.clear()       
 
# Start frame
canvas = pygame.display.set_mode(canvas_size,pygame.RESIZABLE)
pygame.display.set_caption("B's Battleship Game")
canvas.fill(BLUE)

### initialize test ships rect and circ
ctr =[center[0]-150,center[0]-150] # Initial left top corner of the ship rect 
circ = CircleShip(center,100)
circ.draw_circle(WHITE)
rect = [ctr,[ctr[0]+300,ctr[1]],[ctr[0]+300,ctr[1]+300],[ctr[0],ctr[1]+300] ]
pygame.draw.polygon(canvas,WHITE,rect,1)
# cursor_pos = pygame.mouse.get_pos()



pygame.display.flip()

while running:
    findevent()
    draw_handler()

    
    

    
        

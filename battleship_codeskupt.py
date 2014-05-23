#Battleship from CodeAcademy

#Global calls
import random, simplegui
board1 = []
board2 = []
ship = []
n = "10"
c_size = 600
message = "Welcome to Battleship!"
ds = '--'
used_space = []

# Helper Functions to create the objects placed in the canvase

def create_board1():
###    !!!This creates a new 10 x 10 board filled with --'s
###    This board has 10 rows with 10 entries in each row!!!
    board1 = []
    for x in range(0,10):
        board1.append([ds]*10)
    return board1

def create_board2():
    ###This creates a new 10 x 10 board filled with O's!!!
    board2 = []
    for x in range(10):
        board2.append([ds] * 10)
    return board2

def t_width(string, size):
    ###Returns the width of a text string with a specified font
    ### size (integer type)  for placement on the board
    w = frame.get_canvas_textwidth(string,size,'serif')
    return w
    
def chk_avail(list):
    ##### returns the boolean value of whether or not the list contains any coordinates already in use
    global used_space
    status = True
    for i in range(0,len(list)):
        if list[i] in used_space:
            status = False
    return status
        


def create_ship(n):
    #####!!! creates a ship in open water of size n!!!
    global used_space
    avail = []
           
    for r in range(0,11-n):
        for c in range(0,10):
            poss = []
            for j in range(0,n):
                poss.append([r+j,c])
            if chk_avail(poss) == True:
                avail.append(poss)
    for r in range(0,10):
        for c in range(0,11-n):
            poss = []
            for j in range(0,n):
                poss.append([r,c+j])
            if chk_avail(poss) == True:
                avail.append(poss)
                
    pick = random.randrange(0,len(avail))
    ship = avail[pick]
    for j in range(0,len(ship)):
        used_space.append(ship[j])
    
    return ship
    
    ####disregard the rest
    if rand_dir == 0:
        ## ship's direction is horizontal so helm must be between column 0 and n-3 ##
        r =  random.randrange(0, 10)
        c =  random.randrange(0, 6)
        carrier = [[r,c],[r,c+1],[r,c+2],[r,c+3],[r,c+4]]
        
    else:
        ## ship's direction is vertical so helm must be between row 0 and n-3 ##
        r = random.randrange(0, 6)
        c = random.randrange(0, 10)      
        carrier = [[r,c],[r+1,c],[r+2,c],[r+3,c],[r+4,c]]
        
    ship_set = set(carrier)
        
    # generate a battleship which will take 4 places
    
    rand_dir = random.randrange(0,2)
    
    if rand_dir == 0:
        ##horizontal
        
        avail = h_avail(4).difference(carrier)
        avail_list = list(avail)
        pos = random.randrange(0,len(avail_list))
        #####################problem here is the set of available positions needs to be reduced so that the new ship doesn't overlap an old ship
  
    return ship
       
  
def newgame():
    ###This starts every game and randomly picks 5 ships.
    global board1, board2, message, hits, used_space, ship, carrier, battleship, destroyer, submarine, patrol_boat
    global ship_hits, ship_dict
    size = 10
    hits = 0
    ship_hits = [0,0,0,0,0]
    message = "Make your first guess!"
    used_space = []
    for j in range(0,5):
        ship.append([])
    
    ship[0] = carrier = create_ship(5)
    ship[1] = battleship = create_ship(4)
    ship[2] = destroyer = create_ship(3)
    ship[3] = submarine = create_ship(3)
    ship[4] = patrol_boat = create_ship(2)
    ship_dict = {0:"aircraft carrier", 1:"battleship", 2: "destroyer", 3: "submarine", 4: "patrol boat"}

    board1 = create_board1()
    board2 = create_board2()
        
    
    for i in range(0,5):
        print ship_dict[i] + " ",
        for j in range(0,len(ship[i])):
            print [ship[i][j][0]+1,ship[i][j][1]+1],
        print
    print
    print used_space
    print
       
    return 

def row_input(row):
    global r_guess, message
    if row == 'q':
        message =  "Game Over"
        frame.stop()
    else:
        r_guess = int(row)
        
def col_input(col):
    global c_guess, message
    if col == 'q':
        message = "Game Over"
        frame.stop()
    else:
        c_guess = int(col)
        
        

        
def play_game():
    ## player guesses until the ship is found or the player gets tired
    global board1, board2, n, r_guess, c_guess, message, hits, inp_row, inp_col, ship_dict, ship_hits
    
    n=10
    
    if inp_row.get_text() == 'q' or inp_col.get_text() == 'q':
        message =  "Game Over"
        frame.stop()
    elif inp_row.get_text() == '' or inp_col.get_text() == '':
        message =  "You must enter a row and column"
        return
    else:
        r_guess = int(inp_row.get_text())
        c_guess = int(inp_col.get_text())
    guess = [r_guess-1, c_guess-1]
    
    if (r_guess - 1) not in range(0,n) or (c_guess-1) not in range(0, n):
        message = "Your guess is not acceptable. Guess again."
        return
    


    if hits < 17 :            
        if board1[guess[0]][guess[1]] != ds :
            message = "You already guessed this position."
            
        elif guess in used_space:
            message = "Hit!"
            board1[guess[0]][guess[1]] = "H"
            hits = hits + 1
            for j in range(0,5):
                if guess in ship[j]:
                    ship_hits[j] +=1
                    if ship_hits[j] == len(ship[j]):
                        message =  "You sank my " + ship_dict[j] + "!"
                    break
            if hits == 17:
                message = message + " And YOU WON THE GAME!"
                return
        else:
            message = "Miss!"
            board1[guess[0]][guess[1]] = "X"
    else:
        message = "Click Reset to play again"
        print

    return
 
def draw_board(canvas):
    global board1, board2, message
    i = 1
    j = 1
    
    
   
    for row in board1[0:10]:
         w = t_width("  ".join(row[0:10]),25)
         canvas.draw_text("  ".join(row[0:10]),[.5 *(c_size - w),i*25+.30*c_size],25,"White")
         i += 1
            
    for row in board2:
         w = t_width("  ".join(row[0:10]),25)
         canvas.draw_text("  ".join(row[0:10]),[c_size +.5 *(c_size - w),j*25+.30*c_size],25,"White")
         j += 1
            
    canvas.draw_text(message,[.5*(2*c_size - t_width(message,35)),.85*c_size],35,"Red")
    canvas.draw_text("BATTLESHIP",[.5*(2*c_size - t_width("BATTLESHIP",45)),.15*c_size],45,"GREEN")
    
    
    if board1 != []:
        text1 = "This is the enemy board."
        text2 = "This is Your board."
        x1 = .5 *(c_size - t_width("  ".join(board1[0]),25))-25
        x2 = .30*c_size-10
        side = 50+ t_width("  ".join(board1[0]),25)
        canvas.draw_text(text1,[.5*(c_size - t_width(text1,25)),.25*c_size],25,"White")
        canvas.draw_polygon([(x1,x2),(x1+side,x2),(x1+side,x2+275),(x1,x2+275)],5,'blue')
        canvas.draw_text(text2,[c_size + .5*(c_size - t_width(text2,25)),.25*c_size],25,"White")
        canvas.draw_polygon([(c_size +x1,x2),(c_size +x1+side,x2),(c_size + x1+side,x2+275),(c_size + x1,x2+275)],5,'blue')
        
    
    
    
    
def reset():
    global n
    newgame()
    
def quit_game():
    frame.stop()

    
##   Create a frame

frame = simplegui.create_frame("Battleship",2*c_size,c_size)

## register event handlers


#  f.add_button("Range is [0, 100)", range100, 200)
#  f.add_button("Range is [0, 1000)", range1000, 200)

frame.set_draw_handler(draw_board)
frame.add_button("Start a new game!", reset, 200)
#inp_size = frame.add_input("Type in a board size between 5 and 10 and press ENTER", newgame, 80)
#inp_size.set_text("5")
frame.add_label("Guess the correct row and column below. Press q to quit.")
inp_row = frame.add_input("Row =",row_input,50)
inp_col = frame.add_input("Column =", col_input,50)
inp_row.set_text("")
inp_col.set_text("")
frame.add_button("Check your guess", play_game,200)
frame.add_button("Quit the game", quit_game,200)

### start frame

frame.start()
         
            
        
        

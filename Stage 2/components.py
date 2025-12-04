
#Used these so I save like 1 second when coding
#yeah they're all 5 characters as well so it's aligned when printing
light="Light"
dark="Dark "
none="None "

def initialise_board(size=8):
    board_temp=[] #temp list for board
    for x in range(0, size):
        temp_none=[] #temp list for storing none values
        for y in range(0, size):
            temp_none.append(none)
        board_temp.append(temp_none)
    #print(board_temp)
    #print(len(board_temp))

    #following 4 lines are to find middle 4 coordinates
    x1=size//2 
    x2=x1-1
    y1=size//2
    y2=y1-1 #yeah could've just used x1 and x2 didn't need to make y variables this is just so it's easier to understand for me
    

    board_temp[y1][x1]=light #this messed me up at first its y first then x I forgot that
    board_temp[y2][x1]=dark
    board_temp[y1][x2]=dark
    board_temp[y2][x2]=light
    return board_temp


def print_board(board):
    size=len(board)
    print(" ", end="|")
    for z in range(0, size):
        print(z+1, end="    |")#yeah printing numbers for columns and rows makes it easier to test as well. This line is for columns
    print("\n") #added numbers because it's easier to enter coordinates I barely understand this game right now this just makes it go next line instead of printing in this line
    for x in range(0, size):
        print(x+1, end="|") #prints the number for the rows
        for y in range(0, size):
            print(board[x][y], end="|")#Had "light" to 5 characters and if I left end="" it would combine the light and dark into one word so it looks better with a |
        print("\n")

possible_moves=[[1, 0], [-1, 0], [0, 1], [0, -1], [-1, 1], [-1, -1], [1, -1], [1, 1]]

def legal_move(colour, coordinates, board_object):
    x_coordinate=coordinates[0]-1 #just changes it to suit the list because lists starts from 0 not 1
    y_coordinate=coordinates[1]-1
    size=len(board_object)
    #following few lines of code validate if correct colour was entered
    if colour=="Dark" or colour=="dark" or colour==dark:
        opponent_colour=light
        colour=dark
    elif colour=="Light" or colour=="light" or colour==light:
        opponent_colour=dark
        colour=light
    else:
        return False
    if x_coordinate>-1 and x_coordinate<size: #validates that x coordinate is within range
       if y_coordinate>-1 and y_coordinate<size: #validates that y coordinate is within range
           if board_object[y_coordinate][x_coordinate]==none:
               for m in possible_moves: #now validates that if pieces can be outflanked I think that's the criteria for a valid move I barely understand this game
                   x1=x_coordinate+m[0]
                   y1=y_coordinate+m[1]
                   if x1<0 or x1>size-1: #makes sure nothing messes up if x coordinates are outside board
                        continue
                   if y1<0 or y1>size-1: #makes sure nothing messes up if y coordinates are outside board WHY IS THERE SO MUCH VALIDATION I NEED TO DO
                        continue
                   if board_object[y1][x1]==opponent_colour: #yeah this was annoying to code, checking if all spaces next to the coordinate are opponent colour or not and tries to find if pieces can be outflanked
                        while True: #now checks if pieces can be outflanked
                            x1=x1+m[0]
                            y1=y1+m[1]
                            if x1<0 or x1>size-1: #makes sure no errors appear if x coordinates are outside board
                                break
                            if y1<0 or y1>size-1: #makes sure no errors appear if y coordinates are outside board
                                break
                            if board_object[y1][x1]==colour: #if its the colour its a valid move yay
                                return True
                            elif board_object[y1][x1]==none: #if its none it continues and tries the next value in possible_moves
                                break               
           else:
               return False
       else:
           return False
    else:
        return False
    return False
    
'''
#just me testing it while coding
board=initialise_board()
print_board(board)
print(legal_move("dark", (6,5), board))
'''
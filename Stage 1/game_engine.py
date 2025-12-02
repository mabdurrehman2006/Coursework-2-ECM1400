def cli_coords_input():
    valid=[1, 2, 3, 4, 5, 6, 7, 8]
    check=True
    while check==True: #while loop to ensure that X coordinate is valid
        user_x=input("Enter X coordinate(Between 1 to 8)")
        if user_x.isdigit():
            check=False
            '''if int(user_x) in valid:
                check=False'''
        else:
            print("Invalid X coordinate")
            check=True
    check=True
    while check==True: #while loop to ensure that Y coordinate is valid
        user_y=input("Enter Y coordinate(Between 1 to 8)")
        if user_y.isdigit():
            check=False
            '''if int(user_y) in valid:
                check=False'''
        else:
            print("Invalid Y coordinate")
            check=True
    coordinates=(int(user_x), int(user_y))
    return coordinates

light="Light"
dark="Dark "
none="None "

def simple_game_loop():
    print("\n Welcome to this othello game \n")
    from components import initialise_board, print_board, legal_move
    board=initialise_board()
    print_board(board)
    size=len(board)
    move_counter=60
    turn=dark
    legal_move_available1=0

    #this whole loop checks if theres legal moves available for the current player
    while move_counter>0 and legal_move_available1<2:
        print(f"Current turn: {turn}")
        move_available=False
        for x in range(0, size):
            for y in range(0, size):
                    turn_available=legal_move(turn, (x+1, y+1), board)
                    if turn_available==True:
                        move_available=True
                        break
                    else:
                        continue
        if move_available==False:
                legal_move_available1+=1
                if turn==dark:
                     turn=light
                else:
                     turn=dark
                continue
        legal_move_available1=0
        
        coord_validation=False
        
        #this loop checks if coordinates are valid
        while coord_validation==False:
             coord=cli_coords_input()
             valid_coord=legal_move(turn, coord, board)
             #print(valid_coord)
             if valid_coord==True:
                  coord_validation=True
             else:
                  print(f"Not legal move. Try again. Coordinates must be between 1 and {size}")
                  continue
        
        
        x_coordinate=coord[0]-1
        y_coordinate=coord[1]-1
        if turn==dark:
            opponent_colour=light
        elif turn==light:
            opponent_colour=dark

        to_flip=[]
        #Now to flip each piece. This code is copied from my components.py file and then modified for this because I decided to be lazy
        possible_moves=[[1, 0], [-1, 0], [0, 1], [0, -1], [-1, 1], [-1, -1], [1, -1], [1, 1]]
        if x_coordinate>-1 and x_coordinate<size: #validates that x coordinate is within range
            if y_coordinate>-1 and y_coordinate<size: #validates that y coordinate is within range
                if board[y_coordinate][x_coordinate]==none:
                    for m in possible_moves: #now validates that if pieces can be outflanked I think that's the criteria for a valid move I barely understand this game
                        x1=x_coordinate+m[0]
                        y1=y_coordinate+m[1]
                        if x1<0 or x1>size-1: #makes sure nothing messes up if x coordinates are outside board
                            continue
                        if y1<0 or y1>size-1: #makes sure nothing messes up if y coordinates are outside board WHY IS THERE SO MUCH VALIDATION I NEED TO DO
                            continue
                        if board[y1][x1]==opponent_colour: #yeah this was annoying to code, checking if all spaces next to the coordinate are opponent colour or not and tries to find if pieces can be outflanked
                            while True: #now checks if pieces can be outflanked
                                to_flip.append([x1, y1])
                                x1=x1+m[0]
                                y1=y1+m[1]
                                if x1<0 or x1>size-1: #makes sure no errors appear if x coordinates are outside board
                                    to_flip=[]
                                    break
                                if y1<0 or y1>size-1: #makes sure no errors appear if y coordinates are outside board
                                    to_flip=[]
                                    break
                                if board[y1][x1]==turn: #if its the colour its a valid move yay
                                    for t in to_flip: #now flips the piece
                                        board[t[1]][t[0]]=turn
                                    to_flip=[]
                                    break
                                elif board[y1][x1]==none: #if its none it continues and tries the next value in possible_moves
                                    to_flip=[]
                                    break               
                
        board[y_coordinate][x_coordinate]=turn 
        move_counter-=1 #decreases move counter 

        #Now changes the turn to other colour
        if turn==dark:
            turn=light
        else:
            turn=dark
        print_board(board)
        continue
    
    #Calculates score
    dark_score=0
    light_score=0
    for x in range(0, size):
        for y in range(0, size):
            if board[y][x]==dark:
                dark_score+=1
            elif board[y][x]==light:
                light_score+=1
    
    #prints score
    print(f"Dark score: {dark_score}")
    print(f"Light score: {light_score}")

    #prints winner
    if dark_score<light_score:
        print("Light wins")
    elif dark_score>light_score:
        print("Dark wins")
    else:
        print("Draw")

             
            
        
             
        
if __name__=="__main__":
    simple_game_loop()
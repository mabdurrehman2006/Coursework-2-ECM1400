from flask import Flask, render_template, request, jsonify
import flask
import json
from components import initialise_board, print_board, legal_move

app = Flask(__name__)

light="Light"
dark="Dark "
none="None "

#board=None
#turn=dark

def legal_move_check(board, player): #checks if there's any legal moves available and returns true if there is
    size=len(board)
    for x in range(size):
        for y in range(size):
            if legal_move(player, (x+1, y+1), board):
                return True
    return False

@app.route('/')
def start():
    global board, turn, move_counter #makes these 3 variables global variables so I can access them in other functions
    board=initialise_board()
    turn=dark
    move_counter=60 
    return render_template("index.html", game_board=board)

@app.route('/move')
def move():
    global board, turn, move_counter
    x=request.args.get("x") #fetches x coordinate
    y=request.args.get("y") #fetches y coordiante
    if move_counter <= 0: #checks if board is full
                dark_score=0
                light_score=0
                #now calculates score if board is full
                for x in range(0, size):
                    for y in range(0, size):
                        if board[y][x]==dark:
                            dark_score+=1
                        elif board[y][x]==light:
                            light_score+=1
                #prints winner
                if dark_score<light_score:
                    winner=light
                    return jsonify(board=board, finished=f"{winner.strip()} has won")
                elif dark_score>light_score:
                    winner=dark
                    return jsonify(board=board, finished=f"{winner.strip()} has won")
                else:
                    winner="draw"
                    return jsonify(board=board, finished=f"It's a {winner}")
    try: #tries to convert x and y coordinate to integers. They should always be integers anyway using the gui
        x=int(x) 
        y=int(y)
    except:
        return jsonify(status="fail", message="coordinates not integers")
    valid_move=legal_move(turn, (x, y), board) 
    if valid_move==True: #checks if the move is valid
        #now subtracts one from both x and y coordinates
        x_coordinate=x-1
        y_coordinate=y-1 
        size=len(board) #calculates size of board

        #defines opponent colour because I copied the piece flipping code from my game_engine.py file
        if turn==dark:
            opponent_colour=light
        else:
            opponent_colour=dark
        possible_moves=[[1, 0], [-1, 0], [0, 1], [0, -1], [-1, 1], [-1, -1], [1, -1], [1, 1]]
        to_flip=[]
        
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

        #updates the coordinate selected and decreases move counter        
        board[y_coordinate][x_coordinate]=turn 
        move_counter-=1
        if move_counter==0: #checks if move counter has reached 0
                dark_score=0
                light_score=0
                for x in range(0, size):
                    for y in range(0, size):
                        if board[y][x]==dark:
                            dark_score+=1
                        elif board[y][x]==light:
                            light_score+=1
                #prints winner this is really inefficient idk how I tried programming it at first like I really don't need winner= but I had the return jsonify outside the if statements before
                if dark_score<light_score:
                    winner=light
                    return jsonify(board=board, finished=f"{winner.strip()} has won")
                elif dark_score>light_score:
                    winner=dark
                    return jsonify(board=board, finished=f"{winner.strip()} has won")
                else:
                    winner="draw"
                    return jsonify(board=board, finished=f"It's a {winner}")
                

        if turn==dark:
            next_turn=light
        else:
            next_turn=dark
        #Now checks if next player can make a move
        if legal_move_check(board, next_turn):
            turn=next_turn
            return jsonify(status="success", board=board, player=turn)
        else: 
            if legal_move_check(board, turn)==False: #checks if the current player cannot make a move and then counts score and outputs winner
                dark_score=0
                light_score=0
                for x in range(0, size):
                    for y in range(0, size):
                        if board[y][x]==dark:
                            dark_score+=1
                        elif board[y][x]==light:
                            light_score+=1
                #prints winner
                if dark_score<light_score:
                    winner=light
                    return jsonify(board=board, finished=f"{winner.strip()} has won")
                elif dark_score>light_score:
                    winner=dark
                    return jsonify(board=board, finished=f"{winner.strip()} has won")
                else:
                    winner="draw"
                    return jsonify(board=board, finished=f"It's a {winner}")
                
            else: #Else it lets the current player take another turn as the opponent has no valid moves
                return jsonify(status="success", board=board, player=turn)
                
        

        
    else:
        return jsonify(status="fail", message="Invalid coordinates") #just in case anything goes wrong but it can't really you just select the coordinates on the gui

@app.route('/save')
def save(): 
    global turn, move_counter, board
    game={"board": board, "turn": turn, "move counter": move_counter}
    try: #tries to save game to json file. Saves board, turn and move_counter
        with open("game_save.json", "w") as file:
            json.dump(game, file)
        return jsonify(status="success", message="Game saved")
    except:
        return jsonify(status="failed", message=f"Could not save game")
    
@app.route('/load')
def load():
    global turn, move_counter, board
    try: #tries to open json file and then read it and load board, turn and move_counter
        with open("game_save.json", "r") as file:
            game=json.load(file)
            board=game["board"]
            turn=game["turn"]
            move_counter=game["move counter"]
        return jsonify(status="success", board=board, player=turn, message="Game loaded")
    except:
        return jsonify(status="failed", message=f"Could not load game")




if __name__=="__main__": #didn't say to do this but I'm keeping it here
    app.run()





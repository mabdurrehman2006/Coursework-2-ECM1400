from flask import Flask, render_template, request, jsonify
import flask
from components import initialise_board, print_board, legal_move

app = Flask(__name__)

light="Light"
dark="Dark "
none="None "

#board=None
#turn=dark

def legal_move_check(board, player): #checks if there's any legal moves available
    size=len(board)
    for x in range(size):
        for y in range(size):
            if legal_move(player, (x, y), board):
                return True
    return False

@app.route('/')
def start():
    global board, turn, move_counter
    board=initialise_board()
    turn=dark
    move_counter=60 #might take a while for me to figure out this part
    return render_template('index.html', game_board=board)

@app.route('/move')
def move():
    global board, turn, move_counter
    x=request.args.get('x')
    y=request.args.get('y')
    try:
        x=int(x)
        y=int(y)
    except:
        return jsonify(status="fail", message="coordinates not integers")
    valid_move=legal_move(turn, (x, y), board)
    if valid_move==True:
        x_coordinate=x-1
        y_coordinate=y-1
        size=len(board)
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
                #prints winner
                if dark_score<light_score:
                    winner=light
                elif dark_score>light_score:
                    winner=dark
                else:
                    winner="draw"
                return jsonify(status="success", board=board, finished=winner)

        if turn==dark:
            next_turn=light
        else:
            next_turn=dark
        #Now checks if next player can make a move
        if legal_move_check(board, next_turn):
            turn=next_turn
            return jsonify(status="success", board=board, player=turn)
        else:
            if legal_move_check(board, turn)==False:
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
                elif dark_score>light_score:
                    winner=dark
                else:
                    winner="draw"
                return jsonify(status="success", board=board, finished=winner)
            else:
                message=f"{next_turn.strip()} has no moves available. It is {turn.strip()}'s turn"
                return jsonify(status="success", board=board, player=turn, message=message)
                
        

        
    else:
        return jsonify(status="fail", message="Invalid coordinates")

app.run()





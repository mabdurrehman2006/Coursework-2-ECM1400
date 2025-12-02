from flask import Flask, render_template, request, jsonify
import flask
from components import initialise_board, print_board, legal_move

app = Flask(__name__)

light="Light"
dark="Dark "
none="None "

#board=None
#turn=dark

@app.route('/')
def start():
    global board, turn
    board=initialise_board()
    turn=dark
    return render_template('index.html', game_board=board)

@app.route('/move')
def move():
    global board, turn
    x=request.args.get('x')
    y=request.args.get('y')
    try:
        x=int(x)
        y=int(y)
    except:
        return jsonify(status="fail", message="coordinates not integers")
    valid_move=legal_move(turn, (x, y), board)
    if valid_move==True:
        return jsonify(status="success")
    else:
        return jsonify(status="fail", message="Invalid coordinates")

app.run()

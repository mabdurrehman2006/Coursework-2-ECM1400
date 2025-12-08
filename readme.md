# Project Details
Author: Muhammad Abdur Rehman

Student ID: 750062970

Continuous Assessment 2

For the ECM1400 programming module at the University of Exeter

Date: December 2025

Repository: https://github.com/mabdurrehman2006/Coursework-2-ECM1400

# Flow diagram
### AI algorithm flowchart
![alt text](<Stage 3 AI algorithm.png>)
# How does the code function?
It's split into 3 files. The components.py file where it has core game logic such as initialising the board and validating a move. The flask web server and game engine in the flask_game_engine.py file. It uses the components.py file to initialise the board and validate moves. It also has an AI programmed like the specification asked. And then there's the index.html file which makes the user interface.

## components.py
### initialise_board(size=8)
Creates an 8x8 grid or the size that is defined by the user when calling it
Generates a 2d list filled with 'None ' and then places the four starting pieces('Light' and 'Dark ') in the center of the board with each colour diagonally opposite to their other piece. 
Returns the 2d list of the board

### legal_move(colour, coordinates, board_object)
Figures out if a selected move is valid according to othello rules
Checks if coordinates are between 0 and 7 and then if the target coordinate is empty
Then searches every direction to make sure pieces can be flipped according to the rules
Returns True if at least one direction where a piece can be flipped according to the rules is found, otherwise returns False

### print_board(board)
Displays the board in the console
Loops through the 2d list and prints rows separated by "|" and also includes column and row numbers. 

## flask_game_engine.py
Manages game, has code for AI opponent and uses flask to create server and communicates with html template. Uses 3 global variables(board, turn, move_counter)
### start()
Initialises the board by calling the initialise_board() function and then uses the html template
### move()
The actual game logic and where it handles everything from game end scenarios to executing moves

Validates selected coordinate. If its valid it flips them. 

Checks for game over scenario such as both players not having legal moves or move counter going to 0 or board being full.

Automatically passes turn to AI after checking if AI(light) has legal move available. Calls opponent_ai() to calculate best move and executes it using flip_pieces()

Handles passing turns when one player doesn't have legal moves available but the other one does. 

Returns json object containing updated board, current player and any game over messages. More in the manual.doc as it explains how the api works
### legal_move_check(board_object, player)
Figures out if current player has legal moves available
Iterates through every coordinate and calls legal_move(). If a valid move is found, returns True otherwise returns False
### flip_pieces(player, board_object, x_coordinate, y_coordinate)
Executes a move by flipping pieces on the board. Searches all directions for places where pieces can be outflanked and then flips all pieces that can be outflanked using the selected user coordinate

Returns total pieces flipped. Used by the AI to figure out what the best move is
### opponent_ai(player, board_object)
AI algorithm that just picks the move that flips the most pieces. Iterates through every coordinate and if its a legal move, creates a copy of the board and uses flip_pieces() to calculate how many pieces are flipped. Selects move with highest pieces flipped.
### save()
Writes board, turn, move_counter into a json file called game_save.json
### load()
Loads board, turn, move_counter from a json file called game_save.json

Updates global variables


### More details of how the API works and more details about the function are in the manual.doc file


## index.html
This file has the code for the graphical user interface
Uses html and css

Sends requests to the flask server when a user clicks something and then fetches the response

Updates the board to show the result of moves

## Reasoning for decisions made
Code isn't the cleanest. I definitely could've done better. I tried to clean it up as much as I can and reduce repetitive code

The AI just selects the move with the most pieces flipped because it seemed like the easiest one to program and was also the first idea that came to me. 



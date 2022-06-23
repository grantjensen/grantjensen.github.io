import chess
import chess.svg
import random
from js import console, document
from pyodide import create_proxy



def draw(board, powerupSquares = None):
    if powerupSquares is None:
        b_svg = chess.svg.board(
            board=board,
            size=600,
            flipped = not board.turn)
    else:
        squareSet = chess.SquareSet()
        for sq in powerupSquares:
            squareSet.add(sq)
        b_svg = chess.svg.board(
            board=board,
            size=600,
            squares = squareSet,
            flipped = not board.turn)
    pyscript.write('svg', b_svg)


def submit_move(move): 
    global board   
    global powerupSquares
    try:
        move = board.parse_san(move)
    except:
        pyscript.write('output', "Illegal move")
    board.push(move)
    draw(board)
    if move.to_square in powerupSquares:
        powerup = Powerup(board)
        powerup.randPowerup(move.to_square)
        board = powerup.board
    draw(board, powerupSquares)
    if board.is_game_over():
        pyscript.write('output', 'Game over')

def reset(*args, **kwargs):
    global board
    global powerupSquares
    board, powerupSquares = createGame(5)
    draw(board, powerupSquares)


def createGame(numPowerups):
    board = chess.Board()
    powerupSquares = random.sample(range(64), numPowerups)
    names = []
    for sq in powerupSquares:
        names += [chess.square_name(sq)]
    return board, powerupSquares

def convert_to_int(board):
    indices = '♚♛♜♝♞♟·♙♘♗♖♕♔'
    piece_map = board.piece_map()
    ret = [0] * 64
    for key in piece_map.keys():
        ret[key] = indices.index(piece_map[key].unicode_symbol()) - 6
    return ret


class Powerup:
    def __init__(self, board):
        self.board = board

    def randPowerup(self, square):
        numPowerups = 4
        powerup = random.randint(0,numPowerups - 1)
        if powerup == 0:
            pyscript.write('output', 'White swap!')
            self.swap(True)
        elif powerup == 1:
            pyscript.write('output', "Black swap!")
            self.swap(False)
        elif powerup == 2:
            pyscript.write('output',"Go again!")
            self.repeat()
        else:
            pyscript.write('output', "Replace!")
            self.replace(square)

    def repeat(self):
        self.board.turn = not self.board.turn


    def swap(self, color):
        # color is boolean, True swap two of white's pieces
        # False swap blacks
        if type(color) is not bool:
            console.log("Color arg must be bool")
        boardInt = convert_to_int(self.board)
        possibleSquares = []
        if color:  # White's turn
            for i in range(len(boardInt)):
                if boardInt[i] > 0:
                    possibleSquares += [i]
        else:
            for i in range(len(boardInt)):
                if boardInt[i] < 0:
                    possibleSquares += [i]
        pair = random.sample(possibleSquares, 2)
        pieceMap = self.board.piece_map()
        pieceMap[pair[0]], pieceMap[pair[1]] = pieceMap[pair[1]], pieceMap[pair[0]]
        self.board.set_piece_map(pieceMap)
        return
            
    

    def replace(self, square):
        piece_map = self.board.piece_map()
        if square not in piece_map.keys():
            console.log("Required swap does not have piece on square")
            return
        currType = piece_map[square].piece_type
        if abs(currType) == 6:  # king requested to stop
            pyscript.write('output', 'Swap! (King cannot swap)')
            return
        possibleOutcome = list(range(1, 6))
        if currType < 0: 
            possibleOutcome *= -1
        possibleOutcome.remove(currType)
        random.shuffle(possibleOutcome)
        piece_map[square].piece_type = possibleOutcome[0]
        board.set_piece_map(piece_map) 
        return


board, powerupSquares = createGame(5)
draw(board, powerupSquares)

 
def _move_press(e):
    if e.key == "Enter":
        move = e.target.value
        document.getElementById("input").value = ""
        pyscript.write("output", "")
        submit_move(move)

move_press = create_proxy(_move_press)
document.getElementById("input").addEventListener("keypress", move_press)


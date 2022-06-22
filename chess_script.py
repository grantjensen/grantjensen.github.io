import chess
import chess.svg
import random
from js import console



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


def submit_move(*args, **kwargs): 
    global board   
    global powerupSquares
    move = Element('input').element.value
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
        swapPairs = []
        for i in range(len(possibleSquares)):
            for j in range(len(possibleSquares)):
                if i < j and boardInt[possibleSquares[i]] != boardInt[possibleSquares[j]]:
                    swapPairs += [[possibleSquares[i], possibleSquares[j]]]
        random.shuffle(swapPairs)
        for i in range(len(swapPairs)):
            board2 = self.board.copy()
            pieceMap = self.board.piece_map()
            pieceMap[swapPairs[i][0]] , pieceMap[swapPairs[i][1]] = pieceMap[swapPairs[i][1]] , pieceMap[swapPairs[i][0]]
            board2.set_piece_map(pieceMap)
            if board2.is_valid():
                self.board = board2
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
        for i in range(4):
            board2 = self.board.copy()
            piece_map[square].piece_type = possibleOutcome[i]
            board2.set_piece_map(piece_map)
            if board2.is_valid():
                self.board = board2
                return
        piece_map = self.board.piece_map()


board, powerupSquares = createGame(5)
draw(board, powerupSquares)


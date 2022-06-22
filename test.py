import chess
import chess.svg
board = chess.Board()
board.push_san("e4")
boardsvg = chess.svg.board(board)
with open('board.svg', 'w') as f:
  f.write(boardsvg)

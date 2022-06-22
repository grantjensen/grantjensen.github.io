import chess
import chess.svg
board = chess.Board()
boardsvg = chess.svg.board(board)
with open('board.svg', 'w') as f:
  f.write(boardsvg)

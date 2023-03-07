"""
Handling the AI moves.
"""
import random
import ChessMain
import math
from pprint import pprint
import pygame
global positionsEvaluated 


piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}




knightSquares = [[0 for file in range(8)] for rank in range(8)]
for rank in range(len(knightSquares)):
    for file in range(len(knightSquares[rank])):
        knightSquares[rank][file] = knightSquares[rank][file] = round(0.07 * (7 - abs(file-3.5) - abs(rank-3.5)), 2)


#pprint(knightSquares)
BishopSquares = [[0 for file in range(8)] for rank in range(8)]
for rank in range(len(BishopSquares)):
    for file in range(len(BishopSquares[rank])):
        BishopSquares[rank][file] = round(0.05 * (7 - abs(file + rank - 7)), 2)
        if file % 5 == 1:
          if rank % 5 == 1:
            BishopSquares[rank][file] = 0.4


#pprint(BishopSquares)



RookSquares = [[0 for file in range(8)] for rank in range(8)]
for rank in range(len(RookSquares)):
    for file in range(len(RookSquares[rank])):
        RookSquares[rank][file] =  round(0.1 * (3.5 - abs(file - 3.5)), 2)
        if rank == 1:
            RookSquares[rank][file] = 1






QueenSquares = [[0 for file in range(8)] for rank in range(8)]
for rank in range(len(QueenSquares)):
    for file in range(len(QueenSquares[rank])):
        QueenSquares[rank][file] = QueenSquares[rank][file] = round(0.03 * (7 - abs(file-3.5) - abs(rank-3.5)), 2)
#pprint(QueenSquares)

pawnSquares = [[0 for file in range(8)] for rank in range(8)]
for rank in range(len(pawnSquares)):
    for file in range(len(pawnSquares[rank])):
        pawnSquares[rank][file] =  round(0.2 * (6 - rank ), 2)
        if rank == 3 or rank == 4:
            if file == 3 or file == 4:
               pawnSquares[rank][file] = 1

#pprint(pawnSquares)



piecePositionScores = {"wN": knightSquares,
                         "bN": knightSquares[::-1],
                         "wB": BishopSquares,
                         "bB": BishopSquares[::-1],
                         "wQ": QueenSquares,
                         "bQ": QueenSquares[::-1],
                         "wR": RookSquares,
                         "bR": RookSquares[::-1],
                         "wp": pawnSquares,
                         "bp": pawnSquares[::-1]}

CHECKMATE = 10000
STALEMATE = 0
DEPTH = 3

def findBestMove(game_state, valid_moves, return_queue):

    
    print("depth: " + str(ChessMain.getAiDepth()))
    global positionsEvaluated
    positionsEvaluated = 0
    global next_move
    next_move = None
    random.shuffle(valid_moves)
    findMoveNegaMaxAlphaBeta(game_state, valid_moves, DEPTH, -CHECKMATE, CHECKMATE,
                             1 if game_state.white_to_move else -1)
    return_queue.put(next_move)
    print("evaluated " + str(positionsEvaluated) + " positions")
    print("depth: " + str(DEPTH))


def findMoveNegaMaxAlphaBeta(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
    global next_move
    global positionsEvaluated
    stalemate = False
    
    if depth == 0:
        positionsEvaluated += 1
       
        return turn_multiplier * scoreBoard(game_state)
        
   
    max_score = -CHECKMATE
    for move in valid_moves:
        game_state.makeMove(move)
        next_moves = game_state.getValidMoves()
        if depth == 1:
            positionsEvaluated += 1
        score = -findMoveNegaMaxAlphaBeta(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        game_state.undoMove()
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break
      
    return max_score


def scoreBoard(game_state):
    """
    Score the board. A positive score is good for white, a negative score is good for black.
    """
    global stalemate 
    
    
   
    if game_state.checkmate:
        if game_state.white_to_move:
            return -CHECKMATE  # black wins
        else:
            return CHECKMATE  # white wins
    elif game_state.stalemate:
        return STALEMATE
    score = 0
    for rank in range(len(game_state.board)):
        for col in range(len(game_state.board[rank])):
            piece = game_state.board[rank][col]
            if piece != "--":
                piece_position_score = 0
                if piece[1] != "K":
                    piece_position_score = piecePositionScores[piece][rank][col]
                if piece[0] == "w":
                    score += piece_score[piece[1]] + piece_position_score
                if piece[0] == "b":
                    score -= piece_score[piece[1]] + piece_position_score

    return score

def countMaterial(game_state):
    score = 0
    for rank in range(len(game_state.board)):
        for col in range(len(game_state.board[rank])):
            piece = game_state.board[rank][col]
            if piece != "--":
                piece_position_score = 0
                if piece[0] == "w":
                    score += piece_score[piece[1]] + piece_position_score
                if piece[0] == "b":
                    score -= piece_score[piece[1]] + piece_position_score
    return score
def findRandomMove(valid_moves):
   
    return random.choice(valid_moves)



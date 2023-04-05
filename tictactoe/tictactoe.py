"""
Tic Tac Toe Player
"""

import math
import copy 

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """

    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    xo_count = 0
    for i in board:
        for j in i:
            if(j != EMPTY):
                xo_count+=1
    if(xo_count%2==0):
        return X
    return O


def actions(board):
    spots = []
    for i in range(3):
        for j in range(3):
            if(board[i][j] == EMPTY):
                spots.append([i, j])
    return spots


def result(board, action):
    turn = player(board)
    copyBoard = copy.deepcopy(board)
    if(board[action[0]][action[1]] is EMPTY):
        copyBoard[action[0]][action[1]] = turn
        return copyBoard
    raise ValueError


def winner(board):
    for i in range(3):
        if(board[i][0]==board[i][1]==board[i][2]):
            return board[i][0]
        
    for i in range(3):
        if(board[0][i]==board[1][i]==board[2][i]):
            return board[0][i]
        
    if (board[0][0] == board[1][1] == board[2][2]):
        return board[0][0]
    
    if (board[0][2] == board[1][1] == board[2][0]):
        return board[0][2]
    
    return None


def terminal(board):
    if(winner(board) != None):
        return True
    elif(actions(board) == []):
        return True
    return False


def utility(board):
    if(winner(board) == X):
        return 1
    if(winner(board) == O):
        return -1
    return 0


alpha = -2
beta = 2

def minimax(board):
    nextMove = []
    global alpha
    global beta
    
    if terminal(board):
        return [utility(board), actions(board)]

    if player(board) == X:
        v = -2
        for i in actions(board):
            eval = minimax(result(board, i))[0]
            if eval>v:
                v = eval
                alpha = eval
                nextMove = i
            
            if v > beta:
                break
    
    if player(board) == O:
        v = 2
        for i in actions(board):
            eval = minimax(result(board, i))[0]
            if eval<v:
                v = eval
                beta = eval
                nextMove = i

            if v < alpha:
                break

    return [v, nextMove]
    


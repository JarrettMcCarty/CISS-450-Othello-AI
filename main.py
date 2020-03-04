#-------------------------#
# File  : main.py         #
# Author: Jarrett McCarty #
#-------------------------#

#-------------------------------------------------#
# Description: MiniMax/Alpha-Beta/Negamax Othello #
#-------------------------------------------------#

import copy

# List of potential directions to check
DIRS = [[-1, -1], [1, 1], [0, -1], [0, 1], [-1, 1], [1, -1], [-1, 0], [1, 0]]


MAX = 1000000
MIN = -1000000


def within_bounds(x, y, board_size):
    ''' Returns bool if the (x, y) coordinates passed in are within
        the game board. '''
    
    return x >= 0 and x < board_size and y >= 0 and y < board_size

def count(game_board, player_piece, board_size):
    ''' Gets total pieces on the board '''
    
    opposing_piece = None

    mine = 0
    yours = 0
    
    if player_piece == 'W':
        opposing_piece = 'B'
    else:
        opposing_piece = 'W'

    for i in range(board_size):
        for j in range(board_size):
            if game_board[i][j] == player_piece:
                mine += 1
            if game_board[i][j] == opposing_piece:
                yours += 1
    return (mine, yours)
    
def eval_move(game_board, player_piece, board_size):
    ''' Gives a score to a move '''
    opposing_piece = None
    if player_piece == 'W':
        opposing_piece = 'B'
    else:
        opposing_piece = 'W'
    P = 0
    if board_size == 8:
        for row in range(8):
            for col in range(8):
                if game_board[row][col] == player_piece:
                    P += B8[(row+1)*10+1+col]
                elif game_board[row][col] == opposing_piece:
                    P -= B8[(row+1)*10+1+col]
    elif board_size == 6:
        for row in range(6):
            for col in range(6):
                if game_board[row][col] == player_piece:
                    P += B8[(row+1)*10+1+col]
                elif game_board[row][col] == opposing_piece:
                    P -= B8[(row+1)*10+1+col]
    
    b = 0 # black pieces
    w = 0 # white pieces
    mob = 0 # mobility
        
    # Get values for parity calculation
    M, Y = count(game_board, player_piece, board_size)
        
    parity = 100 * (M - Y) / (M + Y)
 
    for i in range(board_size):
        for j in range(board_size):
            if check_move(game_board, i, j, 'W', board_size):
                w += 1
            if check_move(game_board, i, j, 'B', board_size):
                b += 1
    if b + w > 0:
        mob = 100 * (b - w) / (b + w)
    else:
        mob = 0
    return (parity + P + mob) 

def dead_end(game_board, player_piece, board_size):
    ''' bool for if a move exists '''
    
    for j in range(board_size):
        for i in range(board_size):
            if check_move(game_board, i, j, player_piece, board_size):
                return False
    return True


def move(game_board, x, y, player_piece, board_size):
    ''' Commit move to board '''
    
    game_board[y][x] = player_piece

    swaps = 0

    for D in DIRS:
        c = 0
        for i in range(board_size):
            xd = x + D[0] * (i + 1)
            yd = y + D[1] * (i + 1)
            if not within_bounds(xd, yd, board_size) or game_board[yd][xd] == ' ':
                c = 0
                break
            elif game_board[yd][xd] == player_piece:
                break
            else: c += 1

        for i in range(c):
            xd = x + D[0] * (i + 1)
            yd = y + D[1] * (i + 1)
            game_board[yd][xd] = player_piece
        swaps += c

    return (swaps, game_board)
            
def check_move(game_board, x, y, player_piece, board_size):
    ''' Validity of move '''
    
    if not within_bounds(x, y, board_size) or game_board[y][x] != ' ':
        return False

    swaps = 0
    
    for D in DIRS:
        c = 0
        for i in range(board_size):
            xd = x + D[0] * (i + 1)
            yd = y + D[1] * (i + 1)
            if not within_bounds(xd, yd, board_size) or game_board[yd][xd] == ' ':
                c = 0
                break
            elif game_board[yd][xd] == player_piece:
                break
            else: c += 1

        swaps += c

    if swaps > 0:
        return True
    else:
        return False

def minimax(game_board, board_size, player_piece, d, maxplayer):
    '''  MiniMax algorithim implementation
         TODO-> add max and min functions '''
    
    if dead_end(game_board, player_piece, board_size) or d == 0:
        return eval_move(game_board, player_piece, board_size)
    if maxplayer:
        B = MIN
        for j in range(board_size):
            for i in range(board_size):
                if check_move(game_board, i, j, player_piece, board_size):
                    c, temp = move(copy.deepcopy(game_board), i, j, player_piece, board_size)
                    V = minimax(temp, board_size, player_piece, d - 1, False)
                    B = max(B, V)
                                      
    else:
        B = MAX
        for j in range(board_size):
            for i in range(board_size):
                if check_move(game_board, i, j, player_piece, board_size):
                    c, temp = move(copy.deepcopy(game_board), i, j, player_piece, board_size)
                    V = minimax(temp, board_size, player_piece, d - 1, True)
                    B = min(B, V)
    return B
    

    

def alpha_beta(game_board, board_size, player_piece, d, alpha, beta, maxplayer):
    ''' AlphaBeta search algorithim implementation by sorting eval function
        values. Commented out is the normal alpha beta.
        TODO-> add max and min functions '''

    def getkey(item):
        return item[0]
    
    if dead_end(game_board, player_piece, board_size) or d == 0:
        return eval_move(game_board, player_piece, board_size)
    pri = []
    for j in range(board_size):
        for i in range(board_size):
            if check_move(game_board, i, j, player_piece, board_size):
                c, temp = move(copy.deepcopy(game_board), i, j, player_piece, board_size)
                pri.append((eval_move(game_board, player_piece, board_size), temp))
    pri = sorted(pri, key=lambda item:getkey(item), reverse = True)
    pri = [x[1] for x in pri]
    
    if maxplayer:
        V = MIN
        #for j in range(board_size):
        #for i in range(board_size):
        #if check_move(game_board, i, j, player_piece, board_size):
        #c, temp = move(copy.deepcopy(game_board), i, j, player_piece, board_size)
        # change state to temp in max(V, alpha_beta(...)) if using regular alpha beta
        for state in pri:
            V = max(V, alpha_beta(state, board_size, player_piece, d - 1, alpha, beta, False))
            alpha = max(alpha, V)
            if beta <= alpha:
                break
        return V
    else:
        V = MAX
        #for j in range(board_size):
        #for i in range(board_size):
        #if check_move(game_board, i, j, player_piece, board_size):
        #c, temp = move(copy.deepcopy(game_board), i, j, player_piece, board_size)
        # change state to temp in max(V, alpha_beta(...)) if using regular alpha beta
        for state in pri:
            V = min(V, alpha_beta(state, board_size, player_piece, d - 1, alpha, beta, True))
            beta = min(beta, V)
            if beta <= alpha:
                break
        return V
    
def negamax():
    ''' TODO Negamax algorithim implementation '''
    pass

def alpha_beta_negamax():
    ''' TODO Alpha beta negamax algorithim implementation '''
    pass

def good_move(game_board, player_piece, d, board_size):
    ''' This functon will return a good move given by one of the
        implemented algorithims '''
    
    M = -10000
    X, Y = [None, None]
    for j in range(board_size):
        for i in range(board_size):
            if check_move(game_board, i, j, player_piece, board_size):
                c, temp = move(copy.deepcopy(game_board), i, j, player_piece, board_size)
                #P = minimax(game_board, board_size, player_piece, d, True)
                P = alpha_beta(game_board, board_size, player_piece, d, MIN, MAX, True)
                if P > M:
                    M = P
                    X = i
                    Y = j
    return [Y, X]# Y X

def get_move(board_size, board_state, turn, time_left, opponent_time_left):
    ''' Get move function returns the [x, y] used to make a move againts
        another Othello ai '''

    if time_left >= 150000:
        XY = good_move(board_state, turn, 7, board_size)#5
    elif time_left < 150000 and time_left > 75000:
        XY = good_move(board_state, turn, 4, board_size)#3
    else:
        XY = good_move(board_state, turn, 2, board_size)
    if XY == [None, None]:
        return None
    return XY




if __name__ == '__main__':
    pass


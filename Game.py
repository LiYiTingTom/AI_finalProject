import multiprocessing as mp
import threading as td
import time
from random import shuffle

from Board import Board

# --------- GLOBAL VARS ---------
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
WIN_LINE = 4
SCR_LIST = {
    2:9,
    3:999,
    4:999999
}

def humanPlay(board, player):
    """ human player movement

        @Retrun Win=<bool>
    """
    while True:
        pos = input(f"\nplayer {player} input: ")

        # Check input validability
        try:
            pos = int(pos)
            if pos in board.getValCols():
                if board.isValMov(pos):
                    break

        except ValueError:
            pass
        print("Invalid Value")

    # do movement
    board.doMov(pos, player)

    # dradBoard
    board.drawBoard()

    # check win
    if board.gameOver([player], WIN_LINE):
        print(f"Human Player {player} Won !")
        board.printBoard()
        board.winner = 'human'
        return False

    # check draw
    if board.draw():
        board.winner = 'Draw'
        print("Draw")
        return False

    # next player
    return True



def aiPlay(board, player, depth=5):
    """ ai player movement

        @Retrun Win=<bool>
    """
    # do alpha-beta purnning
    pos = minmaxAB(board, depth, player)
    board.doMov(pos, player)

    # dradBoard
    board.drawBoard()

    # check win
    if board.gameOver([player], WIN_LINE):
        print(f"AI Player {player} Won !")
        board.printBoard()
        board.winner = 'ai'
        return False

    # check draw
    if board.draw():
        board.winner = 'Draw'
        print("Draw")
        return False

    # next player
    return True



def minmaxAB(board, depth, player):
    """ do minmax alpha-beta

        @Return best_mov=<int>
    """
    #-- multicore --- START
    pool = mp.Pool(processes=4)
    #-- multicore --- END

    # get valid moves
    validMovs = board.getValCols()
    shuffle(validMovs)
    if sum(board.board[board.height-1]) < 2:
        bestMov = int(board.width/2)
        validMovs[0], validMovs[bestMov] = validMovs[bestMov], validMovs[0]

    bestScr = float("-inf")

    # init alpha and beta
    alpha = float("-inf")
    beta = float("inf")

    oppo = 2 if player == 1 else 1

    board_list = []

    # Finding
    for mov in validMovs:

        # copy current board to temp board
        tmpBoard = board.copyBoard()
        # do the move
        tmpBoard.doMov(mov, player)

#        multi_res = pool.map(minBeta, (tmpBoard, depth-1, alpha, beta, player, oppo))


        board_list.append((tmpBoard, depth-1, alpha, beta, player, oppo, mov))
    multi_res = pool.map(minBeta, board_list)

    print(multi_res)
    time.sleep(1)

    return bestMov



#def minBeta(board, depth, a, b, player, oppo):
def minBeta(*args):
    """ min beta

        @Return beta=<int>
    """
    board, depth, a, b, player, oppo, mov = args[0]

    validMovs = []
    validMovs = board.getValCols()

    # check Game Over
    if depth == 0 \
    or len(validMovs) == 0 \
    or board.gameOver((1, 2), WIN_LINE):
        print(board.utiVal(player, WIN_LINE, SCR_LIST)*depth)
        return board.utiVal(player, WIN_LINE, SCR_LIST)*depth

    beta = b

    # if end of tree evaluate scr
    for mov in validMovs:
        boardScr = float("inf")

        # else keep down tree, until a, b met
        if a < beta:
            # copy current board to temp board
            tmpBoard = board.copyBoard()

            # do move
            tmpBoard.doMov(mov, oppo)

            # call maxAlpha on tmp board
            boardScr = maxAlpha(tmpBoard, depth-1, a, beta, player, oppo, mov)

        if boardScr < beta:
            beta = boardScr

    return beta



def maxAlpha(board, depth, a, b, player, oppo, mov):
    """ max alpha

        @Return alpha=<int>
    """
    validMovs = []
    validMovs = board.getValCols()

    # check Game Over
    if depth == 0 \
    or len(validMovs) == 0 \
    or board.gameOver((1, 2), WIN_LINE):
        return board.utiVal(player, WIN_LINE, SCR_LIST)*depth

    alpha = a
    # if end of tree, evalute scr
    for mov in validMovs:
        boardScr = float("-inf")

        if alpha < b:
            tmpBoard = board.copyBoard()
            tmpBoard.doMov(mov, player)
            boardScr = minBeta((tmpBoard, depth-1, alpha, b, player, oppo, mov))


        if boardScr > alpha:
            alpha = boardScr

    return alpha

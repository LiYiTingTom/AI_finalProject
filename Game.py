import sys
sys.modules['__main__'].__file__='ipython'
import os
import multiprocessing as mp
from random import shuffle

from Board import Board

CORE_NUM = 4
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
                if board.isValMov(pos): break

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

    if player == 1: oppo = 2
    else: oppo = 1

#    pool = mp.Pool()
    job_args_list = []
    boardScr_tup_list = []

    # Finding
    for mov in validMovs:

        # copy current board to temp board
        tmpBoard = board.copyBoard()
        # do the move
        tmpBoard.doMov(mov, player)

        job_args_list.append([tmpBoard, depth-1, alpha, beta, player, oppo, mov])

#    for args in job_args_list:
#        # call min on tmp board
#        boardScr_tup_list.append(minBeta(args))
#    boardScr_tup_list.sort(key=lambda tup: tup[0])
#
#    print(boardScr_tup_list)
#    bestMov = boardScr_tup_list[0][1]

    boardScr_tup_list_p = pool.map(minBeta, job_args_list)

    boardScr_tup_list_p.sort(key=lambda tup: tup[0])

    print(boardScr_tup_list_p)
    bestMov = boardScr_tup_list_p[-1][1]

#    global test_times
#    test_times += 1
#    if test_times > 50:
#        os.sys.exit()

    return bestMov



#def minBeta(board, depth, a, b, player, oppo):
def minBeta(*args):
    """ min beta

        @Return beta=<int>
    """
    board, depth, a, b, player, oppo, mov_o = args[0]
    validMovs = []
    validMovs = board.getValCols()

    # check Game Over
    if depth == 0 \
    or len(validMovs) == 0 \
    or board.gameOver((1, 2), WIN_LINE):
        return board.utiVal(player, WIN_LINE, SCR_LIST)*depth, mov_o

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
            boardScr = maxAlpha([tmpBoard, depth-1, a, beta, player, oppo, mov_o])[0]

        if boardScr < beta:
            beta = boardScr

    return beta, mov_o

#def maxAlpha(board, depth, a, b, player, oppo):
def maxAlpha(*args):
    """ max alpha

        @Return alpha=<int>
    """
    board, depth, a, b, player, oppo, mov_o = args[0]
    validMovs = []
    validMovs = board.getValCols()

    # check Game Over
    if depth == 0 \
    or len(validMovs) == 0 \
    or board.gameOver((1, 2), WIN_LINE):
        return board.utiVal(player, WIN_LINE, SCR_LIST)*depth, mov_o

    alpha = a

    # if end of tree, evalute scr
    for mov in validMovs:
        boardScr = float("-inf")

        if alpha < b:
            tmpBoard = board.copyBoard()
            tmpBoard.doMov(mov, player)
            boardScr = minBeta([tmpBoard, depth-1, alpha, b, player, oppo, mov_o])[0]


        if boardScr > alpha:
            alpha = boardScr

    return alpha, mov_o

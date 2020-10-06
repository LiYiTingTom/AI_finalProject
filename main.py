""" MAIN """
from Game import *

def checkInputIsNum(words, ran):
    """ Check Input is Number

        @Return number=<int>
    """
    while True:
        mod = input(words)
        try:
            mod = int(mod)
            if mod in range(ran):
                break
        except ValueError:
            pass
        print("Invalid Value")

    return mod


def main():
    """ MAIN """
    mod = checkInputIsNum("Game mode (0: human-human, 1: human-computer, 2: computer-computer): ", 3)

    # board init
    board = Board(BOARD_WIDTH, BOARD_HEIGHT)

    # h-h
    if mod == 0:
        rou = 0
        board.drawBoard()
        # Human - Human
        while humanPlay(board, 1) \
          and humanPlay(board, 2):
            rou += 1
            #print(f"round {round}")

    # Human - AI
    elif mod == 1:
        times = int(checkInputIsNum("Please select the difficality (0-5, or 6 is learning) : ", 7))

        if times != 6:
            times += 2
            player1_level = checkInputIsNum("Select your turn (1, 2) : ", 3)
            rou = 0

            if player1_level == 1:
                board.drawBoard()
                while humanPlay(board, 1) \
                  and aiPlay(board, 2, times):
                    rou += 1
                    print(f"round {rou}")
            else:
                while aiPlay(board, 1, times) \
                  and humanPlay(board, 2):
                    rou += 1
                    print(f"round {rou}")
        else:
            times = 4
            while board.winner == 'human':
                rou = 0
                board = Board(BOARD_WIDTH, BOARD_HEIGHT)
                player1_level = checkInputIsNum("Select your turn (1, 2) : ", 3)
                if player1_level == 1:
                    board.drawBoard()
                    while humanPlay(board, 1) \
                      and aiPlay(board, 2, times):
                        rou += 1
                        print(f"round {rou}")
                else:
                    while aiPlay(board, 1, times) \
                      and humanPlay(board, 2):
                        rou += 1
                        print(f"round {rou}")
                if board.winner == 'human':
                    times += 1
                    print("Ai will be stronger ...")
    # c-c
    elif mod == 2:
        player1_level = checkInputIsNum("Please select the difficality (0-5) for AI1: ", 6) + 2
        player2_level = checkInputIsNum("Please select the difficality (0-5) for AI2: ", 6) + 2

        rou = 0
        while aiPlay(board, 1, player1_level) \
          and aiPlay(board, 2, player2_level):
            rou += 1
            print(f"round {rou}")



if __name__ == '__main__':
    main()

from Game import *

def checkInputIsNum(words, ran):
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
  mod = checkInputIsNum("Game mode (0: human-human, 1: human-computer, 2: computer-computer): ", 3)

  # board init
  board = Board(BOARD_WIDTH, BOARD_HEIGHT)
  
  # h-h
  if mod == 0:
    board.drawBoard()
    # Human - Human
    while humanPlay(board, 1) and humanPlay(board, 2):
      pass

  # Human - AI
  elif mod == 1:
    times = int(checkInputIsNum("Please select the difficality (0-5, or 6 is learning) : ", 7))

    if times != 6:
      times += 2
      p1L = checkInputIsNum("Select your turn (1, 2) : ", 3)

      if p1L == 1:
        board.drawBoard()
        while humanPlay(board, 1) and aiPlay(board, 2, times):
          pass
      else:
        while aiPlay(board, 1, times) and humanPlay(board, 2):
          pass
    else:
      times = 4
      while board.winner == 'human':
        board = Board(BOARD_WIDTH, BOARD_HEIGHT)
        p1L = checkInputIsNum("Select your turn (1, 2) : ", 3)
        if p1L == 1:
          board.drawBoard()
          while humanPlay(board, 1) and aiPlay(board, 2, times):
            pass
        else:
          while aiPlay(board, 1, times) and humanPlay(board, 2):
            pass
        if board.winner == 'human':
          times += 1
          print("Ai will be stronger ...")
  # c-c
  elif mod == 2:
    p1L = checkInputIsNum("Please select the difficality (0-5) for AI1: ", 6) + 2
    p2L = checkInputIsNum("Please select the difficality (0-5) for AI2: ", 6) + 2

    while aiPlay(board, 1, p1L) and aiPlay(board, 2, p2L):
      pass


if __name__ == '__main__':
  main()




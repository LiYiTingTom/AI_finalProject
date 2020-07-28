def printRed(arg): print("\033[91m {}\033[00m" .format(arg), end="")
def printYello(arg): print("\033[93m {}\033[00m" .format(arg), end="")
def printBlue(arg): print("\033[92m {}\033[00m" .format(arg), end="")

class Board():

  pass

  def __init__(self, width, height):
    self.board = [[0 for i in range(width)] for j in range(height)]
    self.width = width
    self.height = height
    self.winner = 'human'

  def getWidth(self): return self.width
  def getHeight(self): return self.height
  
  # check column is full or not
  def isNotFull(self, col):
    if self.board[0][col] == 0: return True
    return False

  # get top row
  def getTopRow(self, col):
    for row in range(self.height-1, -1, -1):
      if self.board[row][col] == 0:
        return row
    return False

  # check col and row validability
  def isVal(self, col, row):
    if col in range(self.width) and row in range(self.height):
      return True
    return False
  
  # get valid columns in board
  def getValCols(self):
    valCols = []
    for col in range(self.width):
      if self.isNotFull(col):
        valCols.append(col)
    return valCols
    
  # do player move
  def doMov(self, col, player):
    for row in range(self.height-1, -1, -1):
      if self.board[row][col] == 0:
        self.board[row][col] = player
        return row, col
    return False
  
  # ckeck move's validability
  def isValMov(self, col):
    for row in range(self.height):
      if self.board[row][col] == 0:
        return True
    return False

  # check winner
  def checkWin(self, player, line):

    def checkRow(col, row, player, line):
      # Check next 3 elements & Check index range
      for i in range(row, row+line-1):
        if self.board[col][i] != player or i == self.width-1:
          return False
      return True

    def checkCol(col, row, player, line):
      # Check next 3 element & Check index range
      for j in range(col , col+line-1):
        if self.board[j][row] != player or j == self.height-1:
          return False
      return True

    def checkDiaLR(col, row, player, line):
      # Check next 3 elementa & Check index range
      for i in range(0, line):
        if self.board[col+i][row+i] != player or \
           col+i == self.height-1 or row+i == self.width-1:
          return False
      return True
      
    def checkDiaRL(col, row, player, line):
      # Check next 3 element & Check index range
      for i in range(0, line):
        if self.board[col+i][row-i] != player or \
           col+i == self.height-1 or row-i == 0:
          return False
      return True

    # UL to UR
    for i in range(self.height):
      for j in range(self.width):
        if self.board[i][j] == player:
          if checkRow(i, j, player, line) or checkCol(i, j, player, line) or\
             checkDiaLR(i, j, player, line) or checkDiaRL(i, j, player, line):
            return True
    return False

  def printBoard(self):
    for i in self.board: print(i)

  def drawBoard(self):
    for i in range(self.width):
      print(" %d"%i, end=" ")
    print()
    for i in range(len(self.board)):
      for j in range(len(self.board[i])):
        if self.board[i][j] == 1: printYello("● ")
        elif self.board[i][j] == 2: printRed("● ")
        else: print(" ▢ ",end="")
      print()
    print()

  def copyBoard(self):
    newBoard = Board(self.width, self.height)
    for i in range(self.height):
      for j in range(self.width):
        newBoard.board[i][j] = self.board[i][j]
    return newBoard

  def countSeq(self, player, line):
    def verticalSeq(row, col):
        """Return 1 if it found a vertical sequence with the required line 
        """
        count = 0
        for rowIndex in range(row, self.height):
            if self.board[rowIndex][col] == self.board[row][col]:
                count += 1
            else:
                break
        if count >= line:
            return 1
        else:
            return 0

    def horizontalSeq(row, col):
        """Return 1 if it found a horizontal sequence with the required line 
        """
        count = 0
        for colIndex in range(col, self.width):
            if self.board[row][colIndex] == self.board[row][col]:
                count += 1
            else:
                break
        if count >= line:
            return 1
        else:
            return 0

    def negDiagonalSeq(row, col):
        """Return 1 if it found a negative diagonal sequence with the required line 
        """
        count = 0
        colIndex = col
        for rowIndex in range(row, -1, -1):
            if colIndex > self.height:
                break
            elif self.board[rowIndex][colIndex] == self.board[row][col]:
                count += 1
            else:
                break
            colIndex += 1 # increment column when row is incremented
        if count >= line:
            return 1
        else:
            return 0

    def posDiagonalSeq(row, col):
        """Return 1 if it found a positive diagonal sequence with the required line 
        """
        count = 0
        colIndex = col
        for rowIndex in range(row, self.height):
            if colIndex > self.height:
                break
            elif self.board[rowIndex][colIndex] == self.board[row][col]:
                count += 1
            else:
                break
            colIndex += 1 # increment column when row incremented
        if count >= line:
            return 1
        else:
            return 0

    totalCount = 0

    # for each piece in the self.board...
    for row in range(self.height):
        for col in range(self.height):

            # ...that is of the player we're looking for...
            if self.board[row][col] == player:

                # check if a vertical streak starts at (row, col)
                totalCount += verticalSeq(row, col)

                # check if a horizontal four-in-a-row starts at (row, col)
                totalCount += horizontalSeq(row, col)

                # check if a diagonal (both +ve and -ve slopes) four-in-a-row starts at (row, col)
                totalCount += (posDiagonalSeq(row, col) + negDiagonalSeq(row, col))
    # return the sum of sequences of line 'line'
    return totalCount


  def utiVal(self, player, WIN_LINE, scrList):
    playerScr = 0
    oppoScr = 0

    if player == 1: oppo = 2
    else: oppo = 1

    for i in range(2, WIN_LINE+1):
      playerScr += self.countSeq(player, i+1) * scrList[i]
      oppoScr += self.countSeq(oppo, i+1) * scrList[i]

    if self.countSeq(oppo, i+1) * scrList[i] > 0:
      return float('-inf')
    elif self.countSeq(player, i+1) * scrList[i] > 0:
      return float('inf')
    else:
      return playerScr - oppoScr

  def gameOver(self, players, WIN_LINE):
    totalScr = 0
    for player in players:
      totalScr += self.countSeq(player, WIN_LINE)
    if totalScr != 0: return True
    return False

  def draw(self):
    for row in range(self.height):
      for col in range(self.width):
        if self.board[row][col] == 0:
          return False
    return True


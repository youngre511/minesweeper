from random import randint

def gen_mines(height, width, difficulty):
  mines = []
  num_mines = 0
  if difficulty =="easy":
    num_mines = int(height*width*.12)
  if difficulty =="medium":
    num_mines = int(height*width*.15)
  if difficulty =="hard":
    num_mines = int(height*width*.20)  
  while len(mines) < num_mines:
    coord = (randint(0,width - 1), randint(0,height - 1))
    if coord not in mines:
      mines.append(coord)
  return mines


mines = gen_mines(12, 12, "medium")

class Square:
  def __init__(self, column, row, mine = False, revealed = False, flagged = False):
    self.col = column
    self.row = row
    self.coordinates = (self.col, self.row)
    self.mine = mine
    self.revealed = revealed
    self.adjacents = 0
    self.flagged = flagged
    self.adjacent_list = []

  def set_revealed(self):
    self.revealed = True
  
  def add_adjacent_by_coordinate(self, adj):
    self.adjacent_list.append(adj)
  
  def get_adjacents(self):
    return self.adjacent_list

class Board:
  def __init__(self, height, width):
    self.height = height
    self.width = width
    self.board_dict = {}
  
  def add_square(self, column, row, mine = False):
    square = Square(column, row, mine)
    self.board_dict[square.coordinates] = square
  
  def get_square(self, coord):
    return self.board_dict[coord]
  
  def toggle_flag(self, coord):
    if self.board_dict[coord].flagged is False:
      self.board_dict[coord].flagged = True
    else:
      self.board_dict[coord].flagged = False

  def add_adjacents(self):
    square_coord = list(self.board_dict.keys())
    for square in square_coord:
      if square[0] > 0:
        self.board_dict[square].add_adjacent_by_coordinate((square[0]-1, square[1]))
        if self.board_dict[(square[0]-1, square[1])].mine == True and self.board_dict[square].mine == False:
          self.board_dict[square].adjacents += 1
      if square[0] < self.width - 1:
        self.board_dict[square].add_adjacent_by_coordinate((square[0]+1, square[1]))
        if self.board_dict[(square[0]+1, square[1])].mine == True and self.board_dict[square].mine == False:
          self.board_dict[square].adjacents += 1
      if square[1] > 0:
        self.board_dict[square].add_adjacent_by_coordinate((square[0], square[1]-1))
        if self.board_dict[(square[0], square[1]-1)].mine == True and self.board_dict[square].mine == False:
          self.board_dict[square].adjacents += 1
      if square[1] < self.height - 1:
        self.board_dict[square].add_adjacent_by_coordinate((square[0], square[1]+1))
        if self.board_dict[(square[0], square[1]+1)].mine == True and self.board_dict[square].mine == False:
          self.board_dict[square].adjacents += 1
      if square[0] > 0 and square[1] > 0:
        self.board_dict[square].add_adjacent_by_coordinate((square[0]-1, square[1]-1))
        if self.board_dict[(square[0]-1, square[1]-1)].mine == True and self.board_dict[square].mine == False:
          self.board_dict[square].adjacents += 1
      if square[0] > 0 and square[1] < self.height - 1:
        self.board_dict[square].add_adjacent_by_coordinate((square[0]-1, square[1]+1))
        if self.board_dict[(square[0]-1, square[1]+1)].mine == True and self.board_dict[square].mine == False:
          self.board_dict[square].adjacents += 1
      if square[0] < self.width - 1 and square[1] > 0:
        self.board_dict[square].add_adjacent_by_coordinate((square[0]+1, square[1]-1))
        if self.board_dict[(square[0]+1, square[1]-1)].mine == True and self.board_dict[square].mine == False:
          self.board_dict[square].adjacents += 1
      if square[0] < self.width - 1 and square[1] < self.height - 1:
        self.board_dict[square].add_adjacent_by_coordinate((square[0]+1, square[1]+1))
        if self.board_dict[(square[0]+1, square[1]+1)].mine == True and self.board_dict[square].mine == False:
          self.board_dict[square].adjacents += 1




def create_board(size, difficulty):
  height = 0
  width = 0
  if size == 'small':
    height = 10
    width = 10
  if size == 'medium':
    height = 20
    width = 20
  if size == 'large':
    height = 30
    width = 30
  board = Board(height, width)
  mines = gen_mines(height, width, difficulty)
  for row in range(0,height):
    for col in range(0,width):
      if (col, row) in mines:
        board.add_square(col, row, True)
      else:
        board.add_square(col, row)
  board.add_adjacents()
  return board


def print_board(board):
  columns = 0
  for col, row in board.board_dict.keys():
    if row == 1:
      break
    else:
      columns += 1
  rows = int(len(board.board_dict)/columns)
  upper_key = ""
  for x in range(0,columns):
    if len(str(x+1)) == 1:
      upper_key += " " + str(x + 1) + " "
    else:
      upper_key += " " + str(x + 1) + ""
  print("    " + upper_key)
  border = ""
  for i in range(0, columns):
    border += "\u2500\u2500\u2500"
  print("   \u250C\u2500" + border + "\u2510")
  for y in range(0,rows):
    row_dis = "\u2502"
    for x in range(0,columns):
      if board.get_square((x, y)).flagged is True:
        row_dis += " \u25B6 "
      elif board.get_square((x, y)).revealed is False:
        row_dis += " \u2586\u2586"
      elif board.get_square((x, y)).mine is True:
        row_dis += " \u26EF "
      elif board.get_square((x, y)).adjacents > 0:
        row_dis += " " + str(board.get_square((x, y)).adjacents) + " "
      else:
        row_dis += "   "
    if len(str(y+1)) == 1:
      print(" " + str(y+1) + " " + row_dis + " \u2502")
    if len(str(y+1)) == 2:
      print(str(y+1) + " " + row_dis + " \u2502")
  print("   \u2514" + border + "\u2500\u2518")




def play_game():
  size = ''
  difficulty = ''
  print("""
___  ____                                                   
|  \/  (_)                                                  
| .  . |_ _ __   ___  _____      _____  ___ _ __   ___ _ __ 
| |\/| | | '_ \ / _ \/ __\ \ /\ / / _ \/ _ \ '_ \ / _ \ '__|
| |  | | | | | |  __/\__ \\\ V  V /  __/  __/ |_) |  __/ |   
\_|  |_/_|_| |_|\___||___/ \_/\_/ \___|\___| .__/ \___|_|   
                                           | |              
                                           |_|              
        """)

  while True:
    size = input('What size board would you like to play with? Enter "small", "medium", or "large".\n')
    if size in ['small', 'medium', 'large']:
      break
    print('Invalid input. Please enter a valid choice.')
  while True:
    difficulty = input('What difficulty would you like to play? Enter "easy", "medium", or "hard".\n')
    if difficulty in ['easy', 'medium', 'hard']:
      break
    print('Invalid input. Please enter a valid choice.')
  
  gameboard = create_board(size, difficulty)
  print_board(gameboard)

  while True:
    print('Choose a square!')
    row = int(input('Enter row: '))-1
    column = int(input('Enter column: '))-1
    flag = input('Flag/unflag this square? Y/N: ')
    coord = (column, row)
    selection = gameboard.get_square(coord)
    if flag.upper() == 'Y':
      gameboard.toggle_flag(coord)
    elif flag.upper() == 'N' and selection.flagged is True:
      print('Square is flagged. Cannot select. Try again.')
    else:
      if selection.mine is True:
        for square in gameboard.board_dict.keys():
          if gameboard.board_dict[square].mine == True:
            gameboard.board_dict[square].revealed = True
        print_board(gameboard)
        print('Game Over! You Lost!')
        break
      elif selection.mine is False and selection.adjacents > 0:
        selection.revealed = True
      else:
        selection.revealed = True
        adjs = list(selection.get_adjacents())
        checked = []
        while len(adjs) > 0:
          sqr = gameboard.get_square(adjs[-1])
          checked.append(adjs.pop())
          if sqr.adjacents == 0:
            sqr.revealed = True
            adj_squrs= sqr.get_adjacents()
            for adj_squr in adj_squrs:
              if adj_squr not in checked:
                adjs.append(adj_squr)
            # print(adjs)
          else:
            sqr.revealed = True
    print("\n\n\n\n\n\n\n\n\n\n\n")
    print_board(gameboard)
    game_over = True
    for square in gameboard.board_dict.keys():
      if gameboard.board_dict[square].mine is False and gameboard.board_dict[square].revealed == False:
        game_over = False
        break
    if game_over == True:
      print('Congratulations!! You won!!')
      break
  answer = input('Play again? Y/N\n')
  if answer.upper() == 'Y':
    play_game()
  else:
    print('Thank You for Playing')
    print("""
___  ____                                                   
|  \/  (_)                                                  
| .  . |_ _ __   ___  _____      _____  ___ _ __   ___ _ __ 
| |\/| | | '_ \ / _ \/ __\ \ /\ / / _ \/ _ \ '_ \ / _ \ '__|
| |  | | | | | |  __/\__ \\\\ V  V /  __/  __/ |_) |  __/ |   
\_|  |_/_|_| |_|\___||___/ \_/\_/ \___|\___| .__/ \___|_|   
                                           | |              
                                           |_|              
        """)

play_game()
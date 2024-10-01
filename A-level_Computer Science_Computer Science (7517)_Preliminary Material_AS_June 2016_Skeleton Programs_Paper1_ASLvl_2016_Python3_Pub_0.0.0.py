#Skeleton Program for the AQA AS1 Summer 2016 examination
#this code should be used in conjunction with the Preliminary Material
#written by the AQA AS1 Programmer Team
#developed in a Python 3 programming environment

#Version Number 1.0

import random

def GetRowColumn():
  print()
  Column = int(input("Please enter column: "))
  Row = int(input("Please enter row: "))

  while Row > 9 or Row < 0 or Column > 9 or Column < 0:
    print("That position is out of range. Please enter a valid coordinate.")
    Column = int(input("Please enter column: "))
    Row = int(input("Please enter row: "))
    
  print()
  return Row, Column

def RadarScan(Board, Row, Column):
  Adjacent = []
  Adjacent.append(Board[Row-1][Column])
  Adjacent.append(Board[Row+1][Column])
                  
  Adjacent.append(Board[Row][Column-1])
  Adjacent.append(Board[Row][Column+1])

  for Value in Adjacent:
    if Value in ["A","B","S","D","P","F"]:
      return True

  return False
        
def MakePlayerMove(Board, Ships):
  Row, Column = GetRowColumn()
  
  if Board[Row][Column] == "m" or Board[Row][Column] == "h":
    print("Sorry, you have already shot at the square (" + str(Column) + "," + str(Row) + "). Please try again.")
  elif Board[Row][Column] == "-":
    print("Sorry, (" + str(Column) + "," + str(Row) + ") is a miss.")
    Board[Row][Column] = "m"
    if RadarScan(Board, Row, Column):
      print("Enemy Near!")
    else:
      print("All quiet")
  else:
    ShipType = Board[Row][Column]

    for Ship in Ships:
      if Ship[0][0] == ShipType:
        ShipTypeName = Ship[0]

    print("Hit "+ ShipTypeName +" (" + str(Column) + "," + str(Row) + ").")
        
    Board[Row][Column] = "h"
        
def SetUpBoard():
  Board = []
  for Row in range(10):
    BoardRow = []
    for Column in range(10):
      BoardRow.append("-")
    Board.append(BoardRow)
  return Board

def LoadGame(Filename, Board):
  BoardFile = open(Filename, "r")
  for Row in range(10):
    Line = BoardFile.readline()
    for Column in range(10):
      Board[Row][Column] = Line[Column]
  BoardFile.close()

def SaveGame(Filename, Board):
  File = open(Filename, "w")
  for Row in range(10):
    Line = ""
    for Column in range(10):
      Line = Line + Board[Row][Column]
    File.write(Line + "\n")
  File.close()
    
def PlaceRandomShips(Board, Ships):
  for Ship in Ships:
    Valid = False
    while not Valid:
      Row = random.randint(0, 9) 
      Column = random.randint(0, 9) 
      HorVorD = random.randint(0, 2)
      if HorVorD == 0:
        Orientation = "v" 
      elif HorVorD == 1:
        Orientation = "h"
      else:
        Orientation = "d"
        
      Valid = ValidateBoatPosition(Board, Ship, Row, Column, Orientation)
    print("Computer placing the " + Ship[0])
    PlaceShip(Board, Ship, Row, Column, Orientation)

def PlaceShip(Board, Ship, Row, Column, Orientation):
  if Orientation == "v":
    for Scan in range(Ship[1]):
      Board[Row + Scan][Column] = Ship[0][0]
  elif Orientation == "h":
    for Scan in range(Ship[1]):
      Board[Row][Column + Scan] = Ship[0][0]
  elif Orientation == "d":
    for Scan in range(Ship[1]):
      Board[Row+Scan][Column+Scan] = Ship[0][0]

def ValidateBoatPosition(Board, Ship, Row, Column, Orientation):
  if Orientation == "v" and Row + Ship[1] > 10:
    return False
  elif Orientation == "h" and Column + Ship[1] > 10:
    return False
  elif Orientation == "d" and (Column + Ship[1] > 10) or (Row + Ship[1] > 10):
    return False
  else:
    if Orientation == "v":
      for Scan in range(Ship[1]):
        if Board[Row + Scan][Column] != "-":
          return False
    elif Orientation == "h":
      for Scan in range(Ship[1]):
        if Board[Row][Column + Scan] != "-":
          return False
    if Orientation == "d":
      for Scan in range(Ship[1]):
        if Board[Row + Scan][Column+Scan] != "-":
          return False
  return True

def CheckWin(Board):
  for Row in range(10):
    for Column in range(10):
      if Board[Row][Column] in ["A","B","S","D","P","F"]:
        return False
  return True
 
def PrintBoard(Board):
  print()
  print("The board looks like this: ")  
  print()
  print (" ", end="")
  for Column in range(10):
    print(" " + str(Column) + "  ", end="")
  print()
  for Row in range(10):
    print (str(Row) + " ", end="")
    for Column in range(10):
      if Board[Row][Column] == "-":
        print(" ", end="")
      elif Board[Row][Column] in ["A","B","S","D","P", "F"]:
        print(" ", end="")                
      else:
        print(Board[Row][Column], end="")
      if Column != 9:
        print(" | ", end="")
    print()

def RealBoard(Board):
  print()
  print("The board looks like this: ")  
  print()
  print (" ", end="")
  for Column in range(10):
    print(" " + str(Column) + "  ", end="")
  print()
  for Row in range(10):
    print (str(Row) + " ", end="")
    for Column in range(10):
      if Board[Row][Column] == "-":
        print(" ", end="")
      elif Board[Row][Column] in ["A","B","S","D","P", "F"]:
        print(Board[Row][Column], end="")                
      else:
        print(Board[Row][Column], end="")
      if Column != 9:
        print(" | ", end="")
    print()
       
def DisplayMenu():
  print("MAIN MENU")
  print()
  print("1. Start new game")
  print("2. Load training game")
  print("3. Load saved game")
  print("4. Board Test")
  print("9. Quit")
  print()
    
def GetMainMenuChoice():
  print("Please enter your choice: ", end="")
  Choice = int(input())
  print()
  return Choice

def PlayGame(Board, Ships):
  GameWon = False
  Torpedoes = 20
  while not GameWon:
    PrintBoard(Board)
    MakePlayerMove(Board, Ships)
    Torpedoes = Torpedoes - 1
    print("Torpedoes Left: ", Torpedoes)
    GameWon = CheckWin(Board)
    if GameWon:
      print("All ships sunk!")
      print()
    elif Torpedoes == 0:
      print("GAME OVER! You ran out of ammo")
      break
    else:
      Save = input("Do you want to save the game (Y,N)? ")
      print()

      if Save.lower() == "y":
        Filename = input("Please enter a filename, ending in .txt, to save the game to: ")
        SaveGame(Filename, Board)
        

if __name__ == "__main__":
  TRAININGGAME = "Training.txt"
  MenuOption = 0
  while not MenuOption == 9:
    Board = SetUpBoard()
    Ships = [["Aircraft Carrier", 5], ["Battleship", 4], ["Frigate", 3], ["Submarine", 3], ["Destroyer", 3], ["Patrol Boat", 2]]
    DisplayMenu()
    MenuOption = GetMainMenuChoice()
    if MenuOption == 1:
      PlaceRandomShips(Board, Ships)
      PlayGame(Board,Ships)
    if MenuOption == 2:
      LoadGame(TRAININGGAME, Board)
      PlayGame(Board, Ships)
    if MenuOption == 3:
      FileName = input("Enter a filename to load: ")
      LoadGame(FileName, Board)
      PlayGame(Board, Ships)
    if MenuOption == 4:
      PlaceRandomShips(Board, Ships)
      RealBoard(Board)
    if MenuOption == 9:
      sure = input("Are you sure? ")
      if sure != "Y":
        MenuOption = 0

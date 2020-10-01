from random import choice, randint

class Board(object):
    """
    A playing board
    """
    def __init__(self):
        self.game_board = []
        self.rows = 10
        self.columns = 10
        for row in range(0, self.rows):
            self.game_board.append(["O"] * self.columns)
    
    def display_board(self):
        rownames = [" A |", " B |", " C |", " D |", " E |", " F |", " G |", " H |", " I |", " J |"]
        colnames = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        
        print("     " + " ".join(colnames))
        print("    " + "-" * 21)
        for row in range(0, self.rows):
            print(rownames[row], " ".join(self.game_board[row]))
    
    def coordinate_contains_ship(self, rowcoord, colcoord):
        self.game_board[rowcoord][colcoord] = "#"
    
    def coordinate_contains_miss(self, rowcoord, colcoord):
        self.game_board[rowcoord][colcoord] = "-"
    
    def does_coordinate_contain_ship(self, rowcoord, colcoord):
        if self.game_board[rowcoord][colcoord] == "#":
            return True
        else:
            return False

#class CustomBoard(Board):
#    """
#    A custom playing board
#    """
#    game_board = []
#    def __init__(self, rows, columns):
#        self.rows = rows
#        self.columns = columns
#        for row in range(0, self.rows):
#            self.game_board.append(["O"] * self.columns)

class Ship(object):
    """
    A ship in the game
    """
    def __init__(self):
        self.size = 0
    
    def generate_ship_spaces(self, board):
        startingrow = randint(0, board.rows - 1)
        startingcol = randint(0, board.columns - 1)
        shiplength = self.size
        endingrow = startingrow
        endingcol = startingcol
        uprightdownleft = 0
        if (startingrow + shiplength - 1 >= board.rows) and (startingcol + shiplength - 1 >= board.columns):
            uprightdownleft = choice([1, 4])
        elif (startingrow < shiplength - 1) and (startingcol < shiplength - 1):
            uprightdownleft = choice([2, 3])
        elif (startingrow + shiplength - 1 >= board.rows) and (startingcol < shiplength - 1):
            uprightdownleft = choice([1, 2])
        elif (startingrow < shiplength - 1) and (startingcol + shiplength - 1 >= board.columns):
            uprightdownleft = choice([3, 4])
        elif (startingrow + shiplength - 1 >= board.rows):
            uprightdownleft = choice([1, 2, 4])
        elif (startingrow < shiplength - 1):
            uprightdownleft = choice([2, 3, 4])
        elif startingcol + shiplength - 1 >= board.columns:
            uprightdownleft = choice([1, 3, 4])
        elif startingcol < shiplength - 1:
            uprightdownleft = choice([1, 2, 3])
        else:
            uprightdownleft = choice([1, 2, 3, 4])
        guide = {1 : startingrow - (shiplength - 1),
                 2 : startingcol + (shiplength - 1),
                 3 : startingrow + (shiplength - 1),
                 4 : startingcol - (shiplength - 1)}
        if uprightdownleft % 2 == 1:
            endingrow = guide[uprightdownleft]
        elif uprightdownleft % 2 == 0:
            endingcol = guide[uprightdownleft]
        
        listofcoordinates = []
        for rowcoordinate in range(min(startingrow, endingrow), max(startingrow, endingrow) + 1):
            for columncoordinate in range(min(startingcol, endingcol), max(startingcol, endingcol) + 1):
                listofcoordinates.append([rowcoordinate, columncoordinate])
#        print(listofcoordinates)
        return listofcoordinates

    def are_spaces_empty(self, board, listofcoordinates):
        returnvalue = True
        for coordinatepair in listofcoordinates:
            if board.does_coordinate_contain_ship(coordinatepair[0], coordinatepair[1]):
                returnvalue = False
        return returnvalue

    def place_ship(self, board):
        while(True):
            coordinatelist = self.generate_ship_spaces(board)
            if self.are_spaces_empty(board, coordinatelist):
                for coordinatepair in coordinatelist:
                    board.coordinate_contains_ship(coordinatepair[0], coordinatepair[1])
                break
            else:
                continue

class Carrier(Ship):
    def __init__(self):
        self.size = 5

class Battleship(Ship):
    def __init__(self):
        self.size = 4

class Destroyer(Ship):
    def __init__(self):
        self.size = 3

class Submarine(Ship):
    def __init__(self):
        self.size = 3

class PatrolBoat(Ship):
    def __init__(self):
        self.size = 2

def start_game():
    """
    Runs the Battleship game
    """
    battleship_board = Board()
    ships = get_ships()
    place_ships(ships, battleship_board)
    user_facing_board = Board()
    welcome()
    game_body(battleship_board, user_facing_board)
    

def get_ships():
    """
    Returns list of ships to be placed on the board
    """
    ship1 = Carrier()
    ship2 = Battleship()
    ship3 = Destroyer()
    ship4 = Submarine()
    ship5 = PatrolBoat()
    shiplist = [ship1, ship2, ship3, ship4, ship5]
    return shiplist

def place_ships(shiplist, board):
    for shipitem in shiplist:
        shipitem.place_ship(board)

def welcome():
    print("Welcome to Battleship!")
    print("I've hidden 5 ships throughout this grid.")
    print("The Carrier is 5 spaces long, the Battleship is 4 spaces long, the Destroyer and Submarine are both 3 spaces long, and the Patrol Boat is 2 spaces long.")
    print("The ships are either vertically or horizontally oriented.")
    print("")
    print("Your goal is to sink all my ships by shooting missiles throughout the grid.")
    print("A valid coordinate for a square on this grid is of the form 'E7'.")
    print("*************************************************")
    print("Enter your guess below!")
    print("\n")
    
def get_and_check_user_input(innerboard, userfacingboard, livesstatement):
    returnvalue = ""
    user_guess = ""
    rownames = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    colnames = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    possibleguesses = ["q", "Q"]
    for rowname in rownames:
        for colname in colnames:
            possibleguesses.append(str(rowname) + str(colname))
    rowdict = {"A" : 0, "B" : 1, "C" : 2, "D" : 3, "E" : 4, "F" : 5, "G" : 6, "H" : 7, "I" : 8, "J" : 9}

    while(True):
        print(livesstatement)
        userfacingboard.display_board()
        user_guess = input("Enter your guess or type 'q' or 'Q' to quit: ")
        print("*************************************************")
        print("You guessed '" + user_guess + "'")
        if user_guess not in possibleguesses:
            print("Oops, not a valid guess! Remember, your guess must be in the form 'E7'.")
            print("Guess Again!")
            continue
        elif user_guess == "q" or user_guess == "Q":
            returnvalue = "quit"
            break
        else:
            rowinboard = rowdict[(user_guess[0]).upper()]
            colinboard = int(user_guess[1:]) - 1
            if userfacingboard.game_board[rowinboard][colinboard] != "O":
                print("You already guessed that silly!")
                print("Guess Again!")
                continue
            else:
                if innerboard.does_coordinate_contain_ship(rowinboard, colinboard):
                    print("Oh No! You got a HIT!")
                    userfacingboard.coordinate_contains_ship(rowinboard, colinboard)
                    returnvalue = "hit"
                else:
                    print("Haha, you MISSED!")
                    userfacingboard.coordinate_contains_miss(rowinboard, colinboard)
                    returnvalue = "miss"
                break
    return returnvalue


def final_check_board(innerboard):
    for r in range(0, innerboard.rows):
        for c in range(0, innerboard.columns):
            if innerboard.does_coordinate_contain_ship(r, c):
                innerboard.coordinate_contains_ship(r, c)
            else:
                innerboard.coordinate_contains_miss(r, c)
    innerboard.display_board()

def game_body(innerboard, userfacingboard):
    hits = 0
    misses = 0
    allowedhits = 17
    allowedmisses = 25
    while hits < allowedhits and misses < allowedmisses:
        if hits != 0 or misses != 0:
            print("Guess Again!")
        livesleftstatement = "You have %d lives left." % (allowedmisses - misses)
        hitormiss = get_and_check_user_input(innerboard, userfacingboard, livesleftstatement)
        if hitormiss == "hit":
            hits += 1
        elif hitormiss == "miss":
            misses += 1
        else:
            break
    if hits == allowedhits:
        print("Congratulations! You sank all my ships--you won!")
    elif misses == allowedmisses:
        print("You failed to sink all my ships. You Lost")
    else:
        print("Sorry to see you go :(")
    print("My ships were in these locations:")
    final_check_board(innerboard)
    print("Game Over. Please play again some time!")
    




start_game()



#battleship_board2 = CustomBoard(5, 3)
#battleship_board2.display_board()





























































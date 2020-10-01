# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 22:59:00 2020

@author: Morey Ellis
"""

from random import choice, randint
from graphics import *

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
    
    def coordinate_contains_ship(self, rowcoord, colcoord):
        self.game_board[rowcoord][colcoord] = "#"
    
    def does_coordinate_contain_ship(self, rowcoord, colcoord):
        if self.game_board[rowcoord][colcoord] == "#":
            return True
        else:
            return False

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

def generate_graphic_board(win):
    """
    Builds the Battleship Grid on the blank window fed in
    """
    squares = [] #Creates an 11x11 grid of Squares with fixed pixel locations
    for row in range(11):
        for col in range(11):
            square = Rectangle(Point(19 + (42 * col), 19 + (42 * row)), Point(19 + (42 * (col + 1)), 19 + (42 * (row + 1))))
            squares.append(square)
    for square in squares:
        square.draw(win) #Draws the grid to the window
        
    #The following chunk of code adds labels to the first row and column
    rownames = ["Quit", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    colnames = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    rtitles = []
    ctitles = []
    i = 0
    for rowname in rownames:
        rtitle = Text(Point(40, 40 + (i * 42)), str(rowname))
        rtitles.append(rtitle)
        i += 1
    i = 1
    for colname in colnames:
        ctitle = Text(Point(40 + (i * 42), 40), str(colname))
        ctitles.append(ctitle)
        i += 1
    for rtitle in rtitles:
        rtitle.draw(win)
    for ctitle in ctitles:
        ctitle.draw(win)

def click_squares(win, innerboard):
    alreadyguessed = []
    hits = 0
    misses = 0
    allowedhits = 17
    allowedmisses = 25
    msg = "Click on a square to make a guess.\nYou have %d guesses left" % (allowedmisses - misses)
    txt = Text(Point(250, 550), msg)
    txt.draw(win)
    while hits < allowedhits and misses < allowedmisses:
        clickedpoint = win.getMouse()
        a = int(((clickedpoint.x - 19) // 42) - 1)
        b = int(((clickedpoint.y - 19) // 42) - 1)
        txt.undraw()
        if a == -1 and b == -1:
            break
        elif a not in range(10) or b not in range(10):
            msg = "Not a valid click, please try again.\nClick on a square to make a guess.\nYou have %d lives left" % (allowedmisses - misses)
            txt = Text(Point(250, 550), msg)
            txt.draw(win)
            continue
        elif [a,b] in alreadyguessed:
            msg = "You already guessed this square, please try again!\nClick on a square to make a guess.\nYou have %d lives left" % (allowedmisses - misses)
            txt = Text(Point(250, 550), msg)
            txt.draw(win)
            continue
        elif innerboard.does_coordinate_contain_ship(a, b):
            msg = "You got a HIT!.\nClick on a square to make a guess.\nYou have %d lives left" % (allowedmisses - misses)
            txt = Text(Point(250, 550), msg)
            txt.draw(win)
            hits += 1
            change_color_square(win, a + 1, b + 1, "hit")
            alreadyguessed.append([a,b])
        else:
            misses += 1
            msg = "You got a MISS!.\nClick on a square to make a guess.\nYou have %d lives left" % (allowedmisses - misses)
            txt = Text(Point(250, 550), msg)
            txt.draw(win)
            change_color_square(win, a + 1, b + 1, "miss")
            alreadyguessed.append([a,b])
    if hits == allowedhits:
        msg = "Congratulations! You sank all my ships--you won!"
    elif misses == allowedmisses:
        msg = "You failed to sink all my ships. You Lost"
    else:
        msg = "Sorry to see you go :("
    txt.undraw()
    msg2 = msg + "\nMy ships were in these locations!\nGame Over. Please play again some time!"
    final_change_color_square(win, innerboard)
    txt = Text(Point(250, 550), msg2)
    txt.draw(win)

def change_color_square(win1, a, b, status):
    topleftcorner = Point((19 + (42 * a)), (19 + (42 * b)))
    bottomrightcorner = Point((61 + (42 * a)), (61 + (42 * b)))
    square = Rectangle(topleftcorner, bottomrightcorner)
    if status == "hit":
        square.setFill("red")
    elif status == "miss":
        square.setFill("blue")
    square.draw(win1)

def final_change_color_square(win1, innerboard):
    for a in range(0, 10):
        for b in range(0, 10):
            if innerboard.does_coordinate_contain_ship(a, b):
                change_color_square(win1, a + 1, b + 1, "hit")
            else:
                change_color_square(win1, a + 1, b + 1, "miss")

def run_Battleship():
    win1 = GraphWin("Battleship", 501, 600) #Builds blank window
    battleship_board = Board() #Builds Battleship Board Object
    place_ships(get_ships(), battleship_board) #Populates Battleship Board with Ship Objects
    
    generate_graphic_board(win1)
    click_squares(win1, battleship_board)
    win1.getMouse()
    win1.close()


run_Battleship()






















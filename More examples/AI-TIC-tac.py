#!/usr/bin/env python3
from math import inf as infinity
import platform
import time
from os import system

#Design taken from https://stackoverflow.com/questions/64817261/unable-to-implement-minimax-function-in-python-oop
PLAYER = -1
BOT = +1
GRID = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

def reset():
    global GRID
    GRID= [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]
    return


def clear():
    """
    Clears the console
    """
    os_name = platform.system().upper()
    if 'WINDOWS' in os_name:
        system('cls')
    else:
        system('clear')

def avilabe_cells(state):
    """
    Returns the avilable cell count for a given state of box
    """
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells

def win_state(state):
    """
    Checks if either player has won a the given state
    """
    return wins(state, PLAYER) or wins(state, BOT)

def wins(state, player):
    """
    Possible win states 
    -> Three rows    [X X X] or [O O O]
    -> Three cols    [X X X] or [O O O]
    -> Two diagonals [X X X] or [O O O]
    If a player wins has them then return True else false
    
    """
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False

#Taken From the book http://www.r-5.org/files/books/computers/algo-list/common/Heineman_Pollice_Selkow-Algorithms_in_a_Nutshell-EN.pdf
#Page 175
def best_move_weight(state):
    """
    Function to heuristic evaluation of state.
    returns +1 if the computer wins; -1 if the human wins; 0 if draw
    """
    if wins(state, PLAYER):
        score = -1
    elif wins(state, BOT):
        score = +1
    else:
        score = 0

    return score

#Taken From the book http://www.r-5.org/files/books/computers/algo-list/common/Heineman_Pollice_Selkow-Algorithms_in_a_Nutshell-EN.pdf
#Page 175
def minimax(state, depth, player):
    if player == BOT:
        best = [-1, -1, -infinity] # the [best row, best col, best score]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or win_state(state):
        score = best_move_weight(state)
        return [-1, -1, score]

    for cell in avilabe_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == BOT:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best

def confirm_move(x, y, player):
    """
    Set the move on board, for a valid move
    """
    if [x, y] in avilabe_cells(GRID):
        GRID[x][y] = player
        return True
    else:
        return False

def bot_turn (botCh,humanCh):
    depth = len(avilabe_cells(GRID))
    if depth == 0 or win_state(GRID):
        return
    
    clear()
    print("Bot's turn [" + botCh + "]")
    display(GRID,botCh,humanCh)

    #If bot has to go first always go with [2,1]  to start the game
    # Allow user to have a winning chance
    if depth == 9:
        x,y = 2,1
    
    else:
        move = minimax(GRID, depth, BOT)
        x,y = move[0], move[1]
    
    confirm_move(x,y,BOT)
    time.sleep(1) #mimic latency

#dictonary of possible valid moves
#Separated for Config design/Robust
def possible_moves(move):
    moves = {
        7: [0, 0], 8: [0, 1], 9: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        1: [2, 0], 2: [2, 1], 3: [2, 2],
    }
    
    return moves[move]
    

def human_turn( botCh, humanCh):
    """
    The Human plays choosing a valid move.
    """
    depth = len(avilabe_cells(GRID))
    if depth == 0 or win_state(GRID):
        return
        
    move = -1
    
    clear()
    print("Your turn ["+ botCh + "]")
    display(GRID, botCh, humanCh)

    while move < 1 or move > 9:
        try:
            move = int(input('Use numpad format (1..9): '))
            coord = possible_moves(move)
            can_move = confirm_move(coord[0], coord[1], PLAYER)

            if not can_move:
                print('Bad move')
                move = -1
        except:
            print('Bad choice')

def display (state, botCh, humanCh):
    chars = {
        -1: humanCh, +1: botCh, 0: ' '
    }
    dash = '------------------'

    print('\n' + dash)
    
    for row in state:
        for column in row:
            symbol = chars[column]
            print("|  "+ symbol +" |", end='')
        print('\n' + dash)

def winner_display():
    if wins(GRID, PLAYER):
        print("YOU WIN!")
    elif wins(GRID, BOT):
        print("YOU LOSE!")
    else:
        print("DRAW!")

def driver():
    clear()
    humanSelect = ''
    botSelect = ""
    first_turn = ''

    while humanSelect != "X" and humanSelect != "O":
        try:
            humanSelect = input ("Select x or o \n Selection: ").upper()
        
        except :
            print ("Please Try again.. \n")
    
    if humanSelect == "O":
        botSelect = "X"
    else:
        botSelect = "O"

    clear()
    while first_turn != 'Y' and first_turn != "N":
        try:
            first_turn = input("D you want to go first?: [Y/N]").upper()
        
        except:
            print("Please try again!!")
    
    while len(avilabe_cells(GRID)) > 0 and not win_state(GRID):
        if first_turn == "N":
            bot_turn(botSelect, humanSelect)
            first_turn = ''
        
        human_turn(botSelect,humanSelect)
        bot_turn(botSelect, humanSelect)
    
    # Game over message
    clear()
    display(GRID, botSelect, humanSelect)

    winner_display()
    
    return


def main():
    driver()

    play = ""
    while (play != 'Y' and play != "N"):
        try:
            play = input("D you want to go play again?: [Y/N]").upper()
        
        except:
            print("Please try again!!")

    if play == "Y":
        reset()
        main()
    
    return

if __name__ == '__main__':
    main()
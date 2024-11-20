# import colorama to print with color in the console
from colorama import Fore

# import only system from os
from os import system, name

# import sleep to show output for some time period
from time import sleep

# import random
import random

# Create a matrix of 0's
def createMatrix():
    boarGame = [[0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0]]
    return boarGame

# Defining a points for each position
def definingPointMatrix():
    pointMatrix = [[3,4,5 ,7 ,5 ,4,3],
                   [4,6,8 ,10,8 ,6,4],
                   [5,7,11,13,11,7,5],
                   [5,7,11,13,11,7,5],
                   [4,6,8 ,10,8 ,6,4],
                   [3,4,5 ,7 ,5 ,4,3]]
    return pointMatrix

# Show a decent matrix for the user 
def ShowMatrix(matrix):
    header = "  A B C D E F G  "
    print(Fore.WHITE + header)
    for i in range(0,6):
        line = " " + " "
        for j in range(0,7):
            simbol = Fore.CYAN + "o"
            if matrix[i][j] == AI:
                simbol = Fore.RED + "◉"
            if matrix[i][j] == PLAYER:
                simbol = Fore.YELLOW + "◉"
            line += simbol + " "
        print(line)

# Valid if a player won by row
def winByRow(currentPlayer):
    for i in range(0,len(board)):
        for j in range(0,len(board[0])):
            if (board[i][j] == currentPlayer):
                slots = 0
                slotsNeeded = 4
                cont = j
                while cont < len(board[0]):
                    if board[i][cont] != currentPlayer:
                        break
                    slots += 1
                    cont += 1
                j = cont
                if slots == slotsNeeded:
                    global winnerPlayer
                    winnerPlayer = currentPlayer
                    return True
    return False

# Valid if a player won by column
def winByColumn(currentPlayer):
    for i in range(0,len(board)):
        for j in range(0,len(board[0])):
            if (board[i][j] == currentPlayer):
                slots = 0
                slotsNeeded = 4
                cont = i
                while cont < len(board):
                    if board[cont][j] != currentPlayer:
                        break
                    slots += 1
                    cont += 1
                if slots == slotsNeeded:
                    global winnerPlayer
                    winnerPlayer = currentPlayer
                    return True
    return False

# Valid if a player won by diagonal
def winByDiagonal(currentPlayer):
    for i in range(0,len(board)):
        for j in range(0,len(board[0])):
            if (board[i][j] == currentPlayer):
                if (validateDiagonal(i,j,currentPlayer,"left") or validateDiagonal(i,j,currentPlayer,"right")):
                    global winnerPlayer
                    winnerPlayer = currentPlayer
                    return True
    return False

# Valid if a winner in diagonal way (right or left)
def validateDiagonal(i,j,currentPlayer,direction):
    slots = 0
    slotsNeeded = 4
    diagonal = -1 if direction == "left" else 1
    while i < len(board) and j < len(board[0]):
        if board[i][j] != currentPlayer:
            break
        slots += 1
        i += 1
        j += diagonal
    return slots == slotsNeeded

#Check if it's a tie                    
def isTie():
    for i in range(0,len(board)):
        for j in range(0,len(board[0])):
            if board[i][j] == EMPTY_SLOT:
                return False
    return True

# Check if game has ended
def IsFinishGame():
    if (winByRow(PLAYER) or winByRow(AI)):
        return True
    elif (winByColumn(PLAYER) or winByColumn(AI)):
        return True
    elif (winByDiagonal(PLAYER) or winByDiagonal(AI)):
        return True
    elif (isTie()):
        return True
    else:
        return False 

# define our clear function
def clear():
 
    # for windows
    if name == 'nt':
        _ = system('cls')
 
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

# Print a simple message in the console to print the AI movement
def showThinkingMessage():
    message = "Thinking"
    point = 0
    for i in range(0,7):
        if point == 3:
            message = "Thinking"
            point = 0
        message += "."
        point += 1
        print("AI turns")
        print(message)
        sleep(0.3)
        clear()

# Set Token in a specif slot of the board
def setSlotPlayer(column,currentPlayer):
    bottom = 5
    while(bottom >= 0):
        if board[bottom][column] == EMPTY_SLOT:
            board[bottom][column] = currentPlayer
            break
        bottom -= 1

# Set Token in a specif slot of the board
def getBottom(boardCopy,column):
    bottom = 5
    while(bottom >= 0):
        if boardCopy[bottom][column] == EMPTY_SLOT:
            return bottom
        bottom -= 1
    return -1

# Check if it is a valid position
def ifValidPosition(board,column):
    bottom = 5
    while(bottom >= 0):
        if board[bottom][column] == EMPTY_SLOT:
            return True
        bottom -= 1
    return False

# Validate the player position chosen
def PlayerPlaying():
    while (True):
        ShowMatrix(board)
        print()
        print(Fore.CYAN + "Your turn")
        option = input(Fore.CYAN + "Enter your position: ")
        option = option.upper()
        if (not (option in ROW_OPTIONS) or not ifValidPosition(board,ROW_OPTIONS[option])):
            print(Fore.RED + "**** Invalid position ****")
            sleep(1)
            clear()
            
        elif ifValidPosition(board,ROW_OPTIONS[option]):
            setSlotPlayer(ROW_OPTIONS[option],PLAYER)
            break
    clear()

# Find the best for the AI using the min max algorithm with alpá-betha pruning
def find_best_move(board):
    best_val = -1000
    best_move = [-1, -1]
    
    # Traverse all cells, evaluate minimax function for all empty cells, and return the cell with the optimal value.
    columnsOrderByPriority = [0,1,2,3,4,5,6]
    for column in columnsOrderByPriority:
        if not ifValidPosition(board,column):
            continue
        row = getBottom(board,column)

        # Check if cell is empty
        if board[row][column] == EMPTY_SLOT:

            # Make the move
            board[row][column] = AI
                
            # Compute evaluation function for this move
            initial_alpha = -float('inf')
            initial_beta = float('inf')
            move_val = minMaxAlphaBeta(board,4,initial_alpha,initial_beta,PLAYER)

            # Undo the move
            board[row][column] = EMPTY_SLOT
                
            # If the value of the current move is more than the best value, update best
            if move_val > best_val:
                best_move = [row, column]
                best_val = move_val

    return best_move

# Board Evalution score = AI points - PLAYER point
def calculateHeuristicPoints(boardCopy):
    AIPoint = 0
    PlayerPoint = 0
    for i in range(len(boardCopy)):
        for j in range(len(boardCopy[0])):
            if boardCopy[i][j] != EMPTY_SLOT:
                if boardCopy[i][j] == AI:
                    AIPoint += POINT_MATRIX[i][j]
                else:
                    PlayerPoint += POINT_MATRIX[i][j]
    isWinnerAI = 100 if winByColumn(AI) or winByRow(AI) or winByDiagonal(AI) else 0
    isWinnerPlayer = 100 if winByColumn(PLAYER) or winByRow(PLAYER) or winByDiagonal(PLAYER) else 0
    result = (AIPoint  + isWinnerAI) - (PlayerPoint + isWinnerPlayer)
    return result

# The minMaxAlphaBeta pruning adapted to connect4
def minMaxAlphaBeta(boardCopy,depth,alpha,beta,currentPlayer):
    if IsFinishGame() or depth == 0:
        return calculateHeuristicPoints(boardCopy)
    if currentPlayer == AI:
        maxEval = -float('inf')
        for column in [0,1,2,3,4,5,6]:
            if not ifValidPosition(boardCopy,column):
                continue
            row = getBottom(boardCopy,column)
            boardCopy[row][column] = currentPlayer
            eval = minMaxAlphaBeta(boardCopy, depth - 1, alpha, beta, PLAYER)
            boardCopy[row][column] = EMPTY_SLOT
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = float('inf')
        for column in [0,1,2,3,4,5,6]:
            if not ifValidPosition(boardCopy,column):
                continue
            row = getBottom(boardCopy,column)
            boardCopy[row][column] = currentPlayer
            eval = minMaxAlphaBeta(boardCopy, depth - 1, alpha, beta, AI)
            boardCopy[row][column] = EMPTY_SLOT
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval  
    
def IaPlaying():
    showThinkingMessage()
    bestMove = find_best_move(board)
    board[bestMove[0]][bestMove[1]] = AI

# Main program
def main():
    turn = PLAYER
    while (not IsFinishGame()):
        clear()
        if turn == PLAYER:
            PlayerPlaying()
            turn = AI
        else:
            IaPlaying()
            turn = PLAYER
    ShowMatrix(board)
    whoWon = "AI" if winnerPlayer == AI else "Player"
    message = f"Game ended {whoWon} has won. Congrats!"
    print(message)


board = createMatrix()
POINT_MATRIX = definingPointMatrix()
EMPTY_SLOT = 0
PLAYER = 1
AI = 2
global winnerPlayer
winnerPlayer = 0
ROW_OPTIONS = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6}
main()
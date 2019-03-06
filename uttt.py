from time import sleep
from math import inf
from random import randint
import random

class ultimateTicTacToe:
    def __init__(self):
        """
        Initialization of the game.
        """
        self.board=[['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_']]
        self.maxPlayer='X'
        self.minPlayer='O'
        self.maxDepth=3
        #The start indexes of each local board
        self.globalIdx=[(0,0),(0,3),(0,6),(3,0),(3,3),(3,6),(6,0),(6,3),(6,6)]

        #Start local board index for reflex agent playing
        self.startBoardIdx=4
        self.initialBoardIdx=4
        self.minimax_tree=0
        #self.startBoardIdx=randint(0,8)
        #utility value for reflex offensive and reflex defensive agents
        self.winnerMaxUtility=10000
        self.twoInARowMaxUtility=500
        self.preventThreeInARowMaxUtility=100
        self.cornerMaxUtility=30

        self.winnerMinUtility=-10000
        self.twoInARowMinUtility=-100
        self.preventThreeInARowMinUtility=-500
        self.cornerMinUtility=-30

        self.expandedNodes=0
        self.currPlayer=True

    def prevent_two_in_row(self, currBoardIdx, player):
        x = self.globalIdx[currBoardIdx]

        score = 0

        if player == 0:
            #Check for two in a row in corners
            if self.board[x[0]][x[1]] == self.maxPlayer and self.board[x[0]][x[1] + 1] == self.maxPlayer and self.board[x[0]][x[1] + 2] == self.minPlayer:
                score += -500
            if self.board[x[0]][x[1]] == self.maxPlayer and self.board[x[0] + 1][x[1] + 1] == self.maxPlayer and self.board[x[0] + 2][x[1] + 2] == self.minPlayer:
                score += -500
            if self.board[x[0]][x[1]] == self.maxPlayer and self.board[x[0] + 1][x[1]] == self.maxPlayer and self.board[x[0] + 2][x[1]] == self.minPlayer:
                score += -500

            if self.board[x[0]][x[1] + 2] == self.maxPlayer and self.board[x[0]][x[1] + 1] == self.maxPlayer and self.board[x[0]][x[1]] == self.minPlayer:
                score += -500
            if self.board[x[0]][x[1] + 2] == self.maxPlayer and self.board[x[0] + 1][x[1] + 1] == self.maxPlayer and self.board[x[0] + 2][x[1]] == self.minPlayer:
                score += -500
            if self.board[x[0]][x[1] + 2] == self.maxPlayer and self.board[x[0] + 1][x[1] + 2] == self.maxPlayer and self.board[x[0] + 2][x[1] + 2] == self.minPlayer:
                score += -500

            if self.board[x[0] + 2][x[1] + 2] == self.maxPlayer and self.board[x[0] + 1][x[1] + 2] == self.maxPlayer and self.board[x[0]][x[1] + 2] == self.minPlayer:
                score += -500
            if self.board[x[0] + 2][x[1] + 2] == self.maxPlayer and self.board[x[0] + 1][x[1] + 1] == self.maxPlayer and self.board[x[0]][x[1]] == self.minPlayer:
                score += -500
            if self.board[x[0] + 2][x[1] + 2] == self.maxPlayer and self.board[x[0] + 2][x[1] + 1] == self.maxPlayer and self.board[x[0] + 2][x[1]] == self.minPlayer:
                score += -500

            if self.board[x[0] + 2][x[1]] == self.maxPlayer and self.board[x[0] + 1][x[1]] == self.maxPlayer and self.board[x[0]][x[1]] == self.minPlayer:
                score += -500
            if self.board[x[0] + 2][x[1]] == self.maxPlayer and self.board[x[0] + 1][x[1] + 1] == self.maxPlayer and self.board[x[0]][x[1] + 2] == self.minPlayer:
                score += -500
            if self.board[x[0] + 2][x[1]] == self.maxPlayer and self.board[x[0] + 2][x[1] + 1] == self.maxPlayer and self.board[x[0] + 2][x[1] + 2] == self.minPlayer:
                score += -500
            #Check for two in a row in the middle spots
            if self.board[x[0]][x[1] + 1] == self.maxPlayer and self.board[x[0] + 1][x[1] + 1] == self.maxPlayer and self.board[x[0] + 2][x[1] + 1] == self.minPlayer:
                score += -500
            if self.board[x[0] + 1][x[1] + 2] == self.maxPlayer and self.board[x[0] + 1][x[1] + 1] == self.maxPlayer and self.board[x[0] + 1][x[1]] == self.minPlayer:
                score += -500
            if self.board[x[0] + 2][x[1] + 1] == self.maxPlayer and self.board[x[0] + 1][x[1] + 1] == self.maxPlayer and self.board[x[0]][x[1] + 1] == self.minPlayer:
                score += -500
            if self.board[x[0] + 1][x[1]] == self.maxPlayer and self.board[x[0] + 1][x[1] + 1] == self.maxPlayer and self.board[x[0] + 1][x[1] + 2] == self.minPlayer:
                score += -500

            if self.board[x[0]][x[1]] == self.maxPlayer and self.board[x[0]][x[1] + 1] == self.minPlayer and self.board[x[0]][x[1] + 2] == self.maxPlayer:
                score += -500
            if self.board[x[0] + 1][x[1]] == self.maxPlayer and self.board[x[0] + 1][x[1] + 1] == self.minPlayer and self.board[x[0] + 1][x[1] + 2] == self.maxPlayer:
                score += -500
            if self.board[x[0] + 2][x[1]] == self.maxPlayer and self.board[x[0] + 2][x[1] + 1] == self.minPlayer and self.board[x[0] + 2][x[1] + 2] == self.maxPlayer:
                score += -500

            if self.board[x[0]][x[1]] == self.maxPlayer and self.board[x[0] + 1][x[1]] == self.minPlayer and self.board[x[0] + 2][x[1]] == self.maxPlayer:
                score += -500
            if self.board[x[0]][x[1] + 1] == self.maxPlayer and self.board[x[0] + 1][x[1] + 1] == self.minPlayer and self.board[x[0] + 2][x[1] + 1] == self.maxPlayer:
                score += -500
            if self.board[x[0]][x[1] + 2] == self.maxPlayer and self.board[x[0] + 1][x[1] + 2] == self.minPlayer and self.board[x[0] + 2][x[1] + 2] == self.maxPlayer:
                score += -500

            if self.board[x[0]][x[1]] == self.maxPlayer and self.board[x[0] + 1][x[1] + 1] == self.minPlayer and self.board[x[0] + 2][x[1] + 2] == self.maxPlayer:
                score += -500
            if self.board[x[0] + 2][x[1]] == self.maxPlayer and self.board[x[0] + 1][x[1] + 1] == self.minPlayer and self.board[x[0]][x[1] + 2] == self.maxPlayer:
                score += -500

        else:
            #Check for two in a row in corners
            if self.board[x[0]][x[1]] == self.minPlayer and self.board[x[0]][x[1] + 1] == self.minPlayer and self.board[x[0]][x[1] + 2] == self.maxPlayer:
                score += 100
            if self.board[x[0]][x[1]] == self.minPlayer and self.board[x[0] + 1][x[1] + 1] == self.minPlayer and self.board[x[0] + 2][x[1] + 2] == self.maxPlayer:
                score += 100
            if self.board[x[0]][x[1]] == self.minPlayer and self.board[x[0] + 1][x[1]] == self.minPlayer and self.board[x[0] + 2][x[1]] == self.maxPlayer:
                score += 100

            if self.board[x[0]][x[1] + 2] == self.minPlayer and self.board[x[0]][x[1] + 1] == self.minPlayer and self.board[x[0]][x[1]] == self.maxPlayer:
                score += 100
            if self.board[x[0]][x[1] + 2] == self.minPlayer and self.board[x[0] + 1][x[1] + 1] == self.minPlayer and self.board[x[0] + 2][x[1]] == self.maxPlayer:
                score += 100
            if self.board[x[0]][x[1] + 2] == self.minPlayer and self.board[x[0] + 1][x[1] + 2] == self.minPlayer and self.board[x[0] + 2][x[1] + 2] == self.maxPlayer:
                score += 100

            if self.board[x[0] + 2][x[1] + 2] == self.minPlayer and self.board[x[0] + 1][x[1] + 2] == self.minPlayer and self.board[x[0]][x[1] + 2] == self.maxPlayer:
                score += 100
            if self.board[x[0] + 2][x[1] + 2] == self.minPlayer and self.board[x[0] + 1][x[1] + 1] == self.minPlayer and self.board[x[0]][x[1]] == self.maxPlayer:
                score += 100
            if self.board[x[0] + 2][x[1] + 2] == self.minPlayer and self.board[x[0] + 2][x[1] + 1] == self.minPlayer and self.board[x[0] + 2][x[1]] == self.maxPlayer:
                score += 100

            if self.board[x[0] + 2][x[1]] == self.minPlayer and self.board[x[0] + 1][x[1]] == self.minPlayer and self.board[x[0]][x[1]] == self.maxPlayer:
                score += 100
            if self.board[x[0] + 2][x[1]] == self.minPlayer and self.board[x[0] + 1][x[1] + 1] == self.minPlayer and self.board[x[0]][x[1] + 2] == self.maxPlayer:
                score += 100
            if self.board[x[0] + 2][x[1]] == self.minPlayer and self.board[x[0] + 2][x[1] + 1] == self.minPlayer and self.board[x[0] + 2][x[1] + 2] == self.maxPlayer:
                score += 100
            #Check for two in a row in the middle spots
            if self.board[x[0]][x[1] + 1] == self.minPlayer and self.board[x[0] + 1][x[1] + 1] == self.minPlayer and self.board[x[0] + 2][x[1] + 1] == self.maxPlayer:
                score += 100
            if self.board[x[0] + 1][x[1] + 2] == self.minPlayer and self.board[x[0] + 1][x[1] + 1] == self.minPlayer and self.board[x[0] + 1][x[1]] == self.maxPlayer:
                score += 100
            if self.board[x[0] + 2][x[1] + 1] == self.minPlayer and self.board[x[0] + 1][x[1] + 1] == self.minPlayer and self.board[x[0]][x[1] + 1] == self.maxPlayer:
                score += 100
            if self.board[x[0] + 1][x[1]] == self.minPlayer and self.board[x[0] + 1][x[1] + 1] == self.minPlayer and self.board[x[0] + 1][x[1] + 2] == self.maxPlayer:
                score += 100

            if self.board[x[0]][x[1]] == self.minPlayer and self.board[x[0]][x[1] + 1] == self.maxPlayer and self.board[x[0]][x[1] + 2] == self.minPlayer:
                score += 100
            if self.board[x[0] + 1][x[1]] == self.minPlayer and self.board[x[0] + 1][x[1] + 1] == self.maxPlayer and self.board[x[0] + 1][x[1] + 2] == self.minPlayer:
                score += 100
            if self.board[x[0] + 2][x[1]] == self.minPlayer and self.board[x[0] + 2][x[1] + 1] == self.maxPlayer and self.board[x[0] + 2][x[1] + 2] == self.minPlayer:
                score += 100

            if self.board[x[0]][x[1]] == self.minPlayer and self.board[x[0] + 1][x[1]] == self.maxPlayer and self.board[x[0] + 2][x[1]] == self.minPlayer:
                score += 100
            if self.board[x[0]][x[1] + 1] == self.minPlayer and self.board[x[0] + 1][x[1] + 1] == self.maxPlayer and self.board[x[0] + 2][x[1] + 1] == self.minPlayer:
                score += 100
            if self.board[x[0]][x[1] + 2] == self.minPlayer and self.board[x[0] + 1][x[1] + 2] == self.maxPlayer and self.board[x[0] + 2][x[1] + 2] == self.minPlayer:
                score += 100

            if self.board[x[0]][x[1]] == self.minPlayer and self.board[x[0] + 1][x[1] + 1] == self.maxPlayer and self.board[x[0] + 2][x[1] + 2] == self.minPlayer:
                score += 100
            if self.board[x[0] + 2][x[1]] == self.minPlayer and self.board[x[0] + 1][x[1] + 1] == self.maxPlayer and self.board[x[0]][x[1] + 2] == self.minPlayer:
                score += 100
        return score

    def corner_utility(self, currBoardIdx, player):
        x = self.globalIdx[currBoardIdx]
        
        score = 0
        
        if player == 1:
            #Check corners for maxPlayer utility score
            if self.board[x[0]][x[1]] == self.maxPlayer:
                score += 30
            if self.board[x[0]][x[1] + 2] == self.maxPlayer:
                score += 30
            if self.board[x[0] + 2][x[1]] == self.maxPlayer:
                score += 30
            if self.board[x[0]+ 2][x[1] + 2] == self.maxPlayer:
                score += 30
        else:
            if self.board[x[0]][x[1]] == self.minPlayer:
                score += -30
            if self.board[x[0]][x[1] + 2] == self.minPlayer:
                score += -30
            if self.board[x[0] + 2][x[1]] == self.minPlayer:
                score += -30
            if self.board[x[0]+ 2][x[1] + 2] == self.minPlayer:
                score += -30

        return score

    def two_in_row_utility(self, currBoardIdx, player):
        x = self.globalIdx[currBoardIdx]

        score = 0

        if player == 1:
            #Check for two in a row in corners
            if self.board[x[0]][x[1]] == self.maxPlayer and self.board[x[0]][x[1] + 1] == self.maxPlayer and self.board[x[0]][x[1] + 2] != self.minPlayer:
                score += 500
            if self.board[x[0]][x[1]] == self.maxPlayer and self.board[x[0] + 1][x[1] + 1] == self.maxPlayer and self.board[x[0] + 2][x[1] + 2] != self.minPlayer:
                score += 500
            if self.board[x[0]][x[1]] == self.maxPlayer and self.board[x[0] + 1][x[1]] == self.maxPlayer and self.board[x[0] + 2][x[1]] != self.minPlayer:
                score += 500

            if self.board[x[0]][x[1] + 2] == self.maxPlayer and self.board[x[0]][x[1] + 1] == self.maxPlayer and self.board[x[0]][x[1]] != self.minPlayer:
                score += 500
            if self.board[x[0]][x[1] + 2] == self.maxPlayer and self.board[x[0] + 1][x[1] + 1] == self.maxPlayer and self.board[x[0] + 2][x[1]] != self.minPlayer:
                score += 500
            if self.board[x[0]][x[1] + 2] == self.maxPlayer and self.board[x[0] + 1][x[1] + 2] == self.maxPlayer and self.board[x[0] + 2][x[1] + 2] != self.minPlayer:
                score += 500

            if self.board[x[0] + 2][x[1] + 2] == self.maxPlayer and self.board[x[0] + 1][x[1] + 2] == self.maxPlayer and self.board[x[0]][x[1] + 2] != self.minPlayer:
                score += 500
            if self.board[x[0] + 2][x[1] + 2] == self.maxPlayer and self.board[x[0] + 1][x[1] + 1] == self.maxPlayer and self.board[x[0]][x[1]] != self.minPlayer:
                score += 500
            if self.board[x[0] + 2][x[1] + 2] == self.maxPlayer and self.board[x[0] + 2][x[1] + 1] == self.maxPlayer and self.board[x[0] + 2][x[1]] != self.minPlayer:
                score += 500

            if self.board[x[0] + 2][x[1]] == self.maxPlayer and self.board[x[0] + 1][x[1]] == self.maxPlayer and self.board[x[0]][x[1]] != self.minPlayer:
                score += 500
            if self.board[x[0] + 2][x[1]] == self.maxPlayer and self.board[x[0] + 1][x[1] + 1] == self.maxPlayer and self.board[x[0]][x[1] + 2] != self.minPlayer:
                score += 500
            if self.board[x[0] + 2][x[1]] == self.maxPlayer and self.board[x[0] + 2][x[1] + 1] == self.maxPlayer and self.board[x[0] + 2][x[1] + 2] != self.minPlayer:
                score += 500
            #Check for two in a row in the middle spots
            if self.board[x[0]][x[1] + 1] == self.maxPlayer and self.board[x[0] + 1][x[1] + 1] == self.maxPlayer and self.board[x[0] + 2][x[1] + 1] != self.minPlayer:
                score += 500
            if self.board[x[0] + 1][x[1] + 2] == self.maxPlayer and self.board[x[0] + 1][x[1] + 1] == self.maxPlayer and self.board[x[0] + 1][x[1]] != self.minPlayer:
                score += 500
            if self.board[x[0] + 2][x[1] + 1] == self.maxPlayer and self.board[x[0] + 1][x[1] + 1] == self.maxPlayer and self.board[x[0]][x[1] + 1] != self.minPlayer:
                score += 500
            if self.board[x[0] + 1][x[1]] == self.maxPlayer and self.board[x[0] + 1][x[1] + 1] == self.maxPlayer and self.board[x[0] + 1][x[1] + 2] != self.minPlayer:
                score += 500

        else:
            #Check for two in a row in corners
            if self.board[x[0]][x[1]] == self.minPlayer and self.board[x[0]][x[1] + 1] == self.minPlayer and self.board[x[0]][x[1] + 2] != self.maxPlayer:
                score += -100
            if self.board[x[0]][x[1]] == self.minPlayer and self.board[x[0] + 1][x[1] + 1] == self.minPlayer and self.board[x[0] + 2][x[1] + 2] != self.maxPlayer:
                score += -100
            if self.board[x[0]][x[1]] == self.minPlayer and self.board[x[0] + 1][x[1]] == self.minPlayer and self.board[x[0] + 2][x[1]] != self.maxPlayer:
                score += -100

            if self.board[x[0]][x[1] + 2] == self.minPlayer and self.board[x[0]][x[1] + 1] == self.minPlayer and self.board[x[0]][x[1]] != self.maxPlayer:
                score += -100
            if self.board[x[0]][x[1] + 2] == self.minPlayer and self.board[x[0] + 1][x[1] + 1] == self.minPlayer and self.board[x[0] + 2][x[1]] != self.maxPlayer:
                score += -100
            if self.board[x[0]][x[1] + 2] == self.minPlayer and self.board[x[0] + 1][x[1] + 2] == self.minPlayer and self.board[x[0] + 2][x[1] + 2] != self.maxPlayer:
                score += -100

            if self.board[x[0] + 2][x[1] + 2] == self.minPlayer and self.board[x[0] + 1][x[1] + 2] == self.minPlayer and self.board[x[0]][x[1] + 2] != self.maxPlayer:
                score += -100
            if self.board[x[0] + 2][x[1] + 2] == self.minPlayer and self.board[x[0] + 1][x[1] + 1] == self.minPlayer and self.board[x[0]][x[1]] != self.maxPlayer:
                score += -100
            if self.board[x[0] + 2][x[1] + 2] == self.minPlayer and self.board[x[0] + 2][x[1] + 1] == self.minPlayer and self.board[x[0] + 2][x[1]] != self.maxPlayer:
                score += -100

            if self.board[x[0] + 2][x[1]] == self.minPlayer and self.board[x[0] + 1][x[1]] == self.minPlayer and self.board[x[0]][x[1]] != self.maxPlayer:
                score += -100
            if self.board[x[0] + 2][x[1]] == self.minPlayer and self.board[x[0] + 1][x[1] + 1] == self.minPlayer and self.board[x[0]][x[1] + 2] != self.maxPlayer:
                score += -100
            if self.board[x[0] + 2][x[1]] == self.minPlayer and self.board[x[0] + 2][x[1] + 1] == self.minPlayer and self.board[x[0] + 2][x[1] + 2] != self.maxPlayer:
                score += -100
            #Check for two in a row in the middle spots
            if self.board[x[0]][x[1] + 1] == self.minPlayer and self.board[x[0] + 1][x[1] + 1] == self.minPlayer and self.board[x[0] + 2][x[1] + 1] != self.maxPlayer:
                score += -100
            if self.board[x[0] + 1][x[1] + 2] == self.minPlayer and self.board[x[0] + 1][x[1] + 1] == self.minPlayer and self.board[x[0] + 1][x[1]] != self.maxPlayer:
                score += -100
            if self.board[x[0] + 2][x[1] + 1] == self.minPlayer and self.board[x[0] + 1][x[1] + 1] == self.minPlayer and self.board[x[0]][x[1] + 1] != self.maxPlayer:
                score += -100
            if self.board[x[0] + 1][x[1]] == self.minPlayer and self.board[x[0] + 1][x[1] + 1] == self.minPlayer and self.board[x[0] + 1][x[1] + 2] != self.maxPlayer:
                score += -100
        return score

    def printGameBoard(self):
        """
        This function prints the current game board.
        """
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[:3]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[3:6]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[6:9]])+'\n')


    def evaluatePredifined(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for predifined agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        #YOUR CODE HERE
        flag_two = 0
        flag_corner = 0
        for x in range(0, len(self.globalIdx)):
            if isMax == 0:
                if self.two_in_row_utility(x, 1) or self.prevent_two_in_row(x, 1):
                    flag_two = 1
                    if flag_corner == 1:
                        flag_corner = 0
                elif self.corner_utility(x, 1):
                    if flag_two == 0:
                        flag_corner = 1
            else:
                if self.two_in_row_utility(x, 0) < 0 or self.prevent_two_in_row(x, 0) < 0:
                    flag_two = 1
                    if flag_corner == 1:
                        flag_corner = 0
                elif self.corner_utility(x, 0) < 0:
                    if flag_two == 0:
                        flag_corner = 1

        score = 0
        for x in range(0, len(self.globalIdx)):
            if isMax == 0:
                if self.checkWinner() == 1:
                    score = 10000
                    break
                elif (self.two_in_row_utility(x, 1) or self.prevent_two_in_row(x, 1)):
                    if flag_two == 1:
                        score += self.two_in_row_utility(x, 1)
                        score += self.prevent_two_in_row(x, 1)
                elif self.corner_utility(x, 1):
                    if flag_corner == 1:
                        score += self.corner_utility(x, 1)
            elif isMax == 1:
                if self.checkWinner() == -1:
                    score = -10000
                    break
                elif self.two_in_row_utility(x, 0) < 0 or self.prevent_two_in_row(x, 0) < 0:
                    if flag_two == 1:
                        score += self.two_in_row_utility(x, 0)
                        score += self.prevent_two_in_row(x, 0)
                elif self.corner_utility(x, 0) < 0:
                    if flag_corner == 1:
                        score += self.corner_utility(x, 0)
        
        return score


    def evaluateDesigned(self, isMax):
        score=0

        x = self.globalIdx[self.startBoardIdx]

        if isMax == 1:
            if self.board[0][0] == self.minPlayer:  #Never play at the startBoardIdx or at 0 index
                score = inf
        else:    
            if self.board[0][0] == self.maxPlayer:  #Never play at the startBoardIdx or at 0 index
                score = -inf

        for x in range(0, 3):
            for y in range(0, 3):
                if isMax == 1:
                    if self.board[x][y] == self.minPlayer:
                        if self.find_next_board((x, y), 0) == self.initialBoardIdx:
                            score = inf
                else:
                    if self.board[x][y] == self.maxPlayer:
                        if self.find_next_board((x, y), 0) == self.initialBoardIdx:
                            score = -inf

        return score

    def checkMovesLeft(self):
        for x in range(0, 9):
            cnt = 0
            i = self.globalIdx[x]
            for row in range(0, 3):
                for col in range(0, 3):
                    if self.board[row][col] != '_':
                        cnt += 1
            if cnt == 9:
                return False
        return True

    def checkWinner(self):
        #Return termimnal node status for maximizer player 1-win,0-tie,-1-lose
        """
        This function checks whether there is a winner on the board.
        output:
        winner(int): Return 0 if there is no winner.
                     Return 1 if maxPlayer is the winner.
                     Return -1 if miniPlayer is the winner.
        """
        #YOUR CODE HERE

        for i in range(0, len(self.globalIdx)):
            x = self.globalIdx[i]
            if self.board[x[0]][x[1]] == self.maxPlayer and self.board[x[0]][x[1] + 1] == self.maxPlayer and self.board[x[0]][x[1] + 2] == self.maxPlayer:
                return 1
                #max_player_won.append(x)
            elif self.board[x[0] + 1][x[1]] == self.maxPlayer and self.board[x[0] + 1][x[1] + 1] == self.maxPlayer and self.board[x[0] + 1][x[1] + 2] == self.maxPlayer:
                return 1
            elif self.board[x[0] + 2][x[1]] == self.maxPlayer and self.board[x[0] + 2][x[1] + 1] == self.maxPlayer and self.board[x[0] + 2][x[1] + 2] == self.maxPlayer:
                return 1
            elif self.board[x[0]][x[1]] == self.maxPlayer and self.board[x[0] + 1][x[1]] == self.maxPlayer and self.board[x[0] + 2][x[1]] == self.maxPlayer:
                return 1
            elif self.board[x[0]][x[1] + 1] == self.maxPlayer and self.board[x[0] + 1][x[1] + 1] == self.maxPlayer and self.board[x[0] + 2][x[1] + 1] == self.maxPlayer:
                return 1
            elif self.board[x[0]][x[1] + 2] == self.maxPlayer and self.board[x[0] + 1][x[1] + 2] == self.maxPlayer and self.board[x[0] + 2][x[1] + 2] == self.maxPlayer:
                return 1
            elif self.board[x[0]][x[1]] == self.maxPlayer and self.board[x[0] + 1][x[1] + 1] == self.maxPlayer and self.board[x[0] + 2][x[1] + 2] == self.maxPlayer:
                return 1
            elif self.board[x[0]][x[1] + 2] == self.maxPlayer and self.board[x[0] + 1][x[1] + 1] == self.maxPlayer and self.board[x[0] + 2][x[1]] == self.maxPlayer:
                return 1

            if self.board[x[0]][x[1]] == self.minPlayer and self.board[x[0]][x[1] + 1] == self.minPlayer and self.board[x[0]][x[1] + 2] == self.minPlayer:
                return -1
                #max_player_won.append(x)
            elif self.board[x[0] + 1][x[1]] == self.minPlayer and self.board[x[0] + 1][x[1] + 1] == self.minPlayer and self.board[x[0] + 1][x[1] + 2] == self.minPlayer:
                return -1
            elif self.board[x[0] + 2][x[1]] == self.minPlayer and self.board[x[0] + 2][x[1] + 1] == self.minPlayer and self.board[x[0] + 2][x[1] + 2] == self.minPlayer:
                return -1
            elif self.board[x[0]][x[1]] == self.minPlayer and self.board[x[0] + 1][x[1]] == self.minPlayer and self.board[x[0] + 2][x[1]] == self.minPlayer:
                return -1
            elif self.board[x[0]][x[1] + 1] == self.minPlayer and self.board[x[0] + 1][x[1] + 1] == self.minPlayer and self.board[x[0] + 2][x[1] + 1] == self.minPlayer:
                return -1
            elif self.board[x[0]][x[1] + 2] == self.minPlayer and self.board[x[0] + 1][x[1] + 2] == self.minPlayer and self.board[x[0] + 2][x[1] + 2] == self.minPlayer:
                return -1
            elif self.board[x[0]][x[1]] == self.minPlayer and self.board[x[0] + 1][x[1] + 1] == self.minPlayer and self.board[x[0] + 2][x[1] + 2] == self.minPlayer:
                return -1
            elif self.board[x[0]][x[1] + 2] == self.minPlayer and self.board[x[0] + 1][x[1] + 1] == self.minPlayer and self.board[x[0] + 2][x[1]] == self.minPlayer:
                return -1 
        return 0

    def alphabeta(self,depth,currBoardIdx,alpha,beta,isMax):
        #Get empty spaces on local_board
        empty_locations = self.get_empty_location(currBoardIdx)

        #if self.checkWinner() != 0:
        #    return self.checkWinner()

        if depth == 3:
            self.minimax_tree += 1
            return self.evaluatePredifined(isMax)
        #Check the winner, set utility score accordingly

        #Pseudocode retrieved from https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
        if isMax == 1:
            best_score = -inf
            for i in range(0, len(empty_locations)):
                self.board[empty_locations[i][0]][empty_locations[i][1]] = self.maxPlayer
                self.startBoardIdx = self.find_next_board((empty_locations[i][0],empty_locations[i][1]), self.startBoardIdx)
                best_score = max(self.alphabeta(depth + 1, self.startBoardIdx, alpha, beta, 0), best_score)
                alpha = max(alpha, best_score)                #alpha = max(self.alphabeta(depth + 1, currBoardIdx, alpha, beta, 0), best_score)
                self.board[empty_locations[i][0]][empty_locations[i][1]] = '_'
                if beta <= alpha:
                    break;
        elif isMax == 0:
            best_score = inf
            for i in range(0, len(empty_locations)):
                self.startBoardIdx = self.find_next_board((empty_locations[i][0],empty_locations[i][1]), self.startBoardIdx)
                self.board[empty_locations[i][0]][empty_locations[i][1]] = self.minPlayer
                best_score = min(self.alphabeta(depth + 1, self.startBoardIdx, alpha, beta, 1), best_score)
                beta = min(beta, best_score)
                self.board[empty_locations[i][0]][empty_locations[i][1]] = '_'
                if beta <= alpha:
                    break;
                     
        return best_score

    def get_empty_location(self, currBoardIdx):
        x = self.globalIdx[currBoardIdx]
        empty_locations = []
        for i in range(0, 3):
            for j in range(0, 3):
                if self.board[x[0] + i][x[1] + j] == '_':
                    empty_locations.append((x[0] + i, x[1] + j))

        return empty_locations

    def minimax(self, depth, currBoardIdx, isMax):
        
        if isMax == 1:
            best_score = -inf
        else:
            best_score = inf

        empty_locations = self.get_empty_location(currBoardIdx)

        if depth == 3:
            self.minimax_tree += 1
            return self.evaluatePredifined(isMax)

        if isMax == 1:
            best_score = -inf
            for i in range(0, len(empty_locations)):
                self.board[empty_locations[i][0]][empty_locations[i][1]] = self.maxPlayer
                self.startBoardIdx = self.find_next_board((empty_locations[i][0],empty_locations[i][1]), currBoardIdx)
                best_score = max(self.minimax(depth + 1, self.startBoardIdx, 0), best_score)
                self.board[empty_locations[i][0]][empty_locations[i][1]] = '_'
        else:
            best_score = inf
            for i in range(0, len(empty_locations)):
                self.startBoardIdx = self.find_next_board((empty_locations[i][0],empty_locations[i][1]), currBoardIdx)
                self.board[empty_locations[i][0]][empty_locations[i][1]] = self.minPlayer
                best_score = min(self.minimax(depth + 1, self.startBoardIdx, 1), best_score)
                self.board[empty_locations[i][0]][empty_locations[i][1]] = '_'

        return best_score

    def minimax_designed(self, depth, currBoardIdx, isMax):
        
        if isMax == 1:
            best_score = -inf
        else:
            best_score = inf

        empty_locations = self.get_empty_location(currBoardIdx)

        if depth == 3:
            return self.evaluateDesigned(isMax)
        #Check the winner, set utility score accordingly

        #Pseudocode retrieved from https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-3-tic-tac-toe-ai-finding-optimal-move/
        for i in range(0, len(empty_locations)):
            if isMax == 1:
                self.board[empty_locations[i][0]][empty_locations[i][1]] = self.maxPlayer
                self.startBoardIdx = self.find_next_board((empty_locations[i][0],empty_locations[i][1]), currBoardIdx)
                score = self.minimax_designed(depth + 1, self.startBoardIdx, 0)
                self.board[empty_locations[i][0]][empty_locations[i][1]] = '_'

                if score > best_score:
                    best_score = score

            if isMax == 0:
                self.startBoardIdx = self.find_next_board((empty_locations[i][0],empty_locations[i][1]), currBoardIdx)
                self.board[empty_locations[i][0]][empty_locations[i][1]] = self.minPlayer
                score = self.minimax_designed(depth + 1, self.startBoardIdx, 1)
                self.board[empty_locations[i][0]][empty_locations[i][1]] = '_'

                if score < best_score:
                    best_score = score

        return best_score

    def alphabeta_designed(self,depth,currBoardIdx,alpha,beta,isMax):
        empty_locations = self.get_empty_location(currBoardIdx)

        #if self.checkWinner() != 0:
        #    return self.checkWinner()

        if depth == 3:
            self.minimax_tree.append(self.board)
            return self.evaluateDesigned(isMax)
        #Check the winner, set utility score accordingly

        #Pseudocode retrieved from https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
        if isMax == 1:
            best_score = -inf
            for i in range(0, len(empty_locations)):
                self.board[empty_locations[i][0]][empty_locations[i][1]] = self.maxPlayer
                self.startBoardIdx = self.find_next_board((empty_locations[i][0],empty_locations[i][1]), self.startBoardIdx)
                best_score = max(self.alphabeta_designed(depth + 1, self.startBoardIdx, alpha, beta, 0), best_score)
                alpha = max(alpha, best_score)                #alpha = max(self.alphabeta(depth + 1, currBoardIdx, alpha, beta, 0), best_score)
                self.board[empty_locations[i][0]][empty_locations[i][1]] = '_'
                if beta <= alpha:
                    break;
        elif isMax == 0:
            best_score = inf
            for i in range(0, len(empty_locations)):
                self.startBoardIdx = self.find_next_board((empty_locations[i][0],empty_locations[i][1]), self.startBoardIdx)
                self.board[empty_locations[i][0]][empty_locations[i][1]] = self.minPlayer
                best_score = min(self.alphabeta_designed(depth + 1, self.startBoardIdx, alpha, beta, 1), best_score)
                beta = min(beta, best_score)
                self.board[empty_locations[i][0]][empty_locations[i][1]] = '_'
                if beta <= alpha:
                    break;
                     
        return best_score

    def find_next_board(self, coord, currBoardIdx):
        
        x = self.globalIdx[currBoardIdx]

        board = -1
        cnt = 0

        if coord == x:
            board = 0
        elif coord == (x[0], x[1] + 1):
            board = 1
        elif coord == (x[0], x[1] + 2):
            board = 2
        elif coord == (x[0] + 1, x[1]):
            board = 3
        elif coord == (x[0] + 1, x[1] + 1):
            board = 4
        elif coord == (x[0] + 1, x[1] + 2):
            board = 5
        elif coord == (x[0] + 2, x[1]):
            board = 6
        elif coord == (x[0] + 2, x[1] + 1):
            board = 7
        elif coord == (x[0] + 2, x[1] + 2):
            board = 8

        return board

    def reset_board(self):
        for i in range(0, 9):
            for j in range(0, 9):
                self.board[i][j] = '_'

    def playGamePredifinedAgent(self,maxFirst,isMinimaxOffensive,isMinimaxDefensive):
        """
        This function implements the processes of the game of predifined offensive agent vs defensive agent.
        input args:
        maxFirst(bool): boolean variable indicates whether maxPlayer or minPlayer plays first.
                        True for maxPlayer plays first, and False for minPlayer plays first.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for offensive agent.
                        True is minimax and False is alpha-beta.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for defensive agent.
                        True is minimax and False is alpha-beta.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        bestValue(list of float): list of bestValue at each move
        expandedNodes(list of int): list of expanded nodes at each move
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        
        #print(self.alphabeta(0, 0, self.winnerMinUtility, self.winnerMaxUtility, 1))
        expandedNodes = []
        bestMove=[]
        worst=[]
        bestValue=[]
        gameBoards=[]
        winner = 0

        bestmove = []

        self.initialBoardIdx = 4

        self.startBoardIdx = self.initialBoardIdx

        while self.checkWinner() == 0:
            if self.checkMovesLeft() == False:
                break
            empty_locations = self.get_empty_location(self.startBoardIdx)
            if len(empty_locations) == 0:
                break
            if maxFirst == 1:
                best_score = -inf
            else:
                best_score = inf
            for x in empty_locations:
                if maxFirst == 0:
                    self.board[x[0]][x[1]] = self.minPlayer
                    if self.checkWinner() != 0:
                        break
                    tmp = self.startBoardIdx
                    self.startBoardIdx = self.find_next_board(x, self.startBoardIdx)
                    if isMinimaxDefensive:
                        score = self.minimax(1, self.startBoardIdx, 1)
                    else:
                        score = self.alphabeta(1, self.startBoardIdx, -inf, inf, 1)
                    self.startBoardIdx = tmp
                    self.board[x[0]][x[1]] = '_'
                    if score < best_score:
                        if score < best_score:
                            bestmove.insert(0, x)
                            best_score = score
                        else:
                            bestmove.append(x)
                            best_score = score
            
            if self.checkWinner() != 0:
                winner = self.checkWinner()
                break

            tmp_idx = self.startBoardIdx

            if maxFirst == 0:
                x = bestmove[0]
                bestMove.append(x)
                bestmove.clear()
                self.board[x[0]][x[1]] = self.minPlayer
                gameBoards.append(self.board)
                bestValue.append(best_score)
                self.startBoardIdx = tmp_idx
                if self.checkWinner() != 0:
                    winner = self.checkWinner()
                    break
                self.startBoardIdx = self.find_next_board(x, self.startBoardIdx)
                maxFirst = 1

            if maxFirst == 1:
                best_score = -inf
            else:
                best_score = inf
            if self.checkMovesLeft() == False:
                break

            empty_locations = self.get_empty_location(self.startBoardIdx)
            for x in empty_locations:
               if maxFirst == 1:
                    self.board[x[0]][x[1]] = self.maxPlayer
                    if self.checkWinner() != 0:
                        winner = self.checkWinner()
                        break
                    tmp = self.startBoardIdx
                    self.startBoardIdx = self.find_next_board(x, self.startBoardIdx)
                    if isMinimaxOffensive:
                        score = self.minimax(1, self.startBoardIdx, 0)
                    else:
                        score = self.alphabeta(1, self.startBoardIdx, -inf, inf, 0)
                    self.startBoardIdx = tmp
                    self.board[x[0]][x[1]] = '_'
                    if score > best_score:
                        if score > best_score:
                            bestmove.insert(0, x)
                            best_score = score
                        else:
                            bestmove.append(x)
                            best_score = score

            if self.checkWinner() != 0:
                winner = self.checkWinner()
                break
           
            if maxFirst == 1:
                x = bestmove[0]
                bestMove.append(x)
                bestmove.clear()
                self.board[x[0]][x[1]] = self.maxPlayer
                gameBoards.append(self.board)
                bestValue.append(best_score)
                if self.checkWinner() != 0:
                    winner = self.checkWinner()
                    break
                self.startBoardIdx = self.find_next_board(x, self.startBoardIdx)
                maxFirst = 0

        self.printGameBoard()
        winner = self.checkWinner()
        if self.checkWinner() == 1:
            bestValue.append(10000)
        elif self.checkWinner() == -1:
            bestValue.append(-10000)

        expandedNodes.append(self.minimax_tree)
        self.minimax_tree = 0
        return gameBoards, bestMove, expandedNodes, bestValue, winner

    def playGameYourAgent(self):
        """
        This function implements the processes of the game of your own agent vs predifined offensive agent.
        input args:
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        gameBoards=[]
        winner=0

        maxFirst = 1
        bestmove = []

        random_board = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        whogoesfirst = [0, 1]


        self.initialBoardIdx = random.choice(random_board)
        maxFirst = random.choice(whogoesfirst)

        print(self.initialBoardIdx)
        print(maxFirst)

        self.startBoardIdx = self.initialBoardIdx

        while self.checkWinner() == 0:
            empty_locations = self.get_empty_location(self.startBoardIdx)
            if len(empty_locations) == 0:
                break
            if maxFirst == 1:
                best_score = -inf
            else:
                best_score = inf
            for x in empty_locations:
                if maxFirst == 1:
                    self.board[x[0]][x[1]] = self.maxPlayer
                    tmp = self.startBoardIdx
                    self.startBoardIdx = self.find_next_board(x, self.startBoardIdx)
                    score = self.minimax(1, self.startBoardIdx, 0)
                    self.startBoardIdx = tmp
                    self.board[x[0]][x[1]] = '_'
                    if score > best_score:
                        if score > best_score:
                            #bestmove.clear()
                            bestmove.insert(0, x)
                            best_score = score
                        else:
                            bestmove.append(x)
                            best_score = score
                    if x == empty_locations[len(empty_locations) - 1]:
                        bestmove.append(x)
            if maxFirst == 1:
                x = bestmove[0]
                bestMove.append(x)
                bestmove.clear()
                self.board[x[0]][x[1]] = self.maxPlayer
                gameBoards.append(self.board)
                if self.checkWinner() != 0:
                    winner = self.checkWinner()
                    break
                self.startBoardIdx = self.find_next_board(x, self.startBoardIdx)
                maxFirst = 0
            
            empty_locations = self.get_empty_location(self.startBoardIdx)
            for x in empty_locations:
                if maxFirst == 0:
                    self.board[x[0]][x[1]] = self.minPlayer
                    tmp = self.startBoardIdx
                    self.startBoardIdx = self.find_next_board(x, self.startBoardIdx)
                    #score = self.minimax_designed(1, self.startBoardIdx, 1)
                    score = self.alphabeta_designed(1, self.startBoardIdx, -inf, inf, 1)
                    self.startBoardIdx = tmp
                    self.board[x[0]][x[1]] = '_'
                    if score < best_score:
                        if score < best_score:
                            bestmove.insert(0, x)
                            best_score = score
                        else:
                            bestmove.append(x)
                            best_score = score
                    if x == empty_locations[len(empty_locations) - 1]:
                        bestmove.append(x)

            if maxFirst == 0:
                x = bestmove[0]
                bestMove.append(x)
                bestmove.clear()
                self.board[x[0]][x[1]] = self.minPlayer
                gameBoards.append(self.board)
                if self.checkWinner() != 0:
                    winner = self.checkWinner()
                    break
                self.startBoardIdx = self.find_next_board(x, self.startBoardIdx)
                maxFirst = 1

        self.printGameBoard()
        winner = self.checkWinner()
        if winner == 1:
            winner = -1
        elif winner == -1:
            winner = 1
        return gameBoards, bestMove, winner


    def playGameHuman(self):
        """
        This function implements the processes of the game of your own agent vs a human.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        gameBoards=[]
        winner=0

        maxFirst = 1
        bestmove = []

        random_board = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        whogoesfirst = [0, 1]


        self.initialBoardIdx = random.choice(random_board)
        maxFirst = random.choice(whogoesfirst)

        print(self.initialBoardIdx)
        print(maxFirst)

        self.startBoardIdx = self.initialBoardIdx

        while self.checkWinner() == 0:
            if self.checkMovesLeft() != True:
                break
            empty_locations = self.get_empty_location(self.startBoardIdx)
            if len(empty_locations) == 0:
                break
            if maxFirst == 1:
                best_score = -inf
            else:
                best_score = inf

            if maxFirst == 1:
                print('Choose from the following by clicking 0 .... n corresponding numbers')
                print(empty_locations)
                x = input()
                bestmove.append(empty_locations[int(x)])

                x = bestmove[0]
                bestMove.append(x)
                bestmove.clear()
                self.board[x[0]][x[1]] = self.maxPlayer
                gameBoards.append(self.board)
                if self.checkWinner() != 0:
                    winner = self.checkWinner()
                    break
                self.startBoardIdx = self.find_next_board(x, self.startBoardIdx)
                maxFirst = 0

            empty_locations = self.get_empty_location(self.startBoardIdx)
            for x in empty_locations:
                if maxFirst == 0:
                    self.board[x[0]][x[1]] = self.minPlayer
                    tmp = self.startBoardIdx
                    self.startBoardIdx = self.find_next_board(x, self.startBoardIdx)
                    #score = self.minimax_designed(1, self.startBoardIdx, 1)
                    score = self.alphabeta_designed(1, self.startBoardIdx, -inf, inf, 1)
                    self.startBoardIdx = tmp
                    self.board[x[0]][x[1]] = '_'
                    if score < best_score:
                        if score < best_score:
                            bestmove.insert(0, x)
                            best_score = score
                        else:
                            bestmove.append(x)
                            best_score = score
                    if x == empty_locations[len(empty_locations) - 1]:
                        bestmove.append(x)

            if maxFirst == 0:
                x = bestmove[0]
                bestMove.append(x)
                bestmove.clear()
                self.board[x[0]][x[1]] = self.minPlayer
                gameBoards.append(self.board)
                if self.checkWinner() != 0:
                    winner = self.checkWinner()
                    break
                self.startBoardIdx = self.find_next_board(x, self.startBoardIdx)
                maxFirst = 1
                self.printGameBoard()

        self.printGameBoard()
        winner = self.checkWinner()

        return gameBoards, bestMove, winner

if __name__=="__main__":
    uttt=ultimateTicTacToe()
    #uttt.reset_board()
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(True, True, True)
    uttt.reset_board()
    print(expandedNodes)
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(True, True, False)
    uttt.reset_board()
    print(expandedNodes)
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(False, False, True)
    uttt.reset_board()
    print(expandedNodes)
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(False, False, False)
    uttt.reset_board()
    print(expandedNodes)
    #print (uttt.evaluatePredifined(1))

    '''for x in range(0, 21):
        print(x)
        gameBoards, bestMove, winner = uttt.playGameYourAgent()
        print(bestMove)
        uttt.reset_board()
    uttt.reset_board()
    print (uttt.checkMovesLeft())'''

    #gameBoards, bestMove, winner = uttt.playGameHuman()
    #print (uttt.evaluatePredifined(1))

    if winner == 1:
        print("The winner is maxPlayer!!!")
    elif winner == -1:
        print("The winner is minPlayer!!!")
    else:
        print("Tie. No winner:(")

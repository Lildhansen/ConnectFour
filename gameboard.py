import pygame
import numpy as np


#own modules
import piece
import winCondition as wc

#constants
SENTINEL_VALUE = -1000
GAMEBOARD_WIDTH = 640
GAMEBOARD_HEIGHT = 480
MAX_PIECES = 7*6

#helper for Gameboard self.piecesInGameboardArray:
def createIntialBoard():
	intialBoard = [[0]*8 for y in range(7)]
	i = 0
	while i < 7:
		intialBoard[0][i] = SENTINEL_VALUE
		intialBoard[i][0] = SENTINEL_VALUE
		i += 1
	intialBoard[0][7] = SENTINEL_VALUE 
	return intialBoard



#the Gameboard itself which will contain all the pieces (visually and logically), as well as handling some part of the turn logic and checking win condition
class Gameboard:
	def __init__(self,redIsPlayer1,window):
		#this value counts how many pieces that is in each of the columns (1-7 columns) - (0-6 pieces in each column)
		self.columnCounter = [SENTINEL_VALUE,0,0,0,0,0,0,0]#first value is sentiel, since columns start from 1 - rest have 0 in them to begin with
		# 0 = empty 1 = red, 2 = yellow SENTINEL_VALUE = invalid Position
		self.piecesInGameboardArray = createIntialBoard
		self.pieces = []#DO NOT TOUCH - for all the pieces
		self.isRedsTurn = redIsPlayer1
		self.window = window
		self.isIntialTurn = True
		self.npPiecesInGameboardArray = []
		self.locationOfYellowOrRedPieces = []
		self.blackImage = pygame.image.load("billeder/black.png")
		self.blackImagePosition = (0,GAMEBOARD_HEIGHT)
	def displayBlackImage(self):
		self.window.blit(self.blackImage,self.blackImagePosition)
	def returnIsRedsTurn(self): #Tør ikke slette den
		return self.isRedsTurn()
	def nextTurn(self):
		self.isRedsTurn = not self.isRedsTurn
	def addToColumnCounter(self,column):
		self.columnCounter[column] += 1
	def addPieceToGameboard(self,column,isRed):
		piecesInColumn = self.columnCounter[column]
		self.piecesInGameboardArray[piecesInColumn+1][column] = 1 if isRed else 2 #add piece to code
		self.addPieceToVisualGameboard(isRed,piecesInColumn+1,column) #add piece visually
		self.columnCounter[column] += 1 
	def addPieceToVisualGameboard(self,isRed,row,column):
		self.pieces.append(piece.Piece(isRed,row,column,self.window))
	def resetGameboard(self):
		self.pieces = [] #Not sure why this doenst have to be there
		self.piecesInGameboardArray = createIntialBoard()
	def checkWinCondition(self,isRed): #only checks it for one color - the one recently placed
		self.npPiecesInGameboardArray = np.array(self.piecesInGameboardArray)
		self.locationOfYellowOrRedPieces = np.argwhere(self.npPiecesInGameboardArray == (1 if isRed else 2))
		if len(self.locationOfYellowOrRedPieces) > 3:
			numInRows = [0 for _ in range(7)] 
			numInRows[0] = SENTINEL_VALUE
			#numInRows[7] = SENTINEL_VALUE
			numInColumns = [0 for _ in range(8)]
			numInColumns[0] = SENTINEL_VALUE
			for x,y in self.locationOfYellowOrRedPieces:
				numInRows[x] += 1
				numInColumns[y] += 1
				
			winningConditions = []
			winningConditions.append(wc.checkHorizontal(numInRows,self.locationOfYellowOrRedPieces,isRed))
			winningConditions.append(wc.checkVertical(numInColumns,self.locationOfYellowOrRedPieces,isRed))	
			winningConditions.append(wc.checkDiagonal(numInRows,numInColumns,self.locationOfYellowOrRedPieces,isRed))
			for condition in winningConditions:
				if condition != None:
					return condition
			if (len(self.pieces) >= MAX_PIECES):
				return "tie"


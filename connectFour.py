#draw.rect(window,(r,g,b),(distance_bredde,distance_højde,bredde,højde) ) 

#global variable for vertical check in recursive function:
foundFourInRow = False

import pygame,time,os,sys
import numpy as np

#sizes
GAMEBOARD_WIDTH = 640
GAMEBOARD_HEIGHT = 480
COLUMN_WIDTH = 91.43
ROW_HEIGHT = 480 / 6
PIECE_RADIUS = 35

SENTINEL_VALUE = -1000 #a position out of bounds
COLUMNS = 7
ROW = 6
SENTINEL_POSITION = (1000,1000)
MAX_PIECES = 7*6

#colors
RED = (255,0,0)
YELLOW = (255,255,0)
WHITE = (255, 255, 255)
BLACK = (0,0,0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)
LIGHT_BLUE = (30,144,255)

#global variable:
running = True

#pygame stuff
pygame.init()
logo = pygame.image.load("billeder/logo.png")
pygame.display.set_icon(logo)
window = pygame.display.set_mode((GAMEBOARD_WIDTH,GAMEBOARD_HEIGHT+40)) #each column = 91,43 #højden af billedet er 480 - tilføjer 40 for at man kan se hvis tur det er
pygame.display.set_caption("Connect Four")

#måske lav disse til en del af Gameboard class
blackImage = pygame.image.load("billeder/black.png")
blackImagePosition = (0,GAMEBOARD_HEIGHT)

bg = pygame.image.load('billeder/bg.png')

#converts code positions to game positions - for rect and circle, respectively
def codePosToGamePosRect(codeY,codeX): 
	return int(GAMEBOARD_HEIGHT - codeY*ROW_HEIGHT),int((codeX-1)*COLUMN_WIDTH)

def codePosToGamePosCircle(codeY,codeX): 
	return int(GAMEBOARD_HEIGHT - codeY*ROW_HEIGHT+PIECE_RADIUS+6),int((codeX-1)*COLUMN_WIDTH + PIECE_RADIUS+11 ) #de random tal er så det passer i figuren
	
#converts game position to code position
def gamePosToCodePos(gamePos): #works only for checking what column is pressed - doesnt look at rows
	codePos = list(gamePos)
	count = 1
	if codePos[1] > GAMEBOARD_HEIGHT:
		return 0
	while codePos[0] > COLUMN_WIDTH:
		codePos[0] -= COLUMN_WIDTH
		count += 1
	return count

class Piece():
	def __init__(self,isRed,row,column):
		self.row = row
		self.column = column
		self.isRed = isRed
		#gamePosOfRow,gamePosOfColumn = codePosToGamePosRect(row,column) #possible rect
		gamePosOfRow,gamePosOfColumn = codePosToGamePosCircle(self.row,self.column)
		pygame.draw.circle(window,RED if self.isRed else YELLOW,(gamePosOfColumn,gamePosOfRow-2),PIECE_RADIUS+5) #+5 and -2 to make sure all is covered
		#pygame.draw.rect(window,RED if isRed else YELLOW,(gamePosOfColumn,gamePosOfRow,COLUMN_WIDTH,ROW_HEIGHT)) #possible rect



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

class Gameboard:
	def __init__(self,redIsPlayer1):
		#this value counts how many brikker that is in each of the columns (1-7 columns) - (0-6 pieces in each column)
		self.columnCounter = [SENTINEL_VALUE,0,0,0,0,0,0,0]#first value is sentiel, since columns start from 1 - rest have 0 in them to begin with
		# 0 = empty 1 = red, 2 = yellow SENTINEL_VALUE = invalid Position
		self.piecesInGameboardArray = createIntialBoard
		self.pieces = []#DO NOT TOUCH - for all the pieces
		self.isRedsTurn = redIsPlayer1
		self.isIntialTurn = True
		self.npPiecesInGameboardArray = []
		self.locationOfYellowOrRedPieces = []
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
		self.pieces.append(Piece(isRed,row,column))
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
			winningConditions.append(checkHorizontal(numInRows,self.locationOfYellowOrRedPieces,isRed))
			winningConditions.append(checkVertical(numInColumns,self.locationOfYellowOrRedPieces,isRed))	
			#winningConditions.append(checkDiagonalNonRecurse(numInRows,numInColumns,locationOfYellowOrRedPieces,isRed)) #den gøres nonrecurse for at se om det virker. ellers kaldes:
			winningConditions.append(checkDiagonal(numInRows,numInColumns,self.locationOfYellowOrRedPieces,isRed))
			for condition in winningConditions:
				if condition != None:
					return condition
			if (len(gameboard.pieces) == MAX_PIECES):
				return "tie"


def checkHorizontal(numInRows,locationOfYellowOrRedPieces,isRed):
	for	piecesInRow in numInRows:
		if piecesInRow > 3: #dvs der er mindst 4 på samme række:
			rowsWithMoreThan3Pieces = [i for i, x in enumerate(numInRows) if x == piecesInRow]
			for row in rowsWithMoreThan3Pieces:
				piecesInRow = []
				columnsOfPiecesInRow = []
				for piece in locationOfYellowOrRedPieces:
					if piece[0] == row:
						piecesInRow.append(piece)
				for row,column in piecesInRow:
					columnsOfPiecesInRow.append(column)
				counter = 1
				i = 0
				while i < len(columnsOfPiecesInRow)-1:
					if (columnsOfPiecesInRow[i] == columnsOfPiecesInRow[i+1]-1):
						counter += 1
					else:
						counter = 1
					i += 1
					if counter == 4:
						#game won
						return isRed

def checkVertical(numInColumns,locationOfYellowOrRedPieces,isRed):
	for piecesInColumn in numInColumns:
		if piecesInColumn > 3:
			columnsWithMoreThan3Pieces = [i for i, x in enumerate(numInColumns) if x == piecesInColumn]
			for column in columnsWithMoreThan3Pieces:
				piecesInColumns = []
				rowsOfPiecesInColumns = []
				for piece in locationOfYellowOrRedPieces:
					if piece[1] == column:
						piecesInColumns.append(piece)
				for row,column in piecesInColumns:
					rowsOfPiecesInColumns.append(row)
				counter = 1
				i = 0
				while i < len(rowsOfPiecesInColumns)-1:
					if (rowsOfPiecesInColumns[i] == rowsOfPiecesInColumns[i+1]-1):
						counter += 1	
					else:
						counter = 1
					i+=1
					if counter == 4:
						return isRed

def checkDiagonal(numInRows,numInColumns,locationOfYellowOrRedPieces,isRed):
	check = checkForAtLeast1PieceIn4ConsecutiveRowsAndColumns(numInRows,numInColumns)
	if check == None:
		return None
	global foundFourInRow
	foundFourInRow = False
	checkDiagonalRecursive(locationOfYellowOrRedPieces,locationOfYellowOrRedPieces[0],1,0,None)
	if foundFourInRow:
		return isRed


def checkForAtLeast1PieceIn4ConsecutiveRowsAndColumns(numInRows,numInColumns):
	count = 0
	for numInColumn in numInColumns: #make extra checks to prevent huge complexity
		if count == 4:
			break
		if numInColumn == SENTINEL_VALUE:
			continue
		if numInColumn > 0:
			count += 1
		else:
			count = 0
	print(count)
	if count < 4:
		return None
	count = 0
	for numInRow in numInRows:
		if count == 4:
			break
		if numInRow == SENTINEL_VALUE:
			continue
		if numInRow > 0:
			count += 1
		else:
			count = 0
	if count < 4:
		return None
	return True
	
def checkDiagonalRecursive(allPieceLocations,pieceLocation,numFoundInARow,startingPieceIndex,direction):
	global foundFourInRow
	if (foundFourInRow):
		return True

	if numFoundInARow == 4:
		foundFourInRow = True


	if (direction == "NW" or direction == None) and ([pieceLocation[0]+1,pieceLocation[1]-1] in allPieceLocations.tolist()): 
		print("NW")
		checkDiagonalRecursive(allPieceLocations,[pieceLocation[0]+1,pieceLocation[1]-1],numFoundInARow+1,startingPieceIndex,"NW")
	#NE
	if (direction == "NE" or direction == None) and ([pieceLocation[0]+1,pieceLocation[1]+1] in allPieceLocations.tolist()): 
		print("NE")
		checkDiagonalRecursive(allPieceLocations,[pieceLocation[0]+1,pieceLocation[1]+1],numFoundInARow+1,startingPieceIndex,"NE")
	#SW
	if (direction == "SW" or direction == None) and [pieceLocation[0]-1,pieceLocation[1]-1] in allPieceLocations.tolist(): 
		checkDiagonalRecursive(allPieceLocations,[pieceLocation[0]-1,pieceLocation[1]-1],numFoundInARow+1,startingPieceIndex,"SW")
	#SE
	if (direction == "SE" or direction == None) and [pieceLocation[0]-1,pieceLocation[1]+1] in allPieceLocations.tolist(): 
		checkDiagonalRecursive(allPieceLocations,[pieceLocation[0]-1,pieceLocation[1]+1],numFoundInARow+1,startingPieceIndex,"SE")
	
	if direction == None:
		nextPieceIndex = allPieceLocations.tolist().index(allPieceLocations.tolist()[startingPieceIndex])+1
		print("-------------next piece------------------")
		print(allPieceLocations[nextPieceIndex])
		print("-------------------------------")

		if nextPieceIndex+1 == len(allPieceLocations):
			print(nextPieceIndex)
			print("stop")
			return False
		checkDiagonalRecursive(allPieceLocations,allPieceLocations[nextPieceIndex],1,nextPieceIndex,None)



#gameboard = Gameboard() 
#21 af hver - lav alle brikkerne på forhånd i lister - kombiner med columnIsNotFull()

class radioButtonPlayerText():
	def __init__(self,color,text,x,y):
		self.textString = text
		self.color = color
		self.x = x
		self.y = y
		self.font = pygame.font.Font('freesansbold.ttf', 25)
		self.text = self.font.render(text, True, self.color, LIGHT_BLUE)
		print(self.color)
		self.textRect = self.text.get_rect()
		self.textRect.center = (x,y)
	def changeColor(self,yellowIsActivated):
		if yellowIsActivated:
			self.color = YELLOW
		else:
			self.color = RED
		self.text = self.font.render(self.textString, True, self.color, LIGHT_BLUE)
class radioButtonColorText():
	def __init__(self,color,text,x,y):
		self.color = color
		self.x = x
		self.y = y
		self.font = pygame.font.Font('freesansbold.ttf', 20)
		self.text = self.font.render(text, True, self.color, LIGHT_BLUE)
		self.textRect = self.text.get_rect()
		self.textRect.center = (x,y)

class RadioButton():
	def __init__(self,isActivated,color,forPlayerOne,x,y):
		self.isActivated = isActivated
		self.hasBeenActivated = False
		self.color = color
		self.forPlayerOne = forPlayerOne
		self.x = x
		self.y = y
		self.button = None
		self.innerButton = None
		self.innerButtonCenter = None
	def showButton(self):
		self.button = pygame.draw.circle(window,WHITE,(self.x,self.y),15)
		self.innerButtonCenter = self.button.center
	def interactButton(self,activate):
		if activate:
			self.innerButton = pygame.draw.circle(window,self.color,(self.innerButtonCenter),10)
		else:
			self.innerButton = pygame.draw.circle(window,BLACK,SENTINEL_POSITION,10)
	def checkForCollision(self,position):
		if self.button.collidepoint(position):
			return True

#player doesnt have their correct image. also whose turn is it anyways is fucked
class PlayerTurnDisplay: #create 2 instances - with each color, and make the other one invisible/have white color when not their turn / change its position to out of bounds
	def __init__(self,isRed,player):
		self.textbox = pygame.draw.rect(window,(0,0,0),(0,480,640,40))
		self.playerText = pygame.image.load(f"billeder/playerTurn/{str(player)}_{'red' if isRed else 'yellow'}.png")
		self.playerWonText = pygame.image.load(f"billeder/smallPlayerWon/{str(player)}_{'red' if isRed else 'yellow'}.png")
		self.playerWonTextFinal = pygame.image.load(f"billeder/playerWon/{str(player)}_{'red' if isRed else 'yellow'}.png")
		self.player = player
		self.isRed = isRed
		self.position = (GAMEBOARD_WIDTH/2-160/2,GAMEBOARD_HEIGHT) #160 is the width of the image
	def whoseTurnIsItAnyway(self,redsTurn):
		if (redsTurn and self.isRed) or (not redsTurn and not self.isRed):
			self.displayWhoseTurn(self.position)
		else:
			self.displayWhoseTurn(SENTINEL_POSITION)
	def displayWhoseTurn(self,position): #sentinel position if not active - otherwise defined position #must be tuple or list of position x,y
		#denne funktion skal kaldes af en anden funktion
		window.blit(self.playerText,position)
	def removeDisplayWhoseTurn(self,position):
		window.blit(self.playerText,position) # 
		

player1RadioButton = radioButtonPlayerText(YELLOW,"Player 1:",75,240)
player2RadioButton = radioButtonPlayerText(RED,"Player 2:",75,310)
yellowRadioButton = radioButtonPlayerText(YELLOW,"Yellow:",160,200)
redRadioButton = radioButtonPlayerText(RED,"Red:",250,200)

yellowRadioButtons = [RadioButton(True,YELLOW,True,150,240),RadioButton(False,YELLOW,False,150,310)]
redRadioButtons = [RadioButton(False,RED,True,240,240),RadioButton(True,RED,False,240,310)]

def doPlayerTurn(columnToPlacePiece,isRed):
	gameboard.addPieceToGameboard(column,isRed)
	if len(gameboard.pieces) != 0:
		gameboard.isIntialTurn = False
	endGameState = gameboard.checkWinCondition(isRed) #a is used so we can get back to the main loop
	if endGameState != None:
		return endGameState
	else:
		nextPlayersTurn()


def nextPlayersTurn():
	gameboard.nextTurn()
	if gameboard.isRedsTurn:
		if player1Turn.isRed:
			player1Turn.whoseTurnIsItAnyway(True)
		else:
			player2Turn.whoseTurnIsItAnyway(True)
	else:
		if not player1Turn.isRed:
			player1Turn.whoseTurnIsItAnyway(False)
		else:
			player2Turn.whoseTurnIsItAnyway(False)


def findPlayerWhoWonBasedOnIfHeIsRedOrNot(isRed):
	if player1Turn.isRed == isRed:
		return player1Turn
	else:
		return player2Turn


def validColumnSelected(column):
	return bool(column)

def columnNotFull(column):
	if gameboard.columnCounter[column] < 6:
		return True
	return False


def drawGamePreEndScreen():
	mouseClicked = False
	drawImage = pygame.image.load("billeder/smallPlayerWon/draw.PNG")
	waitInputImage = pygame.image.load("billeder/waitInput/noBackGround.PNG")
	drawImagePosition = (GAMEBOARD_WIDTH/2-160/2,GAMEBOARD_HEIGHT) #160 is the width of the image
	waitInputPosition = (GAMEBOARD_WIDTH/2-444/2,GAMEBOARD_HEIGHT/2-159/2) #444x159
	while not mouseClicked:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				mouseClicked = True
		window.blit(drawImage,drawImagePosition)
		window.blit(waitInputImage,waitInputPosition)
		pygame.display.update()

def preEndScreen(whoWonIsRed):
	mouseClicked = False
	waitInputImage = pygame.image.load("billeder/waitInput/noBackGround.PNG")
	wonImagePosition = (GAMEBOARD_WIDTH/2-160/2,GAMEBOARD_HEIGHT) #160 is the width of the image
	waitInputPosition = (GAMEBOARD_WIDTH/2-444/2,GAMEBOARD_HEIGHT/2-159/2) #
	if whoWonIsRed:
		if player1Turn.isRed:
			wonImage = player1Turn.playerWonText
		else:
			wonImage = player2Turn.playerWonText
	else:
		if not player1Turn.isRed:
			wonImage = player1Turn.playerWonText
		else:
			wonImage = player2Turn.playerWonText
	while not mouseClicked:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				mouseClicked = True
		window.blit(wonImage,wonImagePosition)
		window.blit(waitInputImage,waitInputPosition)
		pygame.display.update()

#DOESNT WORK
def blinkImage(imageLocation,imageWidth):
	gameProceeded = False
	isBlinking = False
	clock = pygame.time.Clock()
	image = pygame.image.load(imageLocation)
	position = (GAMEBOARD_WIDTH/2-imageWidth/2,GAMEBOARD_HEIGHT/2) #444 is the width of the image
	
	while not gameProceeded:
		clock.tick(10)
		if isBlinking:
			window.blit(image,SENTINEL_POSITION)
			isBlinking = False
		isBlinking = True 
		pygame.display.update()

		#whatWillBeDisplayed = []
		#whatWillBeDisplayed.append(window.blit(image,position))
		#pygame.time.delay(500)
		#pygame.display.update(whatWillBeDisplayed)
		#window.blit(image,SENTINEL_POSITION)
		#whatWillBeDisplayed.clear()
		#pygame.display.update()
		for event in pygame.event.get(): 
			if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				gameProceeded = True
				break
			if event.type == pygame.QUIT:
				pygame.quit()
		print(gameProceeded)
		clock.tick(10)
	print("stop")

class StartGameButton:
	def __init__(self):
		self.font = pygame.font.Font('freesansbold.ttf', 80)
		self.text = self.font.render('Start Game', True, RED, BLUE)
		self.textRect = self.text.get_rect()
		self.textRect.center = (GAMEBOARD_WIDTH/2,GAMEBOARD_HEIGHT/2-120)
	def checkForCollision(self,position):
		if self.textRect.collidepoint(position):
			return True

startGameButton = StartGameButton()

class ExitGameButton:
	def __init__(self):
		self.font = pygame.font.Font('freesansbold.ttf', 80)
		self.text = self.font.render('Exit Game', True, RED, BLUE)
		self.textRect = self.text.get_rect()
		self.textRect.center = (GAMEBOARD_WIDTH/2,GAMEBOARD_HEIGHT/2+200)
	def checkForCollision(self,position):
		if self.textRect.collidepoint(position):
			return True

exitGameButton = ExitGameButton()

def fixRadioButtons():
	if yellowRadioButtons[0].hasBeenActivated:
		yellowRadioButtons[0].hasBeenActivated = False
		yellowRadioButtons[0].isActivated = True
		yellowRadioButtons[1].isActivated = False
		redRadioButtons[0].isActivated = False
		redRadioButtons[1].isActivated = True
		
	elif yellowRadioButtons[1].hasBeenActivated:
		yellowRadioButtons[1].hasBeenActivated = False
		yellowRadioButtons[1].isActivated = True
		yellowRadioButtons[0].isActivated = False
		redRadioButtons[1].isActivated = False
		redRadioButtons[0].isActivated = True
		
	elif redRadioButtons[0].hasBeenActivated:
		redRadioButtons[0].hasBeenActivated = False
		redRadioButtons[0].isActivated = True
		redRadioButtons[1].isActivated = False
		yellowRadioButtons[0].isActivated = False
		yellowRadioButtons[1].isActivated = True
		
	elif redRadioButtons[1].hasBeenActivated:
		redRadioButtons[1].hasBeenActivated = False
		redRadioButtons[1].isActivated = True
		redRadioButtons[0].isActivated = False
		yellowRadioButtons[1].isActivated = False
		yellowRadioButtons[0].isActivated = True
	else:
		return
		
def fixRadioButtonsVisually():
	i = 0
	while i < 2:
		yellowRadioButtons[i].interactButton(yellowRadioButtons[i].isActivated)
		redRadioButtons[i].interactButton(redRadioButtons[i].isActivated)
		i += 1
	player1RadioButton.changeColor(yellowRadioButtons[0].isActivated)
	player2RadioButton.changeColor(redRadioButtons[0].isActivated)
	#called in a loop to make sure only 1 player has 1 of the colors
	#also fixes the player-name to be that colour

	def __init__(self):
		self.font = pygame.font.Font('freesansbold.ttf', 80)
		self.text = self.font.render('Exit Game', False, RED, BLUE)
		self.textRect = self.text.get_rect()
		self.textRect.center = (GAMEBOARD_WIDTH/2,GAMEBOARD_HEIGHT/2+200)
	def checkForCollision(self,position):
		if self.textRect.collidepoint(position):
			return True

def prepareMainGame():
	global gameboard
	gameboard = Gameboard(True if player1RadioButton.color == RED else False)
	gameboard.isIntialTurn = True
	global player1Turn
	player1Turn = PlayerTurnDisplay(True if player1RadioButton.color == RED else False,1) #player 1
	global player2Turn
	player2Turn = PlayerTurnDisplay(True if player2RadioButton.color == RED else False,2)# player 2
	gameboard.pieces = []
	gameboard.resetGameboard()

#yellowRadioButtons = [RadioButton(True,YELLOW,True),RadioButton(False,YELLOW,False)]
#redRadioButtons = [RadioButton(False,RED,True),RadioButton(True,RED,False)]
#radioButtons = RadioButtons()

#i hovedmenuen skal der være en vælg farve. måske noget ala radio buttons
	#de skal have default værdi
	#deres navn (player x) skal skifte til den farve de vælger
	#måske tilføj senere at de kan vælge mellem 5 farver
	#også tilføj at de kan vælge navn
#der skal være en quit
#prøv med pygame text
def mainMenu():
	running = True
	hasStarted = False
	while running:
		window.fill(LIGHT_BLUE)
		#exit + start
		window.blit(startGameButton.text,startGameButton.textRect)
		window.blit(exitGameButton.text,exitGameButton.textRect)
		#Buttons:
		yellowRadioButtons[0].showButton()
		yellowRadioButtons[1].showButton()
		redRadioButtons[0].showButton()
		redRadioButtons[1].showButton()
		fixRadioButtons()
		fixRadioButtonsVisually()
		#buttonText
		window.blit(player1RadioButton.text,player1RadioButton.textRect)
		window.blit(player2RadioButton.text,player2RadioButton.textRect)
		window.blit(yellowRadioButton.text,yellowRadioButton.textRect)
		window.blit(redRadioButton.text,redRadioButton.textRect)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				if exitGameButton.checkForCollision(pygame.mouse.get_pos()):
					running = False
				if startGameButton.checkForCollision(pygame.mouse.get_pos()):
					running = False 
					hasStarted = True	
				if yellowRadioButtons[0].checkForCollision(pygame.mouse.get_pos()):
					yellowRadioButtons[0].hasBeenActivated = True
				elif yellowRadioButtons[1].checkForCollision(pygame.mouse.get_pos()):
					yellowRadioButtons[1].hasBeenActivated = True
				elif redRadioButtons[0].checkForCollision(pygame.mouse.get_pos()):
					redRadioButtons[0].hasBeenActivated = True
				elif redRadioButtons[1].checkForCollision(pygame.mouse.get_pos()):
					redRadioButtons[1].hasBeenActivated = True
		pygame.display.update()
	if hasStarted:
		prepareMainGame()
		mainGame()

def endScreen(whoWonIsRed,endScreenRunning):
	hasExited = False
	playerWhoWon = findPlayerWhoWonBasedOnIfHeIsRedOrNot(gameboard.isRedsTurn) #whoevers turn it is, is the one who won
	while endScreenRunning:
		window.fill((0,0,0))
		pygame.draw.rect(window,(0,0,0),(0,0,GAMEBOARD_WIDTH,GAMEBOARD_HEIGHT+40))
		if whoWonIsRed == "tie":
			print("TIE")
			window.blit(pygame.image.load("billeder/playerWon/draw.png"),(25,130))
		else:
			window.blit(playerWhoWon.playerWonTextFinal,(0,0)) 
		for event in pygame.event.get():
			if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or (event.type == pygame.MOUSEBUTTONUP and event.button == 1):
				endScreenRunning = False
			if event.type == pygame.QUIT:
				endScreenRunning = False
				hasExited = True
		pygame.display.update()
	if not hasExited:
		mainMenu()
	else:
		print("here")

def mainGame():
	window.fill(WHITE)
	running = True
	while running:
		window.blit(bg,[0,0])
		if gameboard.isIntialTurn:
			window.blit(blackImage,blackImagePosition)
			player1Turn.displayWhoseTurn((GAMEBOARD_WIDTH/2-160/2,GAMEBOARD_HEIGHT))
		for event in pygame.event.get(): 
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				clickedPos = pygame.mouse.get_pos()	
				global column
				column = gamePosToCodePos(clickedPos)
				#time.sleep(0.1)	
				if (validColumnSelected(column) and columnNotFull(column)):
					endGameState = doPlayerTurn(column,gameboard.isRedsTurn)
					if endGameState != None:
						running = False
						pygame.display.update()
						if endGameState == "tie":
							drawGamePreEndScreen()
						else:
							preEndScreen(endGameState)
		pygame.display.update()
	endScreen(endGameState, True)
	
mainMenu()
pygame.quit()

#to do:
"""
Flyt i flere filer
fjern prints og ligegyldige kommentarer
tilføj kommentarer(måske)
"""
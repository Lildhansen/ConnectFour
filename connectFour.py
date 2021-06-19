#draw.rect(window,(r,g,b),(distance_bredde,distance_højde,bredde,højde) ) 

#not sure what im doing - but it works. for vertical check:
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
SENTINEL_POSITION = (100,100)
MAX_PIECES = 7*6

#colors
RED = (255,0,0)
YELLOW = (255,255,0)

#global variable:
running = True
itemsOnScreen=[]

pygame.init()
logo = pygame.image.load("billeder/logo.png")
pygame.display.set_icon(logo)
window = pygame.display.set_mode((GAMEBOARD_WIDTH,GAMEBOARD_HEIGHT+40)) #each column = 91,43 #højden af billedet er 480 - tilføjer 40 for at man kan se hvis tur det er
pygame.display.set_caption("Connect Four")

bg = pygame.image.load('billeder/bg.png')
itemsOnScreen.append(bg)

#takes x,y returns x,y
def codePosToGamePosRect(codeY,codeX): 
	return int(GAMEBOARD_HEIGHT - codeY*ROW_HEIGHT),int((codeX-1)*COLUMN_WIDTH)

def codePosToGamePosCircle(codeY,codeX): 
	return int(GAMEBOARD_HEIGHT - codeY*ROW_HEIGHT+PIECE_RADIUS+6),int((codeX-1)*COLUMN_WIDTH + PIECE_RADIUS+11 ) #de random tal er så det passer i figuren
	

def gamePosToCodePos(gamePos): #works only for checking what column is pressed - doesnt look at rows
	codePos = list(gamePos)
	count = 1
	if codePos[1] > GAMEBOARD_HEIGHT:
		return 0
	while codePos[0] > COLUMN_WIDTH:
		codePos[0] -= COLUMN_WIDTH
		count += 1
	return count


def drawBoard(): #draws the squares of the board
	columns = []
	#topOfColumn = []
	for i in range(7):
		columns.append(pygame.draw.rect(window,(255,255,255),(i*COLUMN_WIDTH,0,COLUMN_WIDTH,480))) 
		#topOfColumn.append(pygame.draw.rect(window,(255,0,0),(i*COLUMN_WIDTH,0,COLUMN_WIDTH-10,5))) #-10 to make sure it doesnt overlap with next column
	return columns
hitboxes = drawBoard()


class Piece():
	def __init__(self,isRed,row,column):
		self.row = row
		self.column = column
		self.isRed = isRed
		#gamePosOfRow,gamePosOfColumn = codePosToGamePosRect(row,column)
		gamePosOfRow,gamePosOfColumn = codePosToGamePosCircle(self.row,self.column)
		#print(gamePosOfRow)
		#print(gamePosOfColumn)
		pygame.draw.circle(window,RED if self.isRed else YELLOW,(gamePosOfColumn,gamePosOfRow-2),PIECE_RADIUS+5) #+5 and -2 to make sure all is covered
		#pygame.draw.rect(window,RED if isRed else YELLOW,(gamePosOfColumn,gamePosOfRow,COLUMN_WIDTH,ROW_HEIGHT)) #lav cirkler i stedet?



#helper for Gameboard self.piecesInGameboardArray:
a = [[0]*8 for y in range(7)]
i = 0
while i < 7:
	a[0][i] = SENTINEL_VALUE
	a[i][0] = SENTINEL_VALUE
	i += 1
a[0][7] = SENTINEL_VALUE 

class Gameboard:
	def __init__(self):
		#this value counts how many brikker that is in each of the columns (1-7 columns) - (0-6 pieces in each column)
		self.columnCounter = [SENTINEL_VALUE,0,0,0,0,0,0,0]#first value is sentiel, since columns start from 1 - rest have 0 in them to begin with
		# 0 = empty 1 = red, 2 = yellow SENTINEL_VALUE = invalid Position
		self.piecesInGameboardArray = a
		self.pieces = []#DO NOT TOUCH - for all the pieces
		self.isRedsTurn = True #maybe not always
		self.isIntialTurn = True
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
		#print(self.piecesInGameboardArray)
	def addPieceToVisualGameboard(self,isRed,row,column):
		self.pieces.append(Piece(isRed,row,column))
	def checkWinCondition(self,isRed): #only checks it for one color - the one recently placed
		npPiecesInGameboardArray = np.array(self.piecesInGameboardArray)
		locationOfYellowOrRedPieces = np.argwhere(npPiecesInGameboardArray == (1 if isRed else 2))
		#print(locationOfYellowOrRedPieces)
		#print(locationOfYellowOrRedPieces[0][0])
		if len(locationOfYellowOrRedPieces) > 3:
			numInRows = [0 for _ in range(7)] 
			numInRows[0] = SENTINEL_VALUE
			#numInRows[7] = SENTINEL_VALUE
			numInColumns = [0 for _ in range(8)]
			numInColumns[0] = SENTINEL_VALUE
			for x,y in locationOfYellowOrRedPieces:
				#print(numInColumns[x])
				numInRows[x] += 1
				numInColumns[y] += 1
				
			#print(f"column: {numInColumns}")
			#print(f"row: {numInRows}")
			winningConditions = []
			winningConditions.append(checkHorizontal(numInRows,locationOfYellowOrRedPieces,isRed))
			winningConditions.append(checkVertical(numInColumns,locationOfYellowOrRedPieces,isRed))	
			#winningConditions.append(checkDiagonalNonRecurse(numInRows,numInColumns,locationOfYellowOrRedPieces,isRed)) #den gøres nonrecurse for at se om det virker. ellers kaldes:
			winningConditions.append(checkDiagonal(numInRows,numInColumns,locationOfYellowOrRedPieces,isRed))
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
					#print(f" numnum: {locationOfYellowOrRedPieces}")
					if piece[0] == row:
						#print(f"piece: {piece}, piece[0]: {piece[0]}")
						piecesInRow.append(piece)
				for row,column in piecesInRow:
					columnsOfPiecesInRow.append(column)
				counter = 1
				i = 0
				while i < len(columnsOfPiecesInRow)-1:
					#print(f"i: {columnsOfPiecesInRow[i]}, i+1: {columnsOfPiecesInRow[i+1]-1}")
					if (columnsOfPiecesInRow[i] == columnsOfPiecesInRow[i+1]-1):
						counter += 1
					else:
						counter = 1
					i += 1
					#print(f"counter: {counter}")
					if counter == 4:
						#game won
						return isRed
def checkVertical(numInColumns,locationOfYellowOrRedPieces,isRed):
	for piecesInColumn in numInColumns:
		if piecesInColumn > 3:
			columnsWithMoreThan3Pieces = [i for i, x in enumerate(numInColumns) if x == piecesInColumn]
			##print(f"col: {columnsWithMoreThan3Pieces}")
			for column in columnsWithMoreThan3Pieces:
				piecesInColumns = []
				rowsOfPiecesInColumns = []
				for piece in locationOfYellowOrRedPieces:
					if piece[1] == column:
						piecesInColumns.append(piece)
				for row,column in piecesInColumns:
					rowsOfPiecesInColumns.append(row)
				#print(piecesInColumns, rowsOfPiecesInColumns)
				counter = 1
				i = 0
				while i < len(rowsOfPiecesInColumns)-1:
					##print(f"counter {counter}")
					if (rowsOfPiecesInColumns[i] == rowsOfPiecesInColumns[i+1]-1):
						counter += 1	
					else:
						counter = 1
					i+=1
					if counter == 4:
						##print(f"ENd {isRed}")
						return isRed

def checkDiagonalNonRecurse(numInRows,numInColumns,locationOfYellowOrRedPieces,isRed):
	check = checkForAtLeast1PieceIn4ConsecutiveRowsAndColumns(numInRows,numInColumns)
	if check == None:
		return None
	if actuallyCheckDiagonalNonRecurse(locationOfYellowOrRedPieces,locationOfYellowOrRedPieces[0]):
		return isRed

#allPieceLocations er kun for den farve den får
def actuallyCheckDiagonalNonRecurse(allPieceLocations,pieceLocation):
	for piece in allPieceLocations:
		#de 4 if checks som i recurse func
		pass

def checkDiagonal(numInRows,numInColumns,locationOfYellowOrRedPieces,isRed):
	#print(numInColumns)
	print(locationOfYellowOrRedPieces)
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
	
#er problemet måske at når vi kigger i en retning og kalder funktionen - vil vi næste iteration igen kigge i alle retning.
#Og det kan give infinite loops fordi når vi når enden kan vi bare gå tilbage igen. eller andre steder hen
#For hver retning kan laves en string der siger hvilken vej, og så skal den have den string for at gå den vej.
def checkDiagonalRecursive(allPieceLocations,pieceLocation,numFoundInARow,startingPieceIndex,direction):
	#validWidthValues = [_ for x in range(1,8)] #pieceLocation[0]+1 in validHeightValues and pieceLocation[1]-1 in validWidthValues
	#validHeightValues = [_ for x in range(1,7)]
	global foundFourInRow
	if (foundFourInRow):
		return True #PLZ FUCKING STOP DIN SATANS REKURSIVE FUNKTION
	print("-------------found 4 inarow------------------")
	print(foundFourInRow)
	print("--------------------------------------------")
	if numFoundInARow == 4:
		foundFourInRow = True #FORSØG PÅ AT LORTET STOPPER
	#NW
	#print("-------------first piece------------------")
	#print(pieceLocation)
	#print("--------------------------------------------")
	print("-------------num in row------------------")
	print(numFoundInARow)
	print("--------------------------------------------")
	#mulige problemer:
		#Tjek om den bevæger sig rigtigt NW,NE osv.
		#Tjek om den går til næste brik hvis den ikke kan gå nogle vegne
		#få shortcircuitet når den er færdig. lav en variabel som der tjekkes efter i øverst af funktionen og tag den med igennem funktionen
		#Hmm, hvis bare der er 4 på stribe virker den faktisk. det er kun hvis den ikke kan finde det.
			#derfor skal den afsluttes ordentligt
	#NW	
	print("---------------------------")
	#print(f"WHY DOES THIS {[pieceLocation[0]+1,pieceLocation[1]-1]} EQUAL THIS??? {list(allPieceLocations)}")
	#print([pieceLocation[0]+1,pieceLocation[1]-1] in list(allPieceLocations))
	print("---------------------------")


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
	#check if checked piece is last piece
	#print(f"{pieceLocation} == {allPieceLocations[-1]}")
	#if (pieceLocation[0] == allPieceLocations[-1][0] and pieceLocation[1] == allPieceLocations[-1][1]):
	#	return False
	#calls for next piece if no piece in 4 corners
	#print(list(allPieceLocations))
	#print(list(allPieceLocations).index(pieceLocation)+1)
	
	if direction == None:
		nextPieceIndex = allPieceLocations.tolist().index(allPieceLocations.tolist()[startingPieceIndex])+1
		print("-------------next piece------------------")
		print(allPieceLocations[nextPieceIndex])
		print("-------------------------------")

		if nextPieceIndex+1 == len(allPieceLocations):
			print(nextPieceIndex)
			print("stop")
			return False

	#print(f"NPI: {nextPieceIndex}")
		checkDiagonalRecursive(allPieceLocations,allPieceLocations[nextPieceIndex],1,nextPieceIndex,None)



gameboard = Gameboard()
#21 af hver - lav alle brikkerne på forhånd i lister - kombiner med columnIsNotFull()



class PlayerTurnDisplay: #create 2 instances - with each color, and make the other one invisible/have white color when not their turn / change its position to out of bounds
	def __init__(self,isRed,player):
		self.textbox = pygame.draw.rect(window,(0,0,0),(0,480,640,40))
		self.playerText = pygame.image.load(f"billeder/playerTurn/{str(player)}_{'red' if isRed else 'yellow'}.png")
		self.isRed = isRed
		self.player = player
		self.position = (GAMEBOARD_WIDTH/2-160/2,GAMEBOARD_HEIGHT) #160 is the width of the image
	def whoseTurnIsItAnyway(self,redsTurn):
		if (redsTurn and self.isRed) or (not redsTurn and not self.isRed):
			#print(f"{self.isRed} --------- {redsTurn}")
			self.displayWhoseTurn(self.position)
		else:
			self.displayWhoseTurn(SENTINEL_POSITION)
	def displayWhoseTurn(self,position): #sentinel position if not active - otherwise defined position #must be tuple or list of position x,y
		#denne funktion skal kaldes af en anden funktion
		window.blit(self.playerText,position)
	def removeDisplayWhoseTurn(self,position):
		window.blit(self.playerText,position) # 
		
playerRedTurn = PlayerTurnDisplay(True,1)
playerYellowTurn = PlayerTurnDisplay(False,2)

def columnOfMouseclick(): #returns false if it is an invalid position - else return the column of which it is. (starting at 0)
	for index,hitbox in enumerate(hitboxes):
		if hitbox.collidepoint(pos):
			return index
	return False

def doPlayerTurn(columnToPlacePiece,isRed):
	gameboard.addPieceToGameboard(column,isRed)
	if len(gameboard.pieces) != 0:
		gameboard.isIntialTurn = False
	a = gameboard.checkWinCondition(isRed) #a is used so we can get back to the main loop
	if a != None:
		return a
	else:
		nextPlayersTurn()


def nextPlayersTurn():
	gameboard.nextTurn()
	if gameboard.isRedsTurn:
		playerRedTurn.whoseTurnIsItAnyway(True)
	else:
		playerYellowTurn.whoseTurnIsItAnyway(False)




def validColumnSelected(column):
	return bool(column)

def columnNotFull(column):
	if gameboard.columnCounter[column] < 6:
		return True
	return False


def tieGamePreEndScreen():
	blinkImage("billeder/waitInput/ClickToProceed.PNG",444)
	pass
def preEndScreen(whoWonIsRed):
	blinkImage("billeder/waitInput/ClickToProceed.PNG",444)

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
			if event.type == pygame.MOUSEBUTTONUP:
				gameProceeded = True
				break
			if event.type == pygame.QUIT:
				pygame.quit()
		print(gameProceeded)
		clock.tick(10)
	print("stop")
	
	


#prøv og lav main menu. se hvordan det virker
def mainMenu():
	print("hello")
	#pygame.quit()

def endScreen(whoWonIsRed,endScreenRunning):#whoWonIsRed is a boolean -----except if it was a tied game
	while endScreenRunning:
		if whoWonIsRed == "tie":
			print("TIE")
			winScreen = pygame.image.load("billeder/playerWon/draw.png")
		elif whoWonIsRed == True:
			print("red")
			winScreen = pygame.image.load("billeder/playerWon/1_red.png")
		else:
			print("yellow")
			winScreen = pygame.image.load("billeder/playerWon/2_yellow.png")
		window.fill((0,0,0))
		pygame.draw.rect(window,(0,0,0),(0,0,GAMEBOARD_WIDTH,GAMEBOARD_HEIGHT+40))
		window.blit(winScreen,(0,0)) 
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					mainGame()
			if event.type == pygame.QUIT:
				endScreenRunning = False
		pygame.display.update()
	mainMenu()
#column = ""

def mainGame():
	running = True
	while running:
		window.blit(bg,[0,0])
		#playerYellowTurn.displayWhoseTurn((640/2-(160/2),480)) #for debugging purpose - tjek dog størrelser - især find en måde at se størrelse på billede med pygame
		if gameboard.isIntialTurn:
			playerRedTurn.displayWhoseTurn((GAMEBOARD_WIDTH/2-160/2,GAMEBOARD_HEIGHT))
		for event in pygame.event.get(): 
			if event.type == pygame.QUIT:
				#pygame.display.quit()
				#pygame.quit()
				running = False
			if event.type == pygame.MOUSEBUTTONUP:
				blinkImage("billeder/waitInput/ClickToProceed.PNG",444) #slet igen
				clickedPos = pygame.mouse.get_pos()
				#print(clickedPos)
				global column
				column = gamePosToCodePos(clickedPos)
				time.sleep(0.1)	
				if (validColumnSelected(column) and columnNotFull(column)):
					a = doPlayerTurn(column,gameboard.isRedsTurn)
					if a != None:
						pygame.display.update()
						if a == "tie":
							tieGamePreEndScreen()
							endScreen(a,True)
						time.sleep(1) #burde nok skrive hvem der vandt her i stedet ... , eller i hvert fald gøre så der kan klikke spå en tast for at gå videre
						running = False
						preEndScreen(a)
						endScreen(a, True)
						#running = False
				#pos = pygame.mouse.get_pos()
				#clickedColumn = columnOfMouseclick()
				#x = columnIsNotFull(clickedColumn)
				#if clickedColumn and x:
				#	addPiece()
		pygame.display.update()

#a,b = mainGame()
#a,b = True,True
#endScreen(a,b)

mainGame()
pygame.quit()


#to do:
	#main menu
		#vælg farve
	#end screen skal ikke ske lige med det samme - først skal der stå med småt nede under brættet (så skal der stå press any button to continue på skærmen
	#hvis alle brikker er sat uden nogle vindere er den uafgjort
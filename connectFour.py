#take from chess.py (backup) - so splite the board into 7 parts and look for where the mouse is clicked and not collision
# Make an array/dictionary/object (class) - probably class, to keep track of how many pieces are in each column.
# make function to add to column - that takes which column (starting from 1) as parameter (0 is invalid)
# When 1 column is full make it so you cant put any more pieces in


#make function to check for 4 connected
	#i stedet for at checke på alle led, skal den efter hver tur, finde alle af den farve (enten 1 eller 0'er), og se om de er 4 på stribe
	#den skal return den position i multidimensionelt array hvor enten 1-tallerne eller 0-tallerne er	

	#ellers skulle alle måde der kan tjekkes 4 på stribe kigges igennem.



#to do:
#addPiece() function
#make window taller, make room for "player x turn" - in blue if he is blue and red if not (or whatever the colors are)
#create the turn based thingy - maybe with a boolean when a valid option is chosen
#check for win
#lav en draw.rect i det øverste hul for alle kolonner (måske kun gør den halv højde, for at være sikker på den under ikke rammer den, 
	#så man kan tjekke collision med brikkerne, og hvis den collider, låses den kolonne

#alternativt - lav det gamle chess hitbox med position i stedet for collision, hvis nu brikkerne dækker over collisionen (det gør de ikke)

#draw.rect(window,(r,g,b),(distance_bredde,distance_højde,bredde,højde) ) 

import pygame,time

#sizes
GAMEBOARD_WIDTH = 640
GAMEBOARD_HEIGHT = 480
COLUMN_WIDTH = 91.43
ROW_HEIGHT = 480 / 6
PIECE_RADIUS = 35

SENTINEL_VALUE = 1000 #a position out of bounds
COLUMNS = 7
ROW = 6

#colors
RED = (255,0,0)
YELLOW = (255,255,0)


pygame.init()
logo = pygame.image.load("billeder/logo.png")
pygame.display.set_icon(logo)
window = pygame.display.set_mode((GAMEBOARD_WIDTH,GAMEBOARD_HEIGHT+40)) #each column = 91,43 #højden af billedet er 480 - tilføjer 40 for at man kan se hvis tur det er
pygame.display.set_caption("Connect Four")

bg = pygame.image.load('billeder/bg.png')

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
		#gamePosOfRow,gamePosOfColumn = codePosToGamePosRect(row,column)
		gamePosOfRow,gamePosOfColumn = codePosToGamePosCircle(row,column)
		print(gamePosOfRow)
		print(gamePosOfColumn)
		pygame.draw.circle(window,RED if isRed else YELLOW,(gamePosOfColumn,gamePosOfRow),PIECE_RADIUS+5,100) #+5 to make sure all is covered
		#pygame.draw.rect(window,RED if isRed else YELLOW,(gamePosOfColumn,gamePosOfRow,COLUMN_WIDTH,ROW_HEIGHT)) #lav cirkler i stedet?



#helper for Gameboard self.piecesInGameboardArray:
a = [[0]*8 for y in range(7)]
i = 0
while i < 7:
    a[0][i] = SENTINEL_VALUE
    a[i][0] = SENTINEL_VALUE
    i += 1
a[0][7] = SENTINEL_VALUE 

class Gameboard():
	def __init__(self):
		#this value counts how many brikker that is in each of the columns (1-7 columns) - (0-6 pieces in each column)
		self.columnCounter = [SENTINEL_VALUE,0,0,0,0,0,0,0]#first value is sentiel, since columns start from 1 - rest have 0 in them to begin with
		# 0 = empty 1 = red, 2 = yellow SENTINEL_VALUE = invalid Position
		self.piecesInGameboardArray = a
		self.pieces = []#DO NOT TOUCH - for all the pieces
	def addToColumnCounter(self,column):
		self.columnCounter[column] += 1
	def addPiecesToGameboard(self,column,isRed):
		piecesInColumn = self.columnCounter[column]
		self.piecesInGameboardArray[piecesInColumn+1][column] = 1 if isRed else 2 #add piece to code
		self.addPieceToVisualGameboard(isRed,piecesInColumn+1,column) #add piece visually
		self.columnCounter[column] += 1 
		print(self.piecesInGameboardArray)
	def addPieceToVisualGameboard(self,isRed,row,column):
		self.pieces.append(Piece(isRed,row,column))
	#make piece from Piece object - put it in position depending on




gameboard = Gameboard()
#21 af hver - lav alle brikkerne på forhånd i lister - kombiner med columnIsNotFull()
class PlayerTurnDisplay(): #create 2 instances - with each color, and make the other one invisible/have white color when not their turn / change its position to out of bounds
	def __init__(self,isRed,player):
		self.textbox = pygame.draw.rect(window,(0,0,0),(0,480,640,40))
		self.playerText = pygame.image.load(f"billeder/playerTurn/{str(player)}_{'red' if isRed else 'yellow'}.png")
	def isMyTurn(self): #changes the text position so it is visible
		pass
	def whoseTurnIsItAnyway(self,redsTurn):
		if (redsTurn and self.isRed) or (not redsTurn and not self.isRed):
			self.displayWhoseTurn(self.position)
		else:
			removeDisplayWhoseTurn(self.position)
	def displayWhoseTurn(self,position): #sentinel position if not active - otherwise defined position #must be tuple or list of position x,y
		#denne funktion skal kaldes af en anden funktion
		window.blit(self.playerText,position)
	def removeDisplayWhoseTurn(self,position):
		window.blit(self.playerText,position) # skal ændres så den blot er hvid - skal sikre sig at displaywhoseTurn ikke stadig kører
		
playerRedTurn = PlayerTurnDisplay(True,1)
playerYellowTurn = PlayerTurnDisplay(False,2)

def columnOfMouseclick(): #returns false if it is an invalid position - else return the column of which it is. (starting at 0)
	for index,hitbox in enumerate(hitboxes):
		if hitbox.collidepoint(pos):
			return index
	return False

def doPlayerTurn(columnToPlacePiece,isRed):
	gameboard.addPiecesToGameboard(column,True)
	nextPlayersTurn()
		#find what position to place it with columnCounter(maybe call it in this func) 
		#change value of piecesInGameboardArray
		#call func that adds visually to board
		#manage turns

def nextPlayersTurn():
	pass


def validColumnSelected(column):
	return bool(column)

def columnNotFull(column):
	if gameboard.columnCounter[column] < 6:
		return True
	return False

def addPiece():
	#check mouse position - er det korrekt:
		#hvems tur er det - skal displayes i bunden
	pass

running = True



while running:
	
	window.blit(bg,[0,0])
	playerYellowTurn.displayWhoseTurn((640/2-(160/2),480)) #for debugging purpose - tjek dog størrelser - især find en måde at se størrelse på billede med pygame

	for event in pygame.event.get(): 
		
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONUP:
			clickedPos = pygame.mouse.get_pos()
			print(clickedPos)
			column = gamePosToCodePos(clickedPos)
			if (validColumnSelected(column) and columnNotFull(column)):
				doPlayerTurn(column,True)	
			#pos = pygame.mouse.get_pos()
			#clickedColumn = columnOfMouseclick()
			#x = columnIsNotFull(clickedColumn)
			#if clickedColumn and x:
			#	addPiece()
	pygame.display.update()

pygame.quit()

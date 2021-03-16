#take from chess.py (backup) - so splite the board into 7 parts and look for where the mouse is clicked and not collision
# Make an array/dictionary/object (class) - probably class, to keep track of how many pieces are in each column.
# make function to add to column - that takes which column (starting from 1) as parameter (0 is invalid)
# When 1 column is full make it so you cant put any more pieces in





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
COLUMN_WIDTH = 91.43
GAMEBOARD_WIDTH = 640
GAMEBOARD_HEIGHT = 480

SENTINEL_POSITION = (1000) #a position out of bounds
COLUMNS = 7
ROW = 6


pygame.init()
logo = pygame.image.load("billeder/logo.png")
pygame.display.set_icon(logo)
window = pygame.display.set_mode((GAMEBOARD_WIDTH,GAMEBOARD_HEIGHT+40)) #each column = 91,43 #højden af billedet er 480 - tilføjer 40 for at man kan se hvis tur det er
pygame.display.set_caption("Connect Four")

bg = pygame.image.load('billeder/bg.png')

def codePosToGamePos(codePos): #takes list as parameter
	gamePos = codePos.copy()
	return [(i-1)*COLUMN_WIDTH for i in gamePos]

def gamePosToCodePos(gamePos):
	codePos = list(gamePos)
	count = 1
	if codePos[1] > GAMEBOARD_HEIGHT:
		return 0
	while codePos[0] > COLUMN_WIDTH:
		codePos[0] -= COLUMN_WIDTH
		count += 1
	return count


def drawBoard(): #draws the squares of the board + the upper bounds
	columns = []
	topOfColumn = []
	for i in range(7):
		columns.append(pygame.draw.rect(window,(255,255,255),(i*COLUMN_WIDTH,0,COLUMN_WIDTH,480))) 
		topOfColumn.append(pygame.draw.rect(window,(255,0,0),(i*COLUMN_WIDTH,0,COLUMN_WIDTH-10,5))) #-10 to make sure it doesnt overlap with next column
	return columns,topOfColumn
hitboxes,topOfColumns = drawBoard()

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
		self.columnCounter = [SENTINEL_POSITION,0,0,0,0,0,0,0]#first value is sentiel, since columns start from 1 - rest have 0 in them to begin with
		# 0 = empty 1 = red, 2 = yellow SENTINEL_VALUE = invalid Position
		self.piecesInGameboardArray = a
	def addToColumnCounter(column):
		self.columnCounter[column] += 1
	def addToPiecesInGameboardArray(column,isRed):
		pass
		#find what position to place it with columnCounter(maybe call it in this func)
		#change value of piecesInGameboardArray
		#call func that adds visually to board
		#manage turns




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



def validColumnSelected(column):
	return bool(column)

def columnNotFull(column):
	if gameboard.columnCounter[column] < 7:
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
			column = gamePosToCodePos(clickedPos)
			if (validColumnSelected(column) and columnNotFull(column)):
				gameboard.addToColumnCounter(column)
				
			#pos = pygame.mouse.get_pos()
			#clickedColumn = columnOfMouseclick()
			#x = columnIsNotFull(clickedColumn)
			#if clickedColumn and x:
			#	addPiece()
	pygame.display.update()

pygame.quit()

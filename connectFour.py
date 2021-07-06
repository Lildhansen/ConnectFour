#draw.rect(window,(r,g,b),(distance_bredde,distance_højde,bredde,højde) ) 

#global variable for vertical check in recursive function:
foundFourInRow = False

#pip modules
import pygame,time,os,sys
import numpy as np

#own modules:
import utility as util
import mainMenu as menu
import mainGameDisplay as mainDisp
import endScreen
import gameboard as gb

#sizes
GAMEBOARD_WIDTH = 640
GAMEBOARD_HEIGHT = 480

#colors
RED = (255,0,0)
YELLOW = (255,255,0)
WHITE = (255, 255, 255)
LIGHT_BLUE = (30,144,255)

#global variable:
running = True

#pygame stuff
pygame.init()
logo = pygame.image.load("billeder/logo.png")
pygame.display.set_icon(logo)
window = pygame.display.set_mode((GAMEBOARD_WIDTH,GAMEBOARD_HEIGHT+40)) #each column = 91,43 #højden af billedet er 480 - tilføjer 40 for at man kan se hvis tur det er
pygame.display.set_caption("Connect Four")
bg = pygame.image.load('billeder/bg.png')

#class instances
#from main menu
player1RadioButton = menu.RadioButtonPlayerText(YELLOW,"Player 1:",75,240)
player2RadioButton = menu.RadioButtonPlayerText(RED,"Player 2:",75,310)
yellowRadioButtonColorText = menu.RadioButtonColorText(YELLOW,"Yellow:",160,200)
redRadioButtonColorText = menu.RadioButtonColorText(RED,"Red:",250,200)

yellowRadioButtons = [menu.RadioButton(True,YELLOW,True,150,240,window),menu.RadioButton(False,YELLOW,False,150,310,window)]
redRadioButtons = [menu.RadioButton(False,RED,True,240,240,window),menu.RadioButton(True,RED,False,240,310,window)]

exitGameButton = menu.ExitGameButton()
startGameButton = menu.StartGameButton()
#the function that handles a players turn if the selected a valid spot for their piece
def doPlayerTurn(columnToPlacePiece,isRed):
	gameboard.addPieceToGameboard(columnToPlacePiece,isRed)
	if len(gameboard.pieces) != 0:
		gameboard.isIntialTurn = False
	endGameState = gameboard.checkWinCondition(isRed) #a is used so we can get back to the main loop
	if endGameState != None:
		return endGameState
	else:
		nextPlayersTurn()

#makes sure its the correct player's turn - also that it is the correct color
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

#not sure how to move this function, since it uses player1/2turn. - den skal flyttes til utility hvis den kan
def findPlayerWhoWonBasedOnIfHeIsRedOrNot(isRed):
	if player1Turn.isRed == isRed:
		return player1Turn
	else:
		return player2Turn

#returns false if the colum is full, otherwise true
def columnNotFull(column):
	return gameboard.columnCounter[column] < 6

#the pop-up screen before the end screen if one of the player's won
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

#calling the appropiate functions before running the main game
def prepareMainGame():
	global gameboard
	gameboard = gb.Gameboard(True if player1RadioButton.color == RED else False,window)
	gameboard.isIntialTurn = True
	global player1Turn
	player1Turn = mainDisp.PlayerTurnDisplay(True if player1RadioButton.color == RED else False,1,window) #player 1
	global player2Turn
	player2Turn = mainDisp.PlayerTurnDisplay(True if player2RadioButton.color == RED else False,2,window)# player 2
	gameboard.pieces = []
	gameboard.resetGameboard()

#the function handling the main menu of the game - this function is the only one needed to call, as it will call the other
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
		menu.fixRadioButtons(yellowRadioButtons,redRadioButtons)
		menu.fixRadioButtonsVisually(yellowRadioButtons,redRadioButtons,player1RadioButton,player2RadioButton)
		#buttonText
		window.blit(player1RadioButton.text,player1RadioButton.textRect)
		window.blit(player2RadioButton.text,player2RadioButton.textRect)
		window.blit(yellowRadioButtonColorText.text,yellowRadioButtonColorText.textRect)
		window.blit(redRadioButtonColorText.text,redRadioButtonColorText.textRect)
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

#the function handling the end screen of the game
def endScreen(whoWonIsRed,endScreenRunning):
	hasExited = False
	playerWhoWon = findPlayerWhoWonBasedOnIfHeIsRedOrNot(gameboard.isRedsTurn) #whoevers turn it is, is the one who won
	while endScreenRunning:
		window.fill((0,0,0))
		pygame.draw.rect(window,(0,0,0),(0,0,GAMEBOARD_WIDTH,GAMEBOARD_HEIGHT+40))
		if whoWonIsRed == "tie":
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

#the function handling the main game and calls all the appropiate functions
def mainGame():
	window.fill(WHITE)
	running = True
	endGameState = None
	while running:
		window.blit(bg,[0,0])
		if gameboard.isIntialTurn:
			gameboard.displayBlackImage()
			player1Turn.displayWhoseTurn((GAMEBOARD_WIDTH/2-160/2,GAMEBOARD_HEIGHT))
		for event in pygame.event.get(): 
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				clickedPos = pygame.mouse.get_pos()	
				global column
				column = util.gamePosToCodePos(clickedPos)
				if (util.validColumnSelected(column) and columnNotFull(column)):
					endGameState = doPlayerTurn(column,gameboard.isRedsTurn)
					if endGameState != None:
						running = False
						pygame.display.update()
						if endGameState == "tie":
							endScreen.drawGamePreEndScreen(window)
						else:
							preEndScreen(endGameState)
		pygame.display.update()
	if endGameState != None:
		endScreen(endGameState, True)

if __name__ == "__main__":
	mainMenu()
	pygame.quit()

#to do:
"""
hovedmenu:
	#måske tilføj senere at de kan vælge mellem 5 farver
	#også tilføj at de kan vælge navn
"""
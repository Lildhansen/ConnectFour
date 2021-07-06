import pygame

GAMEBOARD_WIDTH = 640
GAMEBOARD_HEIGHT = 480
SENTINEL_POSITION = (1000,1000)

#the bottom text describing whose turn it is.
class PlayerTurnDisplay: 
	def __init__(self,isRed,player,window):
		self.playerText = pygame.image.load(f"billeder/playerTurn/{str(player)}_{'red' if isRed else 'yellow'}.png")
		self.playerWonText = pygame.image.load(f"billeder/smallPlayerWon/{str(player)}_{'red' if isRed else 'yellow'}.png")
		self.playerWonTextFinal = pygame.image.load(f"billeder/playerWon/{str(player)}_{'red' if isRed else 'yellow'}.png")
		self.player = player
		self.isRed = isRed
		self.window = window
		self.textbox = pygame.draw.rect(self.window,(0,0,0),(0,480,640,40))
		self.position = (GAMEBOARD_WIDTH/2-160/2,GAMEBOARD_HEIGHT) #160 is the width of the image
	def whoseTurnIsItAnyway(self,redsTurn):
		if (redsTurn and self.isRed) or (not redsTurn and not self.isRed):
			self.displayWhoseTurn(self.position)
		else:
			self.displayWhoseTurn(SENTINEL_POSITION)
	def displayWhoseTurn(self,position): #sentinel position if not active - otherwise defined position #must be tuple or list of position x,y
		self.window.blit(self.playerText,position)
	def removeDisplayWhoseTurn(self,position):
		self.window.blit(self.playerText,position) # 
		
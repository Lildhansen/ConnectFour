import pygame
GAMEBOARD_WIDTH = 640
GAMEBOARD_HEIGHT = 480

#the pop-up screen before the end screen if the game was a draw
def drawGamePreEndScreen(window):
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
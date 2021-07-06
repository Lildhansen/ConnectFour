#window fucker op

import pygame

GAMEBOARD_WIDTH = 640
GAMEBOARD_HEIGHT = 480
SENTINEL_POSITION = (1000,1000)

#colors
RED = (255,0,0)
YELLOW = (255,255,0)
WHITE = (255, 255, 255)
BLACK = (0,0,0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)
LIGHT_BLUE = (30,144,255)

#class representation of the player text used for the radio button
class RadioButtonPlayerText():
    def __init__(self,color,text,x,y):
        self.textString = text
        self.color = color
        self.x = x
        self.y = y
        self.font = pygame.font.Font('freesansbold.ttf', 25)
        self.text = self.font.render(text, True, self.color, LIGHT_BLUE)
        self.textRect = self.text.get_rect()
        self.textRect.center = (x,y)
    def changeColor(self,yellowIsActivated):
        if yellowIsActivated:
            self.color = YELLOW
        else:
            self.color = RED
        self.text = self.font.render(self.textString, True, self.color, LIGHT_BLUE)

#the color text used for the radio button
class RadioButtonColorText():
    def __init__(self,color,text,x,y):
        self.color = color
        self.x = x
        self.y = y
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.text = self.font.render(text, True, self.color, LIGHT_BLUE)
        self.textRect = self.text.get_rect()
        self.textRect.center = (x,y)

#the radiobutton itself
class RadioButton():
    def __init__(self,isActivated,color,forPlayerOne,x,y,window):
        self.isActivated = isActivated
        self.hasBeenActivated = False
        self.color = color
        self.forPlayerOne = forPlayerOne
        self.x = x
        self.y = y
        self.window = window
        self.button = None
        self.innerButton = None
        self.innerButtonCenter = None
    def showButton(self):
        self.button = pygame.draw.circle(self.window,WHITE,(self.x,self.y),15)
        self.innerButtonCenter = self.button.center
    def interactButton(self,activate):
        if activate:
            self.innerButton = pygame.draw.circle(self.window,self.color,(self.innerButtonCenter),10)
        else:
            self.innerButton = pygame.draw.circle(self.window,BLACK,SENTINEL_POSITION,10)
    def checkForCollision(self,position):
        if self.button.collidepoint(position):
            return True

#class representation of the start game button from the main menu
class StartGameButton:
    def __init__(self):
        self.font = pygame.font.Font('freesansbold.ttf', 80)
        self.text = self.font.render('Start Game', True, RED, BLUE)
        self.textRect = self.text.get_rect()
        self.textRect.center = (GAMEBOARD_WIDTH/2,GAMEBOARD_HEIGHT/2-120)
    def checkForCollision(self,position):
        if self.textRect.collidepoint(position):
            return True


#class representation of the exit game button from the main menu
class ExitGameButton:
    def __init__(self):
        self.font = pygame.font.Font('freesansbold.ttf', 80)
        self.text = self.font.render('Exit Game', True, RED, BLUE)
        self.textRect = self.text.get_rect()
        self.textRect.center = (GAMEBOARD_WIDTH/2,GAMEBOARD_HEIGHT/2+200)
    def checkForCollision(self,position):
        if self.textRect.collidepoint(position):
            return True

#DOESNT WORK - but an attempt at making an image blink.
def blinkImage(imageLocation,imageWidth):
    gameProceeded = False
    isBlinking = False
    clock = pygame.time.Clock()
    image = pygame.image.load(imageLocation)
    position = (GAMEBOARD_WIDTH/2-imageWidth/2,GAMEBOARD_HEIGHT/2) #444 is the width of the image
    
    while not gameProceeded:
        clock.tick(10)
        if isBlinking:
            #window.blit(image,SENTINEL_POSITION)
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

#keeps the properties of the radio buttons intact - depending on what button has been activated
def fixRadioButtons(yellowRadioButtons,redRadioButtons):
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

#depending on what button was pressed, the radio buttons are fixed visually	
def fixRadioButtonsVisually(yellowRadioButtons,redRadioButtons,player1RadioButton,player2RadioButton):
    i = 0
    while i < 2:
        yellowRadioButtons[i].interactButton(yellowRadioButtons[i].isActivated)
        redRadioButtons[i].interactButton(redRadioButtons[i].isActivated)
        i += 1
    player1RadioButton.changeColor(yellowRadioButtons[0].isActivated)
    player2RadioButton.changeColor(redRadioButtons[0].isActivated)
    #called in a loop to make sure only 1 player has 1 of the colors
    #also fixes the player-name to be that colour
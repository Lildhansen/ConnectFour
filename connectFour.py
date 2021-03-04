#to do:
#addPiece() function
#make window taller, make room for "player x turn" - in blue if he is blue and red if not (or whatever the colors are)
#create the turn based thingy - maybe with a boolean when a valid option is chosen
#check for win
#lav en draw.rect i det øverste hul for alle kolonner (måske kun gør den halv højde, for at være sikker på den under ikke rammer den, 
    #så man kan tjekke collision med brikkerne, og hvis den collider, låses den kolonne

#alternativt - lav det gamle chess hitbox med position i stedet for collision, hvis nu brikkerne dækker over collisionen

#draw.rect(window,(r,g,b),(distance_bredde,distance_højde,bredde,højde) ) 

import pygame,time

COLUMN_WIDTH = 91.43
SENTINEL_POSITION = (1000) #a position out of bounds

pygame.init()
logo = pygame.image.load("billeder/logo.png")
pygame.display.set_icon(logo)
window = pygame.display.set_mode((640,480+40)) #each column = 91,43 #højden af billedet er 480 - tilføjer 40 for at man kan se hvis tur det er
pygame.display.set_caption("Connect Four")

bg = pygame.image.load('billeder/bg.png')

def drawBoard():
    columns = []
    for i in range(7):
        columns.append(pygame.draw.rect(window,(255,255,255),(i*COLUMN_WIDTH,0,COLUMN_WIDTH,480)))
    return columns

class PlayerTurnDisplay(): #create 2 instances - with each color, and make the other one invisible/have white color when not their turn / change its position to out of bounds
    def __init__(self,isRed,player):
        self.textbox = pygame.draw.rect(window,(0,0,0),(0,480,640,40))
        self.playerText = pygame.image.load(f"billeder/playerTurn/{str(player)}_{'red' if isRed else 'yellow'}.png")
    def isMyTurn(self): #changes the text position so it is visible
        pass
    def whoseTurnIsItAnyway(self,redsTurn):
        if (redsTurn and self.isRed) or (not redsTurn and not self.isRed):
            pass
            #change position to right one
    def displayWhoseTurn(self,position): #sentinel position if not active - otherwise defined position #must be tuple or list of position x,y
        #denne funktion skal kaldes af en anden funktion
        window.blit(self.playerText,position)
        
playerRedTurn = PlayerTurnDisplay(True,1)
playerYellowTurn = PlayerTurnDisplay(False,2)


def addPiece():
    pass


running = True

hitboxes = drawBoard()

while running:
    
    window.blit(bg,[0,0])
    playerYellowTurn.displayWhoseTurn((640/2-(160/2),480)) #for debugging purpose - tjek dog størrelser - især find en måde at se størrelse på billede med pygame

    for event in pygame.event.get(): 
        
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            for hitbox in hitboxes:
                if hitbox.collidepoint(pos):
                    addPiece()
    pygame.display.update()

pygame.quit()

#to do:
#addPiece() function
#make window taller, make room for "player x turn" - in blue if he is blue and red if not (or whatever the colors are)
#create the turn based thingy - maybe with a boolean when a valid option is chosen
#check for win

#alternativt - lav det gamle chess hitbox med position i stedet for collision, hvis nu brikkerne dækker over collisionen

import pygame,time

COLUMN_WIDTH = 91.43

pygame.init()
logo = pygame.image.load("billeder/logo.png")
pygame.display.set_icon(logo)
window = pygame.display.set_mode((640,480)) #each column = 91,43
pygame.display.set_caption("Connect Four")

bg = pygame.image.load('billeder/bg.png')

def drawBoard():
    columns = []
    for i in range(7):
        columns.append(pygame.draw.rect(window,(255,255,255),(i*COLUMN_WIDTH,0,COLUMN_WIDTH,480)))
    return columns


def addPiece():
    pass


running = True

hitboxes = drawBoard()

while running:
    
    window.blit(bg,[0,0])

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

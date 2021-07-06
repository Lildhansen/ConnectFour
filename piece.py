import pygame
import utility as util

RED = (255,0,0)
YELLOW = (255,255,0)
PIECE_RADIUS = 35

#class representation of each piece, alltogether put into the gameboard
class Piece():
    def __init__(self,isRed,row,column,window):
        self.row = row
        self.column = column
        self.isRed = isRed
        self.window = window
        #gamePosOfRow,gamePosOfColumn = codePosToGamePosRect(row,column) #possible rect
        gamePosOfRow,gamePosOfColumn = util.codePosToGamePosCircle(self.row,self.column)
        pygame.draw.circle(self.window,RED if self.isRed else YELLOW,(gamePosOfColumn,gamePosOfRow-2),PIECE_RADIUS+5) #+5 and -2 to make sure all is covered
        #pygame.draw.rect(window,RED if isRed else YELLOW,(gamePosOfColumn,gamePosOfRow,COLUMN_WIDTH,ROW_HEIGHT)) #possible rect


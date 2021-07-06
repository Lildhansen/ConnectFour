#sizes
GAMEBOARD_WIDTH = 640
GAMEBOARD_HEIGHT = 480
COLUMN_WIDTH = 91.43
ROW_HEIGHT = 480 / 6
PIECE_RADIUS = 35

#converts code positions to game positions - for rect and circle, respectively
def codePosToGamePosRect(codeY,codeX): 
    return int(GAMEBOARD_HEIGHT - codeY*ROW_HEIGHT),int((codeX-1)*COLUMN_WIDTH)

def codePosToGamePosCircle(codeY,codeX): 
    return int(GAMEBOARD_HEIGHT - codeY*ROW_HEIGHT+PIECE_RADIUS+6),int((codeX-1)*COLUMN_WIDTH + PIECE_RADIUS+11 ) #de random tal er så det passer i figuren
	
#converts game position to code position
def gamePosToCodePos(gamePos): #works only for checking what column is pressed - doesnt look at rows
    codePos = list(gamePos)
    count = 1
    if codePos[1] > GAMEBOARD_HEIGHT:
        return 0
    while codePos[0] > COLUMN_WIDTH:
        codePos[0] -= COLUMN_WIDTH
        count += 1
    return count

#returns bool for whether the column selected is valid or not.
def validColumnSelected(column):
	return bool(column)
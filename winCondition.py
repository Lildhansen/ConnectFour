SENTINEL_VALUE = -1000

#checks win condition horizontally
def checkHorizontal(numInRows,locationOfYellowOrRedPieces,isRed):
	for	piecesInRow in numInRows:
		if piecesInRow > 3: #dvs der er mindst 4 på samme række:
			rowsWithMoreThan3Pieces = [i for i, x in enumerate(numInRows) if x == piecesInRow]
			for row in rowsWithMoreThan3Pieces:
				piecesInRow = []
				columnsOfPiecesInRow = []
				for piece in locationOfYellowOrRedPieces:
					if piece[0] == row:
						piecesInRow.append(piece)
				for row,column in piecesInRow:
					columnsOfPiecesInRow.append(column)
				counter = 1
				i = 0
				while i < len(columnsOfPiecesInRow)-1:
					if (columnsOfPiecesInRow[i] == columnsOfPiecesInRow[i+1]-1):
						counter += 1
					else:
						counter = 1
					i += 1
					if counter == 4:
						#game won
						return isRed

#checks win condition vertically
def checkVertical(numInColumns,locationOfYellowOrRedPieces,isRed):
	for piecesInColumn in numInColumns:
		if piecesInColumn > 3:
			columnsWithMoreThan3Pieces = [i for i, x in enumerate(numInColumns) if x == piecesInColumn]
			for column in columnsWithMoreThan3Pieces:
				piecesInColumns = []
				rowsOfPiecesInColumns = []
				for piece in locationOfYellowOrRedPieces:
					if piece[1] == column:
						piecesInColumns.append(piece)
				for row,column in piecesInColumns:
					rowsOfPiecesInColumns.append(row)
				counter = 1
				i = 0
				while i < len(rowsOfPiecesInColumns)-1:
					if (rowsOfPiecesInColumns[i] == rowsOfPiecesInColumns[i+1]-1):
						counter += 1	
					else:
						counter = 1
					i+=1
					if counter == 4:
						return isRed

#checks win condition diagonally
def checkDiagonal(numInRows,numInColumns,locationOfYellowOrRedPieces,isRed):
	check = checkForAtLeast1PieceIn4ConsecutiveRowsAndColumns(numInRows,numInColumns)
	if check == None:
		return None
	global foundFourInRow
	foundFourInRow = False
	checkDiagonalRecursive(locationOfYellowOrRedPieces,locationOfYellowOrRedPieces[0],1,0,None)
	if foundFourInRow:
		return isRed

#helper function used to reduce complexity of checkDiagonal
def checkForAtLeast1PieceIn4ConsecutiveRowsAndColumns(numInRows,numInColumns):
	count = 0
	for numInColumn in numInColumns: #make extra checks to prevent huge complexity
		if count == 4:
			break
		if numInColumn == SENTINEL_VALUE:
			continue
		if numInColumn > 0:
			count += 1
		else:
			count = 0
	if count < 4:
		return None
	count = 0
	for numInRow in numInRows:
		if count == 4:
			break
		if numInRow == SENTINEL_VALUE:
			continue
		if numInRow > 0:
			count += 1
		else:
			count = 0
	if count < 4:
		return None
	return True

#recursive function used to check win conditions diagonally in checkDiagonal
def checkDiagonalRecursive(allPieceLocations,pieceLocation,numFoundInARow,startingPieceIndex,direction):
	global foundFourInRow
	if (foundFourInRow):
		return True

	if numFoundInARow == 4:
		foundFourInRow = True


	if (direction == "NW" or direction == None) and ([pieceLocation[0]+1,pieceLocation[1]-1] in allPieceLocations.tolist()): 
		checkDiagonalRecursive(allPieceLocations,[pieceLocation[0]+1,pieceLocation[1]-1],numFoundInARow+1,startingPieceIndex,"NW")
	#NE
	if (direction == "NE" or direction == None) and ([pieceLocation[0]+1,pieceLocation[1]+1] in allPieceLocations.tolist()): 
		checkDiagonalRecursive(allPieceLocations,[pieceLocation[0]+1,pieceLocation[1]+1],numFoundInARow+1,startingPieceIndex,"NE")
	#SW
	if (direction == "SW" or direction == None) and [pieceLocation[0]-1,pieceLocation[1]-1] in allPieceLocations.tolist(): 
		checkDiagonalRecursive(allPieceLocations,[pieceLocation[0]-1,pieceLocation[1]-1],numFoundInARow+1,startingPieceIndex,"SW")
	#SE
	if (direction == "SE" or direction == None) and [pieceLocation[0]-1,pieceLocation[1]+1] in allPieceLocations.tolist(): 
		checkDiagonalRecursive(allPieceLocations,[pieceLocation[0]-1,pieceLocation[1]+1],numFoundInARow+1,startingPieceIndex,"SE")
	
	if direction == None:
		nextPieceIndex = allPieceLocations.tolist().index(allPieceLocations.tolist()[startingPieceIndex])+1

		if nextPieceIndex+1 == len(allPieceLocations):
			return False
		checkDiagonalRecursive(allPieceLocations,allPieceLocations[nextPieceIndex],1,nextPieceIndex,None)


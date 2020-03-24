import pygame, random
# Started on 3/22/2020 7:54 PM and completed on 3/23/2020 at 6:38 PM.

# THE CODE IS CURRENTLY FUNCTIONAL AND MESSY, NOT OPTIMIZED YET!
# Next, make initial random path (solution) and then you have to connect it to the rest of the puzzle
# Maybe sometimes test position + 2 to and connect it?
# Make the branch stop if the next block is at the edge of the array -> testForEdge

# Draw the path and then just draw walls afters. Add a wall if the value to the left is not thisVal +1 or thisVal -1
# Look for a zero, and set it to a value that is is touching (not 0 though)
# Or search for zeros and start new paths?

# I think I fixed the zeros, it will restart until there were no Zeros.

#TODO- Fix Loops things that wouldn't make a game playable?
#  - Change #screen shot
#Initialize all imported pygame modules.
pygame.init()

#Define game variables.
backgroudColour = (0,0,0)


mazeArray = []
COLS, ROWS = 0, 0

def positionInArray(coordinates): # [c, r]
	colPos = coordinates[0]
	rowPos = coordinates[1]

	if colPos >= 0 and colPos <= COLS-1 and rowPos >= 0 and rowPos <= ROWS-1:
		return True
	else: return False


def testForVal(coordinates): # [c, r]
	global mazeArray
	colPos = coordinates[0]
	rowPos = coordinates[1]

	if positionInArray(coordinates):
		if mazeArray[rowPos][colPos] > 0:
			return False
		if mazeArray[rowPos][colPos] == 0:
			# It is okay to place here...
			return True


def testForEdge(coordinates): # [c, r]
	global mazeArray
	colPos = coordinates[0]
	rowPos = coordinates[1]

	if colPos < 0 or colPos > COLS-1 or rowPos < 0 or rowPos > ROWS-1:
		return False
	else:
		return True


def getNewCoords(coordinates, direction):
	newC = coordinates[0] + direction[0]
	newR = coordinates[1] + direction[1]
	newCoords = [newC, newR]

	return newCoords


def getDirectsList(coordinates, direction): # [c, r], [-1/1/0, -1/1/0]
	global mazeArray
	possDirList = [[0, -1], [0, 1], [-1, 0], [1, 0]] # U, D, L, R

	# Dont use direction (filter it out).
	for elem in possDirList:
		if elem == direction:
			possDirList.remove(elem)

	# Dont use direction (filter it out). You may run into problems of the range not working, but it should always be the four directions minus the one passed through.
	for i in range(4-1):

		if positionInArray(getNewCoords(coordinates, possDirList[i])) and not testForVal(getNewCoords(coordinates, possDirList[i])):
			possDirList[i] = 0
		
		elif not testForEdge(getNewCoords(coordinates, possDirList[i])):
			possDirList[i] = 0

		
	newList = list(filter(lambda x: (x != 0), possDirList))

	# Should only leave the valid directions
	return newList


def oppositeDirection(direction):
	for elem in range(2):
		direction[elem] = -1 * int(direction[elem])
	
	return direction


def seachForZeros():
	global mazeArray

	for r in range(ROWS):
		for c in range(COLS):
			if mazeArray[c][r] == 0:
				possibleDirections = [[0, -1], [0, 1], [-1, 0], [1, 0]]
				random.shuffle(possibleDirections)

				for i in range(0, len(possibleDirections)-1):
					newC = getNewCoords([c, r], possibleDirections[i])
					if not testForVal(newC) and positionInArray(newC) and positionInArray([c, r]):
						mazeArray[c][r] = mazeArray[newC[1]][newC[0]]
						#print('Found a zero')
						break


def newBranch(coordinates, direction, number):
	global mazeArray, testArray
	c, r = coordinates

	if positionInArray(coordinates):
		mazeArray[r][c] = number

	possibleDirections = getDirectsList(coordinates, oppositeDirection(direction)) # Don't want it to go backwards.
	random.shuffle(possibleDirections)

	if len(possibleDirections) > 0:
		# Start off by making one more definitive branch
		newC = getNewCoords(coordinates, possibleDirections[0])
		if testForVal(newC):
			newBranch(newC, possibleDirections[0], number + 1)
	
		if len(possibleDirections) > 1:
			FiftyFifty = random.randint(0,2)
			if FiftyFifty == 1:
				
				newCo = getNewCoords(coordinates, possibleDirections[1])
				if testForVal(newCo):
					newBranch(newCo, possibleDirections[1], number + 1)

			if len(possibleDirections) > 2:
				FiftyFiftyy = random.randint(0,3)
				if FiftyFiftyy == 1:
					newCoo = getNewCoords(coordinates, possibleDirections[1])
					if testForVal(newCoo):
						newBranch(newCoo, possibleDirections[1], number + 1)


	else:
		#print("I cannot go any further!")
		return True


def generateMaze(size):
	global mazeArray
	global ROWS
	global COLS
	ROWS = size
	COLS = size
	mazeArray = []
	for rows in range(ROWS):
		thisRow = []

		for cols in range(COLS):
			thisRow.append(0)

		mazeArray.append(thisRow)

	while any(0 in sublist for sublist in mazeArray):
		mazeArray = []
		for rows in range(ROWS):
			thisRow = []

			for cols in range(COLS):
				thisRow.append(0)

			mazeArray.append(thisRow)
		
		newBranch([3,3], [0,1], 1)

	return mazeArray
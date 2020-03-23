import pygame, random, sys
# Started on 3/22/2020 7:54 PM and completed on 3/23/2020 at 6:38 PM.

# THE CODE IS CURRENTLY FUNCTIONAL AND MESSY, NOT OPTIMIZED YET!
# Next, make initial random path (solution) and then you have to connect it to the rest of the puzzle
# Maybe sometimes test position + 2 to and connect it?
# Make the branch stop if the next block is at the edge of the array -> testForEdge

# Draw the path and then just draw walls afters. Add a wall if the value to the left is not thisVal +1 or thisVal -1
# Look for a zero, and set it to a value that is is touching (not 0 though)
# Or search for zeros and start new paths?

#Initialize all imported pygame modules.
pygame.init()

#Define game variables.
SIZE = 13
WIN_WIDTH = (SIZE*30)+30
WIN_HEIGHT = (SIZE*30)+30
ROWS = SIZE
COLS = SIZE
backgroudColour = (0,0,0)

cursorEvent = pygame.event.poll()

timeElapsed = 0
clock = pygame.time.Clock()

notRunning = False

mazeArray = []
for rows in range(ROWS):
	thisRow = []

	for cols in range(COLS):
		thisRow.append(0)

	mazeArray.append(thisRow)

#Set up the Pygame window.
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Maze')

screen.fill(backgroudColour)

# Reusable function to return desired text object, which can be displayed.
def drawText(labelText, xPos, yPos):
	font = pygame.font.Font('freesansbold.ttf', 16)
	text = font.render(labelText, True, (255, 255, 255))
	textRect = text.get_rect()
	textRect.center = (xPos, yPos)
	return screen.blit(text, textRect)


def print_array():
	global mazeArray
	#print("\n")
	for i in range(ROWS):
		print(mazeArray[i])


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
			#print("Full: " + str(mazeArray[rowPos][colPos]))
			return False
		if mazeArray[rowPos][colPos] == 0:
			# It is okay to place here...
			return True


def testForEdge(coordinates): # [c, r]
	global mazeArray
	colPos = coordinates[0]
	rowPos = coordinates[1]

	#if colPos == 0 or colPos == COLS-1 or rowPos == 0 or rowPos == ROWS-1:
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

		#print("iTS greater than 1: " + str(testForVal(getNewCoords(coordinates, possDirList[i]))))
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


def displayStuff():
	lineSize = 3

	lineMarg = 15
	for row in range(ROWS):
		for col in range(COLS):
			#if mazeArray[row][col] == 2:
			#pygame.draw.rect(screen, (0, 250, 0), (col*30, row*30, 10, 10))
			UP = getNewCoords([col, row], [0, -1])
			LEFT = getNewCoords([col, row], [-1, 0])
			DOWN = getNewCoords([col, row], [0, 1])
			RIGHT = getNewCoords([col, row], [1, 0])

			# HERE: This can be more efficient
			if positionInArray(UP):
				if mazeArray[UP[1]][UP[0]] != mazeArray[row][col] + 1 and mazeArray[UP[1]][UP[0]] != mazeArray[row][col] -1:
					pygame.draw.line(screen, (255,255,255), (col*30 + 30 - lineMarg, row*30 + 30 - lineMarg), (col*30 + 30 + lineMarg, row*30 + 30 - lineMarg), lineSize)
			
			if positionInArray(DOWN):
				if mazeArray[DOWN[1]][DOWN[0]] != mazeArray[row][col] + 1 and mazeArray[DOWN[1]][DOWN[0]] != mazeArray[row][col] -1:
					pygame.draw.line(screen, (255,255,255), (col*30 + 30 - lineMarg, row*30 + 30 + lineMarg), (col*30 + 30 + lineMarg, row*30 + 30 + lineMarg), lineSize)

			if positionInArray(LEFT):
				if mazeArray[LEFT[1]][LEFT[0]] != mazeArray[row][col] + 1 and mazeArray[LEFT[1]][LEFT[0]] != mazeArray[row][col] -1:
					pygame.draw.line(screen, (255,255,255), (col*30 + 30 - lineMarg, row*30 + 30 - lineMarg), (col*30 + 30 - lineMarg, row*30 + 30 + lineMarg), lineSize)

			if positionInArray(RIGHT):
				if mazeArray[RIGHT[1]][RIGHT[0]] != mazeArray[row][col] + 1 and mazeArray[RIGHT[1]][RIGHT[0]] != mazeArray[row][col] -1:
					pygame.draw.line(screen, (255,255,255), (col*30 + 30 + lineMarg, row*30 + 30 - lineMarg), (col*30 + 30 + lineMarg, row*30 + 30 + lineMarg), lineSize)

			#pygame.draw.line(screen, (255,255,255), (col*30 + 30 - lineMarg, row*30 + 30 - lineMarg), (col*30 + 30 - lineMarg, row*30 + 30 - lineMarg), lineSize*2)
			pygame.draw.rect(screen, (255, 255, 255), (col*30 + 30 - lineMarg, row*30 + 30 - lineMarg, lineSize-1, lineSize-1)) #, lineSize*2

			pygame.draw.rect(screen, (255, 255, 255), (15, 15, WIN_WIDTH-30 , WIN_HEIGHT-30), lineSize)
			#drawText(str(mazeArray[row][col]), col*30 + 30, row*30 + 30)


def newBranch(coordinates, direction, number):
	global mazeArray
	#print_array()

	c, r = coordinates
	if positionInArray(coordinates):
		mazeArray[r][c] = number

	possibleDirections = getDirectsList(coordinates, oppositeDirection(direction)) # Don't want it to go backwards.
	random.shuffle(possibleDirections)

	#print("I can go these: " + str(possibleDirections))

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


	else: # If I can't go anywhere
		#print("I cannot go any further!")
		return True


newBranch([3,3], [0,1], 1)

seachForZeros()

# Main loop to update and draw the game in screen.
def gameLoop():
	global notRunning
	timeTracker = 0

	while not notRunning:
		timeTracker += 1

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					pygame.quit()

		# Do not update the images every single frame, however, key events are detected every frame.
		if timeTracker % 10 == 0:
			screen.fill(backgroudColour)
			displayStuff()

		pygame.display.flip()	
		clock.tick(60)

	#Stop processing coverField, wait for user to restart the game.
	while notRunning: 
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_SPACE:
					startGame()
			
		screen.fill(backgroudColour)

		#displayStuff()
		drawText("Press space to restart.", 175, 175)

		pygame.display.flip()

		clock.tick(60)

gameLoop()
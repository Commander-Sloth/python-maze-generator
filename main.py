import pygame
import time, sys, random
from mazeGenerator import generateMaze

#FIX SKIPPING THROUGH > Test the diagnonal, and make sure the others are close, if so, don't move. Basically the opposite boolean of the line
# Test from spot up if direction is up, and test from same spot if it is right.
# Function to test this?

pygame.init()

#Define game variables.
SIZE = 10 # >3
WIN_WIDTH = (SIZE*30)+30
WIN_HEIGHT = (SIZE*30)+30
ROWS = SIZE
COLS = SIZE
backgroudColour = (0,0,0)

playerArray = []
for rows in range(ROWS):
	thisRow = []

	for cols in range(COLS):
		thisRow.append(0)

	playerArray.append(thisRow)

mazeArray = generateMaze(SIZE)
# mazeArray = []
# for rows in range(ROWS):
# 	thisRow = []

# 	for cols in range(COLS):
# 		thisRow.append(0)

# 	mazeArray.append(thisRow)

cursorEvent = pygame.event.poll()

timeElapsed = 0
clock = pygame.time.Clock()

notRunning = False

#Set up the Pygame window.
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Maze')

screen.fill(backgroudColour)

# Reusable function to return desired text object, which can be displayed.
def drawText(labelText, xPos, yPos):
	font = pygame.font.Font('freesansbold.ttf', 16)
	text = font.render(labelText, True, (255, 0, 255))
	textRect = text.get_rect()
	textRect.center = (xPos, yPos)
	return screen.blit(text, textRect)


def print_array():
	global mazeArray
	for i in range(ROWS):
		print(mazeArray[i])


def positionInArray(coordinates): # [c, r]
	colPos = coordinates[0]
	rowPos = coordinates[1]

	if colPos >= 0 and colPos <= COLS-1 and rowPos >= 0 and rowPos <= ROWS-1:
		return True
	else: return False


def getNewCoords(coordinates, direction):
	newC = coordinates[0] + direction[0]
	newR = coordinates[1] + direction[1]
	newCoords = [newC, newR]

	return newCoords


def testForEdge(coordinates): # [c, r]
	global mazeArray
	colPos = coordinates[0]
	rowPos = coordinates[1]

	if colPos < 0 or colPos > COLS-1 or rowPos < 0 or rowPos > ROWS-1:
		return False
	else:
		return True


class player:
	def __init__(self):
		# These should be random
		self.x = random.randint(0,COLS-1)
		self.y = random.randint(0,ROWS-1)

	def updatePosition(self, direction):
		global playerArray, mazeArray
		

		playerArray[self.y][self.x] = 0
		newC = getNewCoords([self.x, self.y], direction)

		if testForEdge(newC): #positionInArray(getNewCoords(newC, direction)):
			if mazeArray[newC[1]][newC[0]] == int(mazeArray[self.y][self.x] + 1) or mazeArray[newC[1]][newC[0]] == int(mazeArray[self.y][self.x] - 1):
				if direction == [0,1]:
					self.y = self.y + 1
				elif direction == [0,-1]:
					self.y = self.y - 1
				elif direction == [1,0]:
					self.x = self.x + 1
				elif direction == [-1,0]:
					self.x = self.x - 1

				print("Updating position")
			else:
				print(str(mazeArray[newC[1]][newC[0]]) + " was not ~" + str(mazeArray[self.y][self.x]))

		playerArray[self.y][self.x] = 1#self.process() # or playerArray[self.y][self.x] = 1




	def process(self):
		global playerArray, mazeArray
			
		playerArray[self.y][self.x] = 1

Player = player()

def drawFixers():
	lineSize = 3

	lineMarg = 15
	for row in range(ROWS):
		for col in range(COLS):
			UP = getNewCoords([col, row], [0, -1])
			LEFT = getNewCoords([col, row], [-1, 0])
			DOWN = getNewCoords([col, row], [0, 1])
			RIGHT = getNewCoords([col, row], [1, 0])

			if positionInArray([col+1, row+1]) and positionInArray(RIGHT) and positionInArray(DOWN):
				if mazeArray[row+1][col+1] == mazeArray[row][col]:
					if (mazeArray[DOWN[1]][DOWN[0]] == mazeArray[row][col] + 1 or mazeArray[DOWN[1]][DOWN[0]] == mazeArray[row][col] -1) and (mazeArray[RIGHT[1]][RIGHT[0]] == mazeArray[row][col] + 1 or mazeArray[RIGHT[1]][RIGHT[0]] == mazeArray[row][col] -1):
						pygame.draw.line(screen, (255, 255, 255), (col*30 + 30 - lineMarg, row*30 + 30 + lineMarg), (col*30 + 30 + lineMarg, row*30 + 30 + lineMarg), lineSize)
					# OR RIGHT

			if positionInArray([col-1, row+1]) and positionInArray(LEFT) and positionInArray(DOWN):
				if mazeArray[row+1][col-1] == mazeArray[row][col]:
					if (mazeArray[DOWN[1]][DOWN[0]] == mazeArray[row][col] + 1 or mazeArray[DOWN[1]][DOWN[0]] == mazeArray[row][col] -1) and (mazeArray[LEFT[1]][LEFT[0]] == mazeArray[row][col] + 1 or mazeArray[LEFT[1]][LEFT[0]] == mazeArray[row][col] -1):
						pygame.draw.line(screen, (255, 255, 255), (col*30 + 30 - lineMarg, row*30 + 30 + lineMarg), (col*30 + 30 + lineMarg, row*30 + 30 + lineMarg), lineSize)
					# OR RIGHT


def displayStuff():
	lineSize = 3
	lineMarg = 15

	for row in range(ROWS):
		for col in range(COLS):
			UP = getNewCoords([col, row], [0, -1])
			LEFT = getNewCoords([col, row], [-1, 0])
			DOWN = getNewCoords([col, row], [0, 1])
			RIGHT = getNewCoords([col, row], [1, 0])

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

			pygame.draw.rect(screen, (255, 255, 255), (col*30 + 30 - lineMarg, row*30 + 30 - lineMarg, lineSize-1, lineSize-1))

			pygame.draw.rect(screen, (255, 255, 255), (15, 15, WIN_WIDTH-30 , WIN_HEIGHT-30), lineSize)
			#drawText(str(mazeArray[row][col]), col*30 + 30, row*30 + 30)

			if playerArray[row][col] > 0:
				pygame.draw.rect(screen, (230, 230, 230), (col*30 + 30 - lineMarg, row*30 + 30 - lineMarg, 30, 30))
				#drawText(str(mazeArray[row][col]), col*30 + 30, row*30 + 30)

	Player.process()


# Main loop to update and draw the game in screen.
def displayLoop():
	global notRunning
	timeTracker = 0

	while not notRunning:
		timeTracker += 1

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_SPACE:
					startGame()
				elif  event.key == pygame.K_q:
					pygame.quit()
				elif event.key == pygame.K_UP:
					Player.updatePosition([0,-1])
				elif event.key == pygame.K_DOWN:
					Player.updatePosition([0,1])
				elif event.key == pygame.K_RIGHT:
					Player.updatePosition([1,0])
				elif event.key == pygame.K_LEFT:
					Player.updatePosition([-1,0])

		# Do not update the images every single frame, however, key events are detected every frame.
		if timeTracker % 10 == 0:
			screen.fill(backgroudColour)
			displayStuff()
			drawFixers()

		pygame.display.flip()	
		clock.tick(60)

	#Stop processing coverField, wait for user to restart the game.
	while notRunning: 
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					pygame.quit()
			
		screen.fill(backgroudColour)

		#displayStuff()
		drawText("Press space to restart.", 175, 175)

		pygame.display.flip()

		clock.tick(60)

displayLoop()
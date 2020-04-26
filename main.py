import pygame
import time, sys, random
from mazeGenerator import generateMaze

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

mazeArray, wallArray = generateMaze(SIZE)

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
		global playerArray, mazeArray, wallArray
		
		newC = getNewCoords([self.x, self.y], direction)

		# Erase the player from the old position.
		playerArray[self.y][self.x] = 0

		if testForEdge(newC): #positionInArray(getNewCoords(newC, direction)):

			if direction == [0,1]:
				if wallArray[self.y][self.x].botWall == False and wallArray[newC[1]][newC[0]].topWall == False:
					self.y = self.y + 1
			elif direction == [0,-1]:
				if wallArray[self.y][self.x].topWall == False and wallArray[newC[1]][newC[0]].botWall == False:
					self.y = self.y - 1
			elif direction == [1,0]:
				if wallArray[self.y][self.x].rigWall == False and wallArray[newC[1]][newC[0]].lefWall == False:
						self.x = self.x + 1
			elif direction == [-1,0]:
				if wallArray[self.y][self.x].lefWall == False and wallArray[newC[1]][newC[0]].rigWall == False:
					self.x = self.x - 1

		# Redraw the player at the new coordinates.
		playerArray[self.y][self.x] = 1 #self.process() # or playerArray[self.y][self.x] = 1


	def process(self):
		global playerArray, mazeArray
			
		playerArray[self.y][self.x] = 1

Player = player()

def displayStuff():
	lineSize = 3
	lineMarg = 15

	for row in range(ROWS):
		for col in range(COLS):
			x =col*30+30
			y =row*30+30
			if wallArray[row][col].topWall == True:
				pygame.draw.line(screen, (255,255,255), (x-lineMarg, y-lineMarg), (x+lineMarg, y-lineMarg), lineSize)
			if wallArray[row][col].botWall == True:
				pygame.draw.line(screen, (255,255,255), (x-lineMarg, y+lineMarg), (x+lineMarg, y+lineMarg), lineSize)
			if wallArray[row][col].rigWall == True:
				pygame.draw.line(screen, (255,255,255), (x+lineMarg, y-lineMarg), (x+lineMarg, y+lineMarg), lineSize)
			if wallArray[row][col].lefWall == True:
				pygame.draw.line(screen, (255,255,255), (x-lineMarg, y-lineMarg), (x-lineMarg, y+lineMarg), lineSize)

			if playerArray[row][col] > 0:
				pygame.draw.rect(screen, (230, 230, 230), (x-lineMarg+4, y-lineMarg+4, 22, 22))
			
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
			#drawFixers()

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